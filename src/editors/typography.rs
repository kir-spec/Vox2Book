use regex::Regex;
use std::sync::OnceLock;

static RE_QUOTES: OnceLock<Regex> = OnceLock::new();
static RE_DASH: OnceLock<Regex> = OnceLock::new();
static RE_PARTICLES_TO: OnceLock<Regex> = OnceLock::new();
static RE_PARTICLES_NIBUD: OnceLock<Regex> = OnceLock::new();
static RE_VSE_TAKI: OnceLock<Regex> = OnceLock::new();
static RE_IZ_ZA: OnceLock<Regex> = OnceLock::new();
static RE_IZ_POD: OnceLock<Regex> = OnceLock::new();
static RE_VOBSHEM: OnceLock<Regex> = OnceLock::new();
static RE_TOEST: OnceLock<Regex> = OnceLock::new();
static RE_VRYADLI: OnceLock<Regex> = OnceLock::new();
static RE_PUNCT_SPACE: OnceLock<Regex> = OnceLock::new();
static RE_MULTI_SPACE: OnceLock<Regex> = OnceLock::new();

pub fn apply_typography(text: &str) -> String {
    if text.trim().is_empty() {
        return String::new();
    }

    let re_quotes = RE_QUOTES.get_or_init(|| Regex::new(r#"(\s|^)"([^"]+)"(\s|[.,!?:;]|$)"#).unwrap());
    let re_dash = RE_DASH.get_or_init(|| Regex::new(r#"(\s+)-\s+"#).unwrap());
    let re_particles_to = RE_PARTICLES_TO.get_or_init(|| Regex::new(r#"(?i)\b(кое|где|кто|что|когда|как|куда)\s+то\b"#).unwrap());
    let re_particles_nibud = RE_PARTICLES_NIBUD.get_or_init(|| Regex::new(r#"(?i)\b(где|кто|что|когда|как|куда)\s+нибудь\b"#).unwrap());
    let re_vse_taki = RE_VSE_TAKI.get_or_init(|| Regex::new(r#"(?i)\bвс[её]\s+таки\b"#).unwrap());
    let re_iz_za = RE_IZ_ZA.get_or_init(|| Regex::new(r#"(?i)\bиз\s+за\b"#).unwrap());
    let re_iz_pod = RE_IZ_POD.get_or_init(|| Regex::new(r#"(?i)\bиз\s+под\b"#).unwrap());
    let re_vobshem = RE_VOBSHEM.get_or_init(|| Regex::new(r#"(?i)\bвобщем\b"#).unwrap());
    let re_toest = RE_TOEST.get_or_init(|| Regex::new(r#"(?i)\bтоесть\b"#).unwrap());
    let re_vryadli = RE_VRYADLI.get_or_init(|| Regex::new(r#"(?i)\bврядли\b"#).unwrap());
    let re_punct_space = RE_PUNCT_SPACE.get_or_init(|| Regex::new(r#"\s+([.,!?:;])"#).unwrap());
    let re_multi_space = RE_MULTI_SPACE.get_or_init(|| Regex::new(r#"\s+"#).unwrap());

    let mut res = text.to_string();
    res = re_quotes.replace_all(&res, "${1}«${2}»${3}").to_string();
    res = re_dash.replace_all(&res, " — ").to_string();
    res = re_particles_to.replace_all(&res, "${1}-то").to_string();
    res = re_particles_nibud.replace_all(&res, "${1}-нибудь").to_string();
    res = re_vse_taki.replace_all(&res, "всё-таки").to_string();
    res = re_iz_za.replace_all(&res, "из-за").to_string();
    res = re_iz_pod.replace_all(&res, "из-под").to_string();
    res = re_vobshem.replace_all(&res, "в общем").to_string();
    res = re_toest.replace_all(&res, "то есть").to_string();
    res = re_vryadli.replace_all(&res, "вряд ли").to_string();
    res = re_punct_space.replace_all(&res, "$1").to_string();
    res = re_multi_space.replace_all(&res, " ").to_string();

    res.trim().to_string()
}
