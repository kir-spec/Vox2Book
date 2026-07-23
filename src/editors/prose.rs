use crate::models::{ElementType, LiteratureElement};
use crate::editors::typography::apply_typography;

pub fn process_prose(elements: Vec<LiteratureElement>) -> Vec<LiteratureElement> {
    elements.into_iter().filter_map(|mut elem| {
        let body = elem.body.trim();
        if body.is_empty() {
            return None;
        }

        let mut cleaned = apply_typography(body);

        match elem.element_type {
            ElementType::Heading => {
                elem.edited_body = cleaned;
                Some(elem)
            }
            _ => {
                if cleaned.starts_with('-') || cleaned.starts_with('—') {
                    cleaned = format!("— {}", cleaned.trim_start_matches(|c| c == '-' || c == '—').trim());
                }
                if let Some(first_char) = cleaned.chars().next() {
                    if first_char.is_lowercase() {
                        let mut chars = cleaned.chars();
                        cleaned = format!("{}{}", chars.next().unwrap().to_uppercase(), chars.as_str());
                    }
                }
                if !cleaned.ends_with('.') && !cleaned.ends_with('!') && !cleaned.ends_with('?') && !cleaned.ends_with("...") {
                    cleaned.push('.');
                }
                elem.edited_body = cleaned;
                Some(elem)
            }
        }
    }).collect()
}
