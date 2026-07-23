pub mod config;
pub mod models;
pub mod extractors;
pub mod cleaners;
pub mod editors;
pub mod validators;
pub mod builders;

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

pub fn process_literature_project<P: AsRef<Path>>(
    input_path: P,
    output_path: P,
    genre: Genre,
    title: Option<&str>,
    subtitle: Option<&str>,
) -> Result<Vec<LiteratureElement>, Box<dyn std::error::Error>> {
    println!("=== Vox2Book Engine (Rust) ===");
    println!("Input path: {:?}", input_path.as_ref());
    println!("Requested genre: {}", genre);

    let (raw_elements, final_genre) = extract_content(&input_path, genre);
    println!("Detected genre: {}, elements extracted: {}", final_genre, raw_elements.len());

    let mut filtered = Vec::new();
    for elem in raw_elements {
        if is_spam(&elem.body) {
            continue;
        }
        let mut clean_elem = elem;
        clean_elem.body = clean_stt(&clean_elem.body);
        filtered.push(clean_elem);
    }

    let processed = match final_genre {
        Genre::Poetry => process_poetry(filtered),
        Genre::Drama => process_drama(filtered),
        _ => process_prose(filtered),
    };

    let issues = validate_cuts(&processed);
    println!("Validation completed. Potential issues found: {}", issues.len());

    build_docx_document(&processed, &output_path, &final_genre, title, subtitle)?;
    println!("[SUCCESS] Saved {} processed elements to {:?}", processed.len(), output_path.as_ref());

    Ok(processed)
}
