pub mod config;
pub mod models;
pub mod extractors;
pub mod cleaners;
pub mod editors;
pub mod validators;
pub mod builders;
pub mod gui;
pub mod logger;

use std::path::Path;
use crate::models::{Genre, LiteratureElement};
use crate::extractors::auto::extract_content;
use crate::cleaners::spam::is_spam;
use crate::cleaners::stt_purger::clean_stt;
use crate::editors::prose::process_prose;
use crate::editors::poetry::process_poetry;
use crate::editors::drama::process_drama;
use crate::validators::quality::validate_cuts;
use crate::builders::docx_builder::build_docx_document;
use crate::logger::VoxLogger;

pub fn process_literature_project<P: AsRef<Path>>(
    input_path: P,
    output_path: P,
    genre: Genre,
    title: Option<&str>,
    subtitle: Option<&str>,
) -> Result<Vec<LiteratureElement>, Box<dyn std::error::Error>> {
    let in_str = input_path.as_ref().to_string_lossy().to_string();
    let out_str = output_path.as_ref().to_string_lossy().to_string();

    VoxLogger::info("Engine", &format!("Starting publication pipeline for input: '{}'", in_str));
    VoxLogger::info("Engine", &format!("Requested genre mode: '{}'", genre));

    // 1. Extraction
    let (raw_elements, final_genre) = extract_content(&input_path, genre);
    VoxLogger::info("Extractor", &format!("Auto-detected genre: '{}', extracted {} raw elements", final_genre, raw_elements.len()));

    if raw_elements.is_empty() {
        VoxLogger::warn("Extractor", "No text elements could be extracted from input. Document may be empty.");
    }

    // 2. Spam & STT Purification
    let mut filtered = Vec::new();
    let mut spam_count = 0;

    for elem in raw_elements {
        if is_spam(&elem.body) {
            spam_count += 1;
            continue;
        }
        let mut clean_elem = elem;
        clean_elem.body = clean_stt(&clean_elem.body);
        filtered.push(clean_elem);
    }

    VoxLogger::info("Cleaners", &format!("Filtered {} spam elements, retained {} valid elements", spam_count, filtered.len()));

    // 3. Genre-Specific Editing & Typography
    let processed = match final_genre {
        Genre::Poetry => {
            VoxLogger::info("Editors", "Applying Poetry & Stanza formatting pipeline");
            process_poetry(filtered)
        }
        Genre::Drama => {
            VoxLogger::info("Editors", "Applying Drama & Stage Direction formatting pipeline");
            process_drama(filtered)
        }
        _ => {
            VoxLogger::info("Editors", "Applying Prose & Chapter formatting pipeline");
            process_prose(filtered)
        }
    };

    // 4. Quality Validation
    let issues = validate_cuts(&processed);
    if issues.is_empty() {
        VoxLogger::info("Validator", "Quality audit passed with zero cut-off issues.");
    } else {
        VoxLogger::warn("Validator", &format!("Quality audit detected {} potential sentence cut-offs.", issues.len()));
        for (line_num, conjunction, snippet) in issues.iter().take(3) {
            VoxLogger::warn("Validator", &format!("Line #{}: cut-off at '{}' -> Snippet: '{}'", line_num, conjunction, snippet));
        }
    }

    // 5. DOCX Generation
    VoxLogger::info("Builder", &format!("Building manuscript DOCX at: '{}'", out_str));
    build_docx_document(&processed, &output_path, &final_genre, title, subtitle)?;

    if let Ok(metadata) = std::fs::metadata(&output_path) {
        VoxLogger::info("Builder", &format!("[SUCCESS] DOCX manuscript generated successfully! File size: {} bytes", metadata.len()));
    } else {
        VoxLogger::info("Builder", "[SUCCESS] DOCX manuscript generated successfully!");
    }

    Ok(processed)
}
