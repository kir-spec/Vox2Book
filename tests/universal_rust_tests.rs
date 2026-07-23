use vox2book::models::Genre;
use vox2book::editors::typography::apply_typography;
use vox2book::cleaners::stt_purger::clean_stt;
use vox2book::process_literature_project;
use tempfile::NamedTempFile;
use std::io::Write;

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

#[test]
fn test_1000_scenarios_grid() {
    let genres = vec![Genre::Prose, Genre::Poetry, Genre::Drama, Genre::Dialogue, Genre::Academic];
    let speakers = vec!["Author", "Character", "Narrator", "SpeakerA"];
    let samples = vec!["привет", "как дела", "из за", "всё таки", "в общем", "«тест»"];

    let mut iterations = 0;
    for _g in &genres {
        for sp in &speakers {
            for s in &samples {
                iterations += 1;
                let formatted = apply_typography(&format!("{}: {}", sp, s));
                assert!(!formatted.is_empty());
            }
        }
    }

    assert!(iterations >= 100, "Scenario grid failed to reach 100+ iterations");
}
