use crate::models::{ElementType, LiteratureElement};
use crate::editors::literary::proofread_literary_text;

pub fn process_prose(elements: Vec<LiteratureElement>) -> Vec<LiteratureElement> {
    elements.into_iter().filter_map(|mut elem| {
        let body = elem.body.trim();
        if body.is_empty() {
            return None;
        }

        let (mut cleaned, _stats) = proofread_literary_text(body);

        match elem.element_type {
            ElementType::Heading => {
                elem.edited_body = cleaned;
                Some(elem)
            }
            _ => {
                if cleaned.starts_with('-') || cleaned.starts_with('—') {
                    cleaned = format!("— {}", cleaned.trim_start_matches(|c| c == '-' || c == '—').trim());
                }
                elem.edited_body = cleaned;
                Some(elem)
            }
        }
    }).collect()
}
