pub mod config;
pub mod models;
pub mod extractors;
pub mod cleaners;
pub mod editors;
pub mod validators;
pub mod builders;
pub mod gui;
pub mod logger;
pub mod llm;

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
use crate::llm::{process_with_ollama, smart_offline_restructure};

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

    // 2. Pre-process text (STT Header purge & tech terms restructuring)
    let mut preprocessed = Vec::new();
    for elem in raw_elements {
        if is_spam(&elem.body) {
            continue;
        }
        let mut clean_elem = elem;
        clean_elem.body = smart_offline_restructure(&clean_elem.body);
        clean_elem.body = clean_stt(&clean_elem.body);
        if !clean_elem.body.trim().is_empty() {
            preprocessed.push(clean_elem);
        }
    }

    // 3. Try Ollama AI Neural Network if available, or fallback to offline restructuring
    let mut final_elements = preprocessed;

    // Check if Ollama AI is reachable for deep neural proofreading
    let raw_text_combined: String = final_elements.iter().map(|e| e.body.as_str()).collect::<Vec<_>>().join("\n\n");
    if raw_text_combined.len() > 30 {
        VoxLogger::info("AI Engine", "Attempting deep neural proofreading via Ollama AI (llama3)...");
        match process_with_ollama(&raw_text_combined, "llama3") {
            Ok(ai_processed_text) => {
                VoxLogger::info("AI Engine", "[SUCCESS] Ollama AI neural proofreading complete!");
                let mut ai_elements = Vec::new();
                for para in ai_processed_text.split("\n\n") {
                    let trimmed = para.trim();
                    if !trimmed.is_empty() {
                        ai_elements.push(LiteratureElement {
                            element_type: crate::models::ElementType::Paragraph,
                            body: trimmed.to_string(),
                            edited_body: trimmed.to_string(),
                            speaker: None,
                        });
                    }
                }
                if !ai_elements.is_empty() {
                    final_elements = ai_elements;
                }
            }
            Err(e) => {
                VoxLogger::info("AI Engine", &format!("Ollama AI unavailable ({}), using smart offline restructuring engine.", e));
            }
        }
    }

    // 4. Genre-Specific Editing & Typography
    let processed = match final_genre {
        Genre::Poetry => {
            VoxLogger::info("Editors", "Applying Poetry & Stanza formatting pipeline");
            process_poetry(final_elements)
        }
        Genre::Drama => {
            VoxLogger::info("Editors", "Applying Drama & Stage Direction formatting pipeline");
            process_drama(final_elements)
        }
        _ => {
            VoxLogger::info("Editors", "Applying Prose & Chapter formatting pipeline");
            process_prose(final_elements)
        }
    };

    // 5. Quality Validation
    let issues = validate_cuts(&processed);
    if issues.is_empty() {
        VoxLogger::info("Validator", "Quality audit passed with zero cut-off issues.");
    } else {
        VoxLogger::warn("Validator", &format!("Quality audit detected {} potential sentence cut-offs.", issues.len()));
    }

    // 6. DOCX Generation
    VoxLogger::info("Builder", &format!("Building manuscript DOCX at: '{}'", out_str));
    build_docx_document(&processed, &output_path, &final_genre, title, subtitle)?;

    if let Ok(metadata) = std::fs::metadata(&output_path) {
        VoxLogger::info("Builder", &format!("[SUCCESS] DOCX manuscript generated successfully! File size: {} bytes", metadata.len()));
    } else {
        VoxLogger::info("Builder", "[SUCCESS] DOCX manuscript generated successfully!");
    }

    Ok(processed)
}
