pub const PROJECT_NAME: &str = "Vox2Book";
pub const PROJECT_DESCRIPTION: &str = "Universal Literature Processing & Automated Publishing Engine (Rust Edition)";

pub const SPAM_KEYWORDS: &[&str] = &[
    "#Мультимедиа", "#Видео", "#ТВ", "#Новости", "#Игры", "#Приложения",
    "Free Software", "Official link", "@ApkGeek", "Разблокирован Premium",
    "Разблокирован PRO", "Подписаться на канал", "ВОРОВСТВО АККАУНТОВ",
    "Особенности:", "💫 Обновление", "🔑 Разблокирован", "сообщают эксперты",
    "сообщают финансовые эксперты", "Скидочный бот", "Нажми чтобы найти песню",
    "источник:", "читать далее"
];

pub const SPAM_EMOJIS: &[&str] = &[
    "‼️", "❗️", "❌", "⚡", "✅", "🔥", "📌", "💫", "💡", "⚙", "🔑", "📱", "🎁", "🚀", "💰"
];

pub const WHISPER_HALLUCINATION_PATTERNS: &[&str] = &[
    r"Quiz河\w*", r"quero\w*", r"göra", r"lijuria", r"sis Bushawa", r"Dew archа",
    r"tocar или lijuria", r"ежно-демонquent", r"дичайший пахевизм", r"При sings", r"Этоьте себя",
    r"DimaTorzok", r"Субтитры делал.*", r"Продолжение следует.*", r"незабудьте подписаться",
    r"подпишитесь на канал", r"ставьте лайки"
];

pub const MONTHS_RU: &[&str] = &[
    "", "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
];

pub const DEFAULT_COLOR_PALETTE: &[(u8, u8, u8)] = &[
    (0x1F, 0x49, 0x7D), // Dark Blue
    (0x80, 0x00, 0x40), // Burgundy
    (0x2E, 0x75, 0xB6), // Medium Blue
    (0x70, 0x30, 0xA0), // Purple
    (0xC6, 0x59, 0x11), // Dark Orange
];
