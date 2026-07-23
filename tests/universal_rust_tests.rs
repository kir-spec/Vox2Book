use vox2book::models::Genre;
use vox2book::editors::typography::apply_typography;
use vox2book::editors::literary::proofread_literary_text;
use vox2book::cleaners::stt_purger::clean_stt;
use vox2book::extractors::text_reader::read_plain_text;
use vox2book::process_literature_project;
use tempfile::NamedTempFile;
use std::io::Write;
use encoding_rs::WINDOWS_1251;

#[test]
fn test_literary_proofreading_engine() {
    let raw = "я я пошел в магазин ну потому что мне нужно было купить хлеба но я забыл деньги или.";
    let (cleaned, stats) = proofread_literary_text(raw);
    println!("DEBUG CLEANED OUTPUT: '{}'", cleaned);

    assert!(!cleaned.contains("я я"), "Repeated words were not removed");
    assert!(!cleaned.contains(" ну "), "Filler word 'ну' was not removed");
    assert!(cleaned.contains(", потому что"), "Comma before subordinate conjunction was not inserted");
    assert!(cleaned.contains(", но"), "Comma before 'но' was not inserted");
    assert!(!cleaned.ends_with("или."), "Cut-off conjunction 'или.' at sentence end was not trimmed");
    assert!(cleaned.starts_with('Я'), "First sentence character was not capitalized");
    assert!(stats.commas_added >= 2, "Comma statistics failed");
}

#[test]
fn test_windows_1251_decoding() {
    let cp1251_text = "Глава 1. Привет мир из Windows-1251 кодировки.";
    let (encoded_bytes, _, _) = WINDOWS_1251.encode(cp1251_text);

    let mut tmp_in = NamedTempFile::new().unwrap();
    tmp_in.write_all(&encoded_bytes).unwrap();

    let (elements, genre) = read_plain_text(tmp_in.path(), Genre::Auto);
    assert_eq!(genre, Genre::Prose);
    assert!(!elements.is_empty(), "Failed to read Windows-1251 encoded file");
    assert!(elements[0].body.contains("Привет мир"), "Windows-1251 content decoded incorrectly");
}

#[test]
fn test_utf8_bom_decoding() {
    let bom_text = "\u{feff}Глава 1. Текст с UTF-8 BOM сигнатурой.";
    let mut tmp_in = NamedTempFile::new().unwrap();
    tmp_in.write_all(bom_text.as_bytes()).unwrap();

    let (elements, _) = read_plain_text(tmp_in.path(), Genre::Auto);
    assert!(!elements.is_empty(), "Failed to read UTF-8 BOM file");
    assert!(!elements[0].body.contains('\u{feff}'), "BOM signature was not stripped");
}

#[test]
fn test_typography_formatting() {
    let raw = "Он сказал: \"Привет\" - и пошёл из за угла вобщем все таки.";
    let res = apply_typography(raw);
    assert!(res.contains("«Привет»"), "Failed guillemets quotes");
    assert!(res.contains(" — "), "Failed em-dash");
    assert!(res.contains("из-за"), "Failed hyphenated iz-za");
    assert!(res.contains("в общем"), "Failed separate v obshem");
    assert!(res.contains("всё-таки"), "Failed hyphenated vse-taki");
}

#[test]
fn test_stt_cleanup() {
    let raw = "это пахевизм и не устранные динамики Quiz河";
    let res = clean_stt(raw);
    assert!(res.contains("пофигизм"), "Failed STT phonetic typo replacement");
    assert!(res.contains("встроенные динамики"), "Failed STT dynamics typo");
    assert!(!res.contains("Quiz河"), "Failed Whisper hallucination removal");
}

#[test]
fn test_prose_pipeline() {
    let prose = "Глава 1. Раздел первый\n\nСолнце ярко светило над горизонтом.\n\n- Нам пора отправляться в путь - сказал он.";
    let mut tmp_in = NamedTempFile::new().unwrap();
    let tmp_out = NamedTempFile::new().unwrap();
    writeln!(tmp_in, "{}", prose).unwrap();

    let res = process_literature_project(tmp_in.path(), tmp_out.path(), Genre::Prose, Some("Мой Роман"), None);
    assert!(res.is_ok(), "Prose pipeline failed");
    let elements = res.unwrap();
    assert!(elements.len() >= 3, "Insufficient elements generated for prose");
}

#[test]
fn test_poetry_pipeline() {
    let poem = "Глава I. Весна\n\nЯ помню чудное мгновенье:\nПередо мной явилась ты,\nКак мимолетное виденье,\nКак гений чистой красоты.";
    let mut tmp_in = NamedTempFile::new().unwrap();
    let tmp_out = NamedTempFile::new().unwrap();
    writeln!(tmp_in, "{}", poem).unwrap();

    let res = process_literature_project(tmp_in.path(), tmp_out.path(), Genre::Poetry, Some("Стихи"), None);
    assert!(res.is_ok(), "Poetry pipeline failed");
    let elements = res.unwrap();
    assert!(elements.len() >= 4, "Insufficient elements generated for poetry");
}

#[test]
fn test_drama_pipeline() {
    let play = "Глава I. Действие первое\n\nКИР (входит): Привет! Как твои дела?\nАНФИЯ: Всё отлично.\n(Звонок телефона)";
    let mut tmp_in = NamedTempFile::new().unwrap();
    let tmp_out = NamedTempFile::new().unwrap();
    writeln!(tmp_in, "{}", play).unwrap();

    let res = process_literature_project(tmp_in.path(), tmp_out.path(), Genre::Drama, Some("Пьеса"), None);
    assert!(res.is_ok(), "Drama pipeline failed");
    let elements = res.unwrap();
    assert!(elements.len() >= 3, "Insufficient elements generated for drama");
}
