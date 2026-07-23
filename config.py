# Vox2Book — Universal Literature & Publishing Engine Configuration

PROJECT_NAME = "Vox2Book"
PROJECT_DESCRIPTION = "Universal Literature Processing & Publishing Engine (Prose, Poetry, Drama, Dialogue, Academic)"

SPAM_KEYWORDS = [
    "#Мультимедиа", "#Видео", "#ТВ", "#Новости", "#Игры", "#Приложения",
    "Free Software", "Official link", "@ApkGeek", "Разблокирован Premium",
    "Разблокирован PRO", "Подписаться на канал", "ВОРОВСТВО АККАУНТОВ",
    "Особенности:", "💫 Обновление", "🔑 Разблокирован", "сообщают эксперты",
    "сообщают финансовые эксперты", "Скидочный бот", "Нажми чтобы найти песню",
    "источник:", "читать далее"
]

SPAM_EMOJIS = ['‼️', '❗️', '❌', '⚡️', '✅', '🔥', '📌', '💫', '💡', '⚙️', '🔑', '📱', '🎁', '🚀', '💰']

ALLOWED_BRANDS = {
    'telegram', 'windows', 'apple', 'mac', 'ipad', 'iphone', 'youtube', 'whatsapp',
    'vk', 'siri', 'gpt', 'gemini', 'fifine', 'usb', 'vpn', 'pro', 'deluxe', 'apk',
    'bot', 'chatgpt', 'ozon', 'wildberries', 'headhunter', 'avito', 'android',
    'google', 'play', 'market', 'openai', 'dll', 'exe', 'app', 'store', 'music',
    'yandex', 'premium', 'software', 'link', 'o', 'mini', 'flash', 'thinking', 'ai', 'seeing',
    'audient', 'yamaha', 'edifier', 'litres', 'spotify', 'deezer', 'lookout', 'xlr'
}

WHISPER_HALLUCINATIONS = [
    r'Quiz河\w*', r'quero\w*', r'göra', r'lijuria', r'sis Bushawa', r'Dew archа',
    r'tocar или lijuria', r'ежно-демонquent', r'дичайший пахевизм', r'При sings', r'Этоьте себя',
    r'DimaTorzok', r'Субтитры делал.*', r'Продолжение следует.*', r'незабудьте подписаться',
    r'подпишитесь на канал', r'ставьте лайки'
]

MONTHS_RU = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

DEFAULT_SPEAKER_COLORS = [
    (0x1F, 0x49, 0x7D),  # Dark Blue
    (0x80, 0x00, 0x40),  # Burgundy / Magenta
    (0x2E, 0x75, 0xB6),  # Medium Blue
    (0x70, 0x30, 0xA0),  # Purple
    (0xC6, 0x59, 0x11),  # Dark Orange
]

# Genre Styling Presets
GENRE_PRESETS = {
    'dialogue': {
        'title': 'Диалоги и устная речь',
        'font_name': 'Calibri',
        'font_size_pt': 11,
        'line_spacing': 1.15,
        'space_before_pt': 2,
        'space_after_pt': 5,
        'show_metadata': True
    },
    'prose': {
        'title': 'Художественная и научная проза',
        'font_name': 'Times New Roman',
        'font_size_pt': 12,
        'line_spacing': 1.25,
        'space_before_pt': 0,
        'space_after_pt': 6,
        'first_line_indent_pt': 18,
        'show_metadata': False
    },
    'poetry': {
        'title': 'Поэзия и стихотворения',
        'font_name': 'Georgia',
        'font_size_pt': 11.5,
        'line_spacing': 1.15,
        'space_before_pt': 0,
        'space_after_pt': 2,
        'stanza_space_after_pt': 12,
        'left_indent_pt': 36,
        'show_metadata': False
    },
    'drama': {
        'title': 'Драматургия и пьесы',
        'font_name': 'Arial',
        'font_size_pt': 11,
        'line_spacing': 1.2,
        'space_before_pt': 4,
        'space_after_pt': 4,
        'character_name_bold': True,
        'stage_direction_italic': True,
        'show_metadata': False
    },
    'academic': {
        'title': 'Статьи и академические работы',
        'font_name': 'Times New Roman',
        'font_size_pt': 12,
        'line_spacing': 1.5,
        'space_before_pt': 3,
        'space_after_pt': 6,
        'show_metadata': False
    }
}
