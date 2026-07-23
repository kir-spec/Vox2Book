use regex::Regex;
use crate::models::LiteratureElement;

pub fn validate_cuts(elements: &[LiteratureElement]) -> Vec<(usize, String, String)> {
    let re_cut = Regex::new(r#"(?i)\s+(или|и|но|а|что|если|из-за|потому что|как|так как)\s*\.?$"#).unwrap();
    let mut issues = Vec::new();

    for (idx, elem) in elements.iter().enumerate() {
        let text = &elem.edited_body;
        if let Some(m) = re_cut.find(text) {
            issues.push((idx + 1, m.as_str().trim().to_string(), text.clone()));
        }
    }

    issues
}
