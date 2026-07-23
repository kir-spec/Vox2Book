use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

pub static SPAM_KEYWORDS: &[&str] = &[
    "подписывайтесь на канал",
    "ставьте лайки",
    "колокольчик",
    "спонсировать канал",
    "donationalerts",
];

pub static SPAM_EMOJIS: &[&str] = &["👍", "🔔", "❤️", "👉", "👇"];

pub static WHISPER_HALLUCINATION_PATTERNS: &[&str] = &[
    "Quiz河",
    "DimaTorzok",
    "Субтитры сделал",
    "Продолжение следует...",
    "Благодарю за просмотр",
    "Редактор субтитров",
];

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AppConfig {
    pub api_provider: String,
    pub api_key: String,
    pub model: String,
    pub ollama_url: String,
    pub genre: String,
    pub title: String,
    pub subtitle: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        Self {
            api_provider: "openai".to_string(),
            api_key: String::new(),
            model: "gpt-4o-mini".to_string(),
            ollama_url: "http://localhost:11434".to_string(),
            genre: "prose".to_string(),
            title: String::new(),
            subtitle: String::new(),
        }
    }
}

impl AppConfig {
    pub fn load_or_default<P: AsRef<Path>>(path: P) -> Self {
        if let Ok(content) = fs::read_to_string(path) {
            if let Ok(config) = serde_json::from_str(&content) {
                return config;
            }
        }
        Self::default()
    }
}
