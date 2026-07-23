use crate::models::{ElementType, LiteratureElement};
use crate::editors::typography::apply_typography;

pub fn process_poetry(elements: Vec<LiteratureElement>) -> Vec<LiteratureElement> {
    elements.into_iter().filter_map(|mut elem| {
        if matches!(elem.element_type, ElementType::StanzaBreak) {
            elem.edited_body = String::new();
            return Some(elem);
        }

        let body = elem.body.trim();
        if body.is_empty() {
            return None;
        }

        let mut cleaned = apply_typography(body);
        if let Some(first_char) = cleaned.chars().next() {
            if first_char.is_lowercase() {
                let mut chars = cleaned.chars();
                cleaned = format!("{}{}", chars.next().unwrap().to_uppercase(), chars.as_str());
            }
        }

        elem.edited_body = cleaned;
        Some(elem)
    }).collect()
}
