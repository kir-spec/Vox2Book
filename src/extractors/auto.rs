use std::path::Path;
use crate::models::{Genre, LiteratureElement};
use crate::extractors::text_reader::read_plain_text;

pub fn extract_content<P: AsRef<Path>>(input_path: P, genre: Genre) -> (Vec<LiteratureElement>, Genre) {
    let path = input_path.as_ref();
    if path.is_file() {
        return read_plain_text(path, genre);
    }
    (Vec::new(), genre)
}
