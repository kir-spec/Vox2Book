use regex::Regex;
use std::sync::OnceLock;
use crate::config::WHISPER_HALLUCINATION_PATTERNS;

static RE_TYPOS: OnceLock<Vec<(Regex, &'static str)>> = OnceLock::new();

pub fn clean_stt(text: &str) -> String {
    let mut res = text.to_string();

    for pattern in WHISPER_HALLUCINATION_PATTERNS {
        if let Ok(re) = Regex::new(&format!("(?i){}", pattern)) {
            res = re.replace_all(&res, "").to_string();
        }
    }

    let typos = RE_TYPOS.get_or_init(|| vec![
        (Regex::new(r"(?i)\bпахевизм\b").unwrap(), "пофигизм"),
        (Regex::new(r"(?i)\bне устранные динамики\b").unwrap(), "встроенные динамики"),
        (Regex::new(r"(?i)\bбабберест\b").unwrap(), "Wildberries"),
        (Regex::new(r"(?i)\bежифайр\b").unwrap(), "Edifier"),
        (Regex::new(r"(?i)\bаудиент\b").unwrap(), "Audient"),
    ]);

    for (re, replacement) in typos {
        res = re.replace_all(&res, *replacement).to_string();
    }

    res.trim().to_string()
}
