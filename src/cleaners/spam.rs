use crate::config::{SPAM_EMOJIS, SPAM_KEYWORDS};

pub fn is_spam(text: &str) -> bool {
    let lower = text.to_lowercase();
    for kw in SPAM_KEYWORDS {
        if lower.contains(kw) {
            return true;
        }
    }

    for &emoji in SPAM_EMOJIS {
        if text.contains(emoji) {
            return true;
        }
    }

    false
}
