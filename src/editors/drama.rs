use crate::models::{ElementType, LiteratureElement};
use crate::editors::literary::proofread_literary_text;

pub fn process_drama(elements: Vec<LiteratureElement>) -> Vec<LiteratureElement> {
    elements.into_iter().filter_map(|mut elem| {
        let body = elem.body.trim();
        if body.is_empty() {
            return None;
        }

        let (cleaned, _stats) = proofread_literary_text(body);

        match elem.element_type {
            ElementType::CharacterName => {
                let mut caps = cleaned.to_uppercase();
                if !caps.ends_with('.') {
                    caps.push('.');
                }
                elem.edited_body = caps;
                Some(elem)
            }
            ElementType::StageDirection => {
                let mut sdir = cleaned;
                if !sdir.starts_with('(') {
                    sdir = format!("({})", sdir);
                }
                elem.edited_body = sdir;
                Some(elem)
            }
            _ => {
                elem.edited_body = cleaned;
                Some(elem)
            }
        }
    }).collect()
}
