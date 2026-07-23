use crate::config::{SPAM_EMOJIS, SPAM_KEYWORDS};

pub fn is_spam(text: &str) -> bool {
    let lower = text.to_lowercase();
    for kw in SPAM_KEYWORDS {
        if lower.contains(&kw.to_lowercase()) {
            return true;
        }
    }
    let mut emoji_count = 0;
    for emoji in SPAM_EMOJIS {
        if text.contains(emoji) {
            emoji_count += 1;
            if emoji_count >= 2 {
                return true;
            }
        }
    }
    false
}
