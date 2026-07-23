use regex::Regex;
use std::sync::OnceLock;
use crate::editors::typography::apply_typography;
use crate::cleaners::stt_purger::clean_stt;

static RE_FILLER_WORDS: OnceLock<Regex> = OnceLock::new();
static RE_CONJUNCTION_COMMAS: OnceLock<Regex> = OnceLock::new();
static RE_SENTENCE_SPLIT: OnceLock<Regex> = OnceLock::new();
static RE_DOUBLE_SPACES: OnceLock<Regex> = OnceLock::new();

pub struct ProofreadStats {
    pub typos_fixed: usize,
    pub filler_removed: usize,
    pub commas_added: usize,
    pub sentences_restructured: usize,
}

fn remove_repeated_words(text: &str) -> (String, usize) {
    let mut words = Vec::new();
    let mut count = 0;
    let mut prev_lower = String::new();

    for token in text.split_whitespace() {
        let clean_word: String = token.chars().filter(|c| c.is_alphanumeric()).collect::<String>().to_lowercase();
        if !clean_word.is_empty() && clean_word == prev_lower {
            count += 1;
            continue; // Skip consecutive duplicate word
        }
        if !clean_word.is_empty() {
            prev_lower = clean_word;
        }
        words.push(token);
    }

    (words.join(" "), count)
}

pub fn proofread_literary_text(text: &str) -> (String, ProofreadStats) {
    let mut stats = ProofreadStats {
        typos_fixed: 0,
        filler_removed: 0,
        commas_added: 0,
        sentences_restructured: 0,
    };

    if text.trim().is_empty() {
        return (String::new(), stats);
    }

    // 1. Clean STT noise & phonetic typos
    let mut result = clean_stt(text);
    if result != text {
        stats.typos_fixed += 1;
    }

    // 2. Remove speech stutters and repeated words ("я я пошёл" -> "я пошёл")
    let (deduped, dup_count) = remove_repeated_words(&result);
    if dup_count > 0 {
        result = deduped;
        stats.typos_fixed += dup_count;
    }

    // 3. Remove oral speech filler words ("ну", "э-э", "как бы", "так сказать")
    let re_fillers = RE_FILLER_WORDS.get_or_init(|| {
        Regex::new(r"(?i)\b(ну|э-э|эм|как бы|так сказать|значит|в общем-то)\b").unwrap()
    });
    if re_fillers.is_match(&result) {
        result = re_fillers.replace_all(&result, "").to_string();
        stats.filler_removed += 1;
    }

    let re_spaces = RE_DOUBLE_SPACES.get_or_init(|| {
        Regex::new(r"\s+").unwrap()
    });
    result = re_spaces.replace_all(&result, " ").to_string();

    // 4. Insert missing commas before subordinate conjunctions (multi-word conjunctions MUST be matched first!)
    let re_commas = RE_CONJUNCTION_COMMAS.get_or_init(|| {
        Regex::new(r"(?i)([^.,!?:;—\s])\s+(потому что|так как|так что|для того чтобы|чтобы|который|которая|которое|которые|если|когда|что|но|а|зато)\b").unwrap()
    });

    let comma_matches = re_commas.find_iter(&result).count();
    if comma_matches > 0 {
        result = re_commas.replace_all(&result, "$1, $2").to_string();
        stats.commas_added += comma_matches;
    }

    // 5. Trim trailing cut-off conjunctions at sentence end ("мы пошли или." -> "Мы пошли.")
    let re_cut = Regex::new(r#"(?i)\s+(или|и|но|а|что|если|из-за|потому что|как|так как)\s*\.?$"#).unwrap();
    if re_cut.is_match(&result) {
        result = re_cut.replace_all(&result, ".").to_string();
        stats.sentences_restructured += 1;
    }

    // 6. Apply Russian publishing typography (guillemets, em-dashes, particles)
    result = apply_typography(&result);

    // 7. Capitalize first letter of sentences and ensure sentence end punctuation
    if let Some(first_char) = result.chars().next() {
        if first_char.is_lowercase() {
            let mut chars = result.chars();
            result = format!("{}{}", chars.next().unwrap().to_uppercase(), chars.as_str());
            stats.sentences_restructured += 1;
        }
    }

    let re_split = RE_SENTENCE_SPLIT.get_or_init(|| {
        Regex::new(r"([.!?])(\s+)([а-яa-z])").unwrap()
    });
    result = re_split.replace_all(&result, |caps: &regex::Captures| {
        format!("{}{}{}", &caps[1], &caps[2], caps[3].to_uppercase())
    }).to_string();

    if !result.is_empty() && !result.ends_with('.') && !result.ends_with('!') && !result.ends_with('?') && !result.ends_with("...") {
        result.push('.');
    }

    (result, stats)
}
