use std::sync::OnceLock;
use regex::Regex;

static RE_HEADER: OnceLock<Regex> = OnceLock::new();

pub const SYSTEM_PROMPT: &str = r#"Ты — профессиональный писатель, главный редактор и корректор литературного издательства.
Твоя задача — взять сырую устную расшифровку аудиозаписи (Whisper STT transcript) и превратить её в великолепный, чистый, грамотный и читаемый литературный текст.

ПРАВИЛА ОБРАБОТКИ:
1. Разбей сплошной монолог на логические абзацы и четкие, грамматически завершенные предложения.
2. Исправь все фонетические ошибки распознавания устной речи и сленга:
   - "ссд" / "ssd" -> SSD-накопитель
   - "те из бы" / "юсб" -> USB
   - "а дата" -> ADATA
   - "35 размер" -> 3.5-дюймовый
   - "планктом" -> планктон
   - "в стране джетал" -> Western Digital
   - "трансценд" -> Transcend
   - "самсунг" -> Samsung
3. Удали заикания, слова-паразиты ("ну", "э-э", "как бы", "в общем-то", "значит").
4. Сохрани 100% исходного смысла, живую интонацию и мысль автора, но сделай язык литературным и красивым.
5. Верни ТОЛЬКО вычитанный готовый текст книги без лишних вводных комментариев."#;

pub fn process_with_ollama(prompt: &str, model: &str) -> Result<String, String> {
    let client = reqwest::blocking::Client::builder()
        .timeout(std::time::Duration::from_secs(120))
        .build()
        .map_err(|e| format!("HTTP client error: {}", e))?;

    let payload = serde_json::json!({
        "model": if model.is_empty() { "llama3" } else { model },
        "prompt": format!("{}\n\nИсходный текст:\n{}", SYSTEM_PROMPT, prompt),
        "stream": false
    });

    let res = client.post("http://localhost:11434/api/generate")
        .json(&payload)
        .send()
        .map_err(|e| format!("Не удалось подключиться к Ollama (http://localhost:11434): {}", e))?;

    if !res.status().is_success() {
        return Err(format!("Ollama API error status: {}", res.status()));
    }

    let json_val: serde_json::Value = res.json().map_err(|e| format!("JSON parse error: {}", e))?;
    if let Some(resp_str) = json_val.get("response").and_then(|v| v.as_str()) {
        Ok(resp_str.trim().to_string())
    } else {
        Err("Пустой ответ от Ollama".to_string())
    }
}

pub fn smart_offline_restructure(text: &str) -> String {
    let mut clean = text.to_string();

    // Strip STT Header noise
    let re_hdr = RE_HEADER.get_or_init(|| {
        Regex::new(r"(?i)^(?:Source|Date|Duration|Model|----------+).*\n?").unwrap()
    });
    clean = re_hdr.replace_all(&clean, "").to_string();

    // Contextual tech terms correction
    clean = clean.replace("те из бы", "USB")
                 .replace("в стране джетал", "Western Digital")
                 .replace("а дата", "ADATA")
                 .replace("планктом", "планктон")
                 .replace("35 размер", "3.5\"")
                 .replace("2 и 5 размер", "2.5\"")
                 .replace("кармада", "карман (внешний бокс)")
                 .replace(" жестковую ", " жёсткому ");

    // Break long run-on monologue into paragraph chunks using discourse markers
    let re_break = Regex::new(r"(?i)\s+(поэтому|насчет|так вот|короче|кстати|а да по|в общем|в результате)\s+").unwrap();
    clean = re_break.replace_all(&clean, "\n\n$1 ").to_string();

    // Split sentences inside paragraphs by clauses
    let re_sent = Regex::new(r"(?i)\s+(потому что|так как|если|когда|хотя|чтобы|но|а|зато)\s+").unwrap();
    clean = re_sent.replace_all(&clean, ", $1 ").to_string();

    clean
}
