use crate::models::{ElementType, LiteratureElement};
use crate::editors::literary::proofread_literary_text;

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

        let (cleaned, _stats) = proofread_literary_text(body);
        elem.edited_body = cleaned;
        Some(elem)
    }).collect()
}
