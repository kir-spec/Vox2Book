use reqwest::blocking::Client;
use serde_json::json;
use std::time::Duration;
use crate::config::AppConfig;

pub const SYSTEM_PROMPT: &str = r#"Ты — главный редактор литературного издательства.
Твоя задача — взять сырую устную расшифровку аудиозаписи (Whisper STT transcript) и превратить её в вычитанный, чистый и грамотный литературный текст.

ПРАВИЛА:
1. Разбей сплошной монолог на логические абзацы и четкие предложения с правильной пунктуацией.
2. Исправь все ошибочные технические термины распознавания устной речи:
   - "ссд" / "ssd" -> SSD-накопитель
   - "те из бы" / "юсб" -> USB
   - "а дата" -> ADATA
   - "35 размер" -> 3.5-дюймовый
   - "планктом" -> планктон
   - "в стране джетал" -> Western Digital
   - "трансценд" -> Transcend
3. Удали слова-паразиты ("ну", "э-э", "как бы", "значит").
4. Сохрани авторский смысл, но сделай стиль литературным.
5. Верни ТОЛЬКО вычитанный готовый текст книги без вводных фраз."#;

pub fn call_neural_api(prompt: &str, config: &AppConfig) -> Result<String, String> {
    let client = Client::builder()
        .timeout(Duration::from_secs(180))
        .build()
        .map_err(|e| format!("HTTP Client Error: {}", e))?;

    let provider = config.api_provider.to_lowercase();

    match provider.as_str() {
        "openai" | "deepseek" => {
            let endpoint = if provider == "deepseek" {
                "https://api.deepseek.com/chat/completions"
            } else {
                "https://api.openai.com/v1/chat/completions"
            };

            let key = if config.api_key.trim().is_empty() {
                std::env::var("OPENAI_API_KEY").unwrap_or_default()
            } else {
                config.api_key.clone()
            };

            if key.trim().is_empty() {
                return Err("Ошибка: Укажите api_key в config.json или установленный OPENAI_API_KEY".to_string());
            }

            let payload = json!({
                "model": if config.model.is_empty() { "gpt-4o-mini" } else { &config.model },
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            });

            let res = client.post(endpoint)
                .header("Authorization", format!("Bearer {}", key.trim()))
                .header("Content-Type", "application/json")
                .json(&payload)
                .send()
                .map_err(|e| format!("Ошибка подключения к {}: {}", endpoint, e))?;

            let status = res.status();
            if !status.is_success() {
                let err_text = res.text().unwrap_or_default();
                return Err(format!("API Error (Status {}): {}", status, err_text));
            }

            let json_val: serde_json::Value = res.json().map_err(|e| format!("JSON Parse Error: {}", e))?;
            let content = json_val["choices"][0]["message"]["content"]
                .as_str()
                .unwrap_or("")
                .trim()
                .to_string();

            if content.is_empty() {
                Err("Пустой ответ от API".to_string())
            } else {
                Ok(content)
            }
        }
        "anthropic" | "claude" => {
            let key = if config.api_key.trim().is_empty() {
                std::env::var("ANTHROPIC_API_KEY").unwrap_or_default()
            } else {
                config.api_key.clone()
            };

            if key.trim().is_empty() {
                return Err("Ошибка: Укажите api_key для Anthropic Claude в config.json".to_string());
            }

            let payload = json!({
                "model": if config.model.is_empty() { "claude-3-5-sonnet-20240620" } else { &config.model },
                "max_tokens": 4096,
                "system": SYSTEM_PROMPT,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            });

            let res = client.post("https://api.anthropic.com/v1/messages")
                .header("x-api-key", key.trim())
                .header("anthropic-version", "2023-06-01")
                .header("Content-Type", "application/json")
                .json(&payload)
                .send()
                .map_err(|e| format!("Anthropic API Error: {}", e))?;

            let json_val: serde_json::Value = res.json().map_err(|e| format!("JSON Parse Error: {}", e))?;
            let content = json_val["content"][0]["text"]
                .as_str()
                .unwrap_or("")
                .trim()
                .to_string();

            if content.is_empty() {
                Err("Пустой ответ от Anthropic API".to_string())
            } else {
                Ok(content)
            }
        }
        "ollama" => {
            let url = if config.ollama_url.is_empty() { "http://localhost:11434" } else { &config.ollama_url };
            let payload = json!({
                "model": if config.model.is_empty() { "llama3" } else { &config.model },
                "prompt": format!("{}\n\nИсходный текст:\n{}", SYSTEM_PROMPT, prompt),
                "stream": false
            });

            let res = client.post(format!("{}/api/generate", url))
                .json(&payload)
                .send()
                .map_err(|e| format!("Ошибка соединения с Ollama ({}): {}", url, e))?;

            let json_val: serde_json::Value = res.json().map_err(|e| format!("JSON Parse Error: {}", e))?;
            let content = json_val["response"].as_str().unwrap_or("").trim().to_string();

            if content.is_empty() {
                Err("Пустой ответ от Ollama".to_string())
            } else {
                Ok(content)
            }
        }
        _ => Err(format!("Неизвестный провайдер API: {}. Допустимые: openai, deepseek, anthropic, ollama", provider)),
    }
}
