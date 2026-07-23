use std::fs::File;
use std::io::Read;
use std::path::Path;
use walkdir::WalkDir;
use zip::ZipArchive;
use regex::Regex;

use crate::models::{ElementType, Genre, LiteratureElement};
use crate::extractors::text_reader::read_plain_text;

pub fn read_docx_file<P: AsRef<Path>>(filepath: P) -> Vec<String> {
    let file = match File::open(filepath) {
        Ok(f) => f,
        Err(_) => return Vec::new(),
    };

    let mut archive = match ZipArchive::new(file) {
        Ok(a) => a,
        Err(_) => return Vec::new(),
    };

    let mut xml_content = String::new();
    if let Ok(mut doc_xml) = archive.by_name("word/document.xml") {
        let _ = doc_xml.read_to_string(&mut xml_content);
    }

    if xml_content.is_empty() {
        return Vec::new();
    }

    // Extract text from XML <w:p> paragraphs and <w:t> tags
    let re_p = Regex::new(r"(?s)<w:p\b[^>]*>(.*?)</w:p>").unwrap();
    let re_t = Regex::new(r"<w:t\b[^>]*>(.*?)</w:t>").unwrap();
    let re_tags = Regex::new(r"<[^>]+>").unwrap();

    let mut paragraphs = Vec::new();

    for cap_p in re_p.captures_iter(&xml_content) {
        let p_inner = &cap_p[1];
        let mut p_text = String::new();

        for cap_t in re_t.captures_iter(p_inner) {
            let text_snippet = &cap_t[1];
            let clean_snippet = re_tags.replace_all(text_snippet, "").to_string();
            p_text.push_str(&clean_snippet);
        }

        let trimmed = p_text.trim();
        if !trimmed.is_empty() {
            paragraphs.push(trimmed.to_string());
        }
    }

    paragraphs
}

pub fn extract_content<P: AsRef<Path>>(input_path: P, genre: Genre) -> (Vec<LiteratureElement>, Genre) {
    let path = input_path.as_ref();

    if !path.exists() {
        return (Vec::new(), genre);
    }

    // Handle single file
    if path.is_file() {
        let ext = path.extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();

        if ext == "docx" {
            let lines = read_docx_file(path);
            let mut elements = Vec::new();
            let re_heading = Regex::new(r"(?i)^(?:#+\s*|Глава\s+\d+|Часть\s+\d+|Акт\s+\d+|Chapter\s+\d+)").unwrap();

            for line in lines {
                if re_heading.is_match(&line) {
                    elements.push(LiteratureElement {
                        element_type: ElementType::Heading,
                        body: line.clone(),
                        edited_body: line,
                        speaker: None,
                    });
                } else {
                    elements.push(LiteratureElement {
                        element_type: ElementType::Paragraph,
                        body: line.clone(),
                        edited_body: line,
                        speaker: None,
                    });
                }
            }

            let final_genre = if genre == Genre::Auto { Genre::Prose } else { genre };
            return (elements, final_genre);
        }

        return read_plain_text(path, genre);
    }

    // Handle directory (recursively find all .txt, .md, .docx files)
    if path.is_dir() {
        let mut all_elements = Vec::new();
        let mut detected_genre = genre.clone();

        let mut files: Vec<_> = WalkDir::new(path)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.file_type().is_file())
            .collect();

        files.sort_by_key(|e| e.path().to_path_buf());

        for entry in files {
            let fpath = entry.path();
            let ext = fpath.extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();

            if ext == "txt" || ext == "md" {
                let (elems, g) = read_plain_text(fpath, genre.clone());
                if detected_genre == Genre::Auto && g != Genre::Auto {
                    detected_genre = g;
                }
                all_elements.extend(elems);
            } else if ext == "docx" {
                let lines = read_docx_file(fpath);
                for l in lines {
                    all_elements.push(LiteratureElement {
                        element_type: ElementType::Paragraph,
                        body: l.clone(),
                        edited_body: l,
                        speaker: None,
                    });
                }
            }
        }

        let final_g = if detected_genre == Genre::Auto { Genre::Prose } else { detected_genre };
        return (all_elements, final_g);
    }

    (Vec::new(), genre)
}
