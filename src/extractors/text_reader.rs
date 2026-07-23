use std::fs;
use std::path::Path;
use regex::Regex;
use encoding_rs::WINDOWS_1251;
use crate::models::{ElementType, Genre, LiteratureElement};

pub fn read_plain_text<P: AsRef<Path>>(filepath: P, default_genre: Genre) -> (Vec<LiteratureElement>, Genre) {
    let bytes = match fs::read(&filepath) {
        Ok(b) => b,
        Err(_) => return (Vec::new(), default_genre),
    };

    if bytes.is_empty() {
        return (Vec::new(), default_genre);
    }

    // 1. Strip UTF-8 BOM if present
    let raw_bytes = if bytes.starts_with(&[0xEF, 0xBB, 0xBF]) {
        &bytes[3..]
    } else {
        &bytes[..]
    };

    // 2. Multi-encoding decoding (UTF-8 -> Windows-1251 -> Lossy)
    let content = match std::str::from_utf8(raw_bytes) {
        Ok(s) => s.to_string(),
        Err(_) => {
            let (decoded, _, has_errors) = WINDOWS_1251.decode(raw_bytes);
            if !has_errors {
                decoded.into_owned()
            } else {
                String::from_utf8_lossy(raw_bytes).into_owned()
            }
        }
    };

    let lines: Vec<String> = content.lines().map(|l| l.to_string()).collect();

    let mut blank_lines = 0;
    let mut short_lines = 0;
    let mut drama_lines = 0;

    let re_heading = Regex::new(r"(?i)^(?:#+\s*|Глава\s+\d+|Часть\s+\d+|Акт\s+\d+|Сцена\s+\d+|Chapter\s+\d+)").unwrap();
    let re_drama_char = Regex::new(r"^([A-ZА-ЯЁ\s]{2,30})\s*(?:\((.*?)\))?[:.](.*)$").unwrap();

    for line in &lines {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            blank_lines += 1;
        } else {
            if trimmed.len() < 50 {
                short_lines += 1;
            }
            if re_drama_char.is_match(trimmed) {
                drama_lines += 1;
            }
        }
    }

    let detected_genre = match default_genre {
        Genre::Auto => {
            let total = lines.len().max(1);
            if drama_lines > 3 && (drama_lines as f64 / total as f64) > 0.05 {
                Genre::Drama
            } else if short_lines > 5 && (short_lines + blank_lines) as f64 / total as f64 > 0.4 {
                Genre::Poetry
            } else {
                Genre::Prose
            }
        }
        g => g,
    };

    let mut elements = Vec::new();

    for line in lines {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            if detected_genre == Genre::Poetry {
                elements.push(LiteratureElement {
                    element_type: ElementType::StanzaBreak,
                    body: String::new(),
                    edited_body: String::new(),
                    speaker: None,
                });
            }
            continue;
        }

        if re_heading.is_match(trimmed) {
            elements.push(LiteratureElement {
                element_type: ElementType::Heading,
                body: trimmed.to_string(),
                edited_body: trimmed.to_string(),
                speaker: None,
            });
            continue;
        }

        match detected_genre {
            Genre::Poetry => {
                elements.push(LiteratureElement {
                    element_type: ElementType::VerseLine,
                    body: trimmed.to_string(),
                    edited_body: trimmed.to_string(),
                    speaker: None,
                });
            }
            Genre::Drama => {
                if let Some(caps) = re_drama_char.captures(trimmed) {
                    let cname = caps.get(1).unwrap().as_str().trim().to_string();
                    let sdir = caps.get(2).map(|m| m.as_str().trim().to_string());
                    let dialogue = caps.get(3).unwrap().as_str().trim().to_string();

                    elements.push(LiteratureElement {
                        element_type: ElementType::CharacterName,
                        body: cname.clone(),
                        edited_body: cname.clone(),
                        speaker: Some(cname.clone()),
                    });

                    if let Some(sd) = sdir {
                        elements.push(LiteratureElement {
                            element_type: ElementType::StageDirection,
                            body: format!("({})", sd),
                            edited_body: format!("({})", sd),
                            speaker: Some(cname.clone()),
                        });
                    }

                    if !dialogue.is_empty() {
                        elements.push(LiteratureElement {
                            element_type: ElementType::Paragraph,
                            body: dialogue.clone(),
                            edited_body: dialogue,
                            speaker: Some(cname),
                        });
                    }
                } else if trimmed.starts_with('(') && trimmed.ends_with(')') {
                    elements.push(LiteratureElement {
                        element_type: ElementType::StageDirection,
                        body: trimmed.to_string(),
                        edited_body: trimmed.to_string(),
                        speaker: None,
                    });
                } else {
                    elements.push(LiteratureElement {
                        element_type: ElementType::Paragraph,
                        body: trimmed.to_string(),
                        edited_body: trimmed.to_string(),
                        speaker: None,
                    });
                }
            }
            _ => {
                elements.push(LiteratureElement {
                    element_type: ElementType::Paragraph,
                    body: trimmed.to_string(),
                    edited_body: trimmed.to_string(),
                    speaker: None,
                });
            }
        }
    }

    (elements, detected_genre)
}
