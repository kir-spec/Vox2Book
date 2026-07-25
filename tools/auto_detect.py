# -*- coding: utf-8 -*-
"""
Vox2Book — Авто-определение жанра, стиля и действий по тексту.

Модуль анализирует сырой текст и возвращает структуру решения:
  - genre          — жанр (prose/dialogue/stt/academic/article/poetry/code/mixed)
  - style_mode     — режим стиля (literary/literary_lively/academic/light)
  - profile        — профиль промпта (none/speech_to_text/dialogue/academic)
  - actions        — список действий (cleanup/rebuild/punctuate/typography/audit/docx/colors)
  - keep_speakers  — сохранять метки спикеров
  - keep_timestamps— сохранять метки времени
  - keep_mat       — сохранять мат (по умолчанию True для речи/диалогов)
  - language       — ru/en/uk
  - confidence     — уверенность (0..1)
  - reasons        — список сработавших правил (для отчёта)

Не использует внешних API — чистая эвристика + регулярки.
"""

import re
from typing import Dict, List, Any


# =====================================================================
# ПРИЗНАКИ ЖАНРОВ (весовые сигналы)
# =====================================================================

def _signals(text: str) -> Dict[str, int]:
    """Возвращает словарь сигнал→балл на основе эвристик."""
    s: Dict[str, int] = {}
    t = text
    low = t.lower()
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    n_lines = max(1, len(lines))
    n_chars = max(1, len(t))

    # --- Диалог / чат -------------------------------------------------
    speaker_marks = len(re.findall(r'^(Анфи|Kir|\w+)\s*\[\d{1,2}:\d{2}\]\s*\[', t, re.M))
    if speaker_marks >= 3:
        s['dialogue'] = speaker_marks * 3
    # Метки спикеров в стиле тире:  — Анфи: ... / Kir: ...
    dash_speakers = len(re.findall(r'^[—\-]\s*\*?\s*[А-ЯЁA-Z][\wё]{2,}\s*:', t, re.M))
    if dash_speakers >= 3:
        s['dialogue'] = s.get('dialogue', 0) + dash_speakers * 2
    # Типичные слова меток
    if re.search(r'\[Голосовое\]|\[Текст\]|\[Аудио\]', t):
        s['dialogue'] = s.get('dialogue', 0) + 30
    # Пересылки/ссылки новостей
    if low.count('https://') >= 3 or low.count('http') >= 5:
        s['dialogue'] = s.get('dialogue', 0) + 10

    # --- STT / речь ---------------------------------------------------
    # Длинные строки без пунктуации
    no_punct_long = 0
    for ln in lines:
        if len(ln) > 120:
            punct = sum(1 for ch in ln if ch in '.,!?;:—')
            if punct < max(1, len(ln) / 80):
                no_punct_long += 1
    if no_punct_long >= 2:
        s['stt'] = no_punct_long * 4
    # Слова-паразиты устной речи
    parasites = len(re.findall(r'\b(ну|типа|короче|вот|блин|значит|прикольно|охренеть|капец|хз|чё|ща|щас)\b', low))
    if parasites >= 5:
        s['stt'] = s.get('stt', 0) + parasites
    # Галлюцинации Whisper
    if re.search(r'субтитры сделал|подписывайтесь на канал|продолжение следует|отправить\. отправить', low):
        s['stt'] = s.get('stt', 0) + 40
    # Заикания/дублирования
    dups = len(re.findall(r'\b(я|не|ну|короче|вот|да|там)\s+\1\b', low))
    if dups >= 3:
        s['stt'] = s.get('stt', 0) + dups * 3
    # Кириллическая «фонетика» брендов
    if re.search(r'\b(протуз|риппер|кубейс|кафка|телега|винда|блютуз|вайфай)\b', low):
        s['stt'] = s.get('stt', 0) + 15

    # --- Проза / рассказ ---------------------------------------------
    # Абзацы с красной строкой / отступами
    paragraphs = [p for p in re.split(r'\n\s*\n', t) if p.strip()]
    if len(paragraphs) >= 3:
        s['prose'] = min(20, len(paragraphs) * 2)
    # Прямая речь автора
    if re.search(r'— [А-ЯЁ]', t) and not speaker_marks:
        s['prose'] = s.get('prose', 0) + 8
    # Литературные маркеры
    if re.search(r'\b(глава|эпилог|пролог|часть первая|часть \d)\b', low):
        s['prose'] = s.get('prose', 0) + 15
    # Описания, прилагательные
    adj_density = len(re.findall(r'\b(ая|ое|ие|ые|ий|ый)\b', low)) / n_chars
    if adj_density > 0.02 and not speaker_marks:
        s['prose'] = s.get('prose', 0) + 10

    # --- Поэзия -------------------------------------------------------
    short_lines = sum(1 for ln in lines if 0 < len(ln) <= 60)
    if n_lines >= 4 and short_lines / n_lines > 0.7:
        # Рифма/ритм: строки похожей длины
        lens = [len(ln) for ln in lines if ln]
        if lens:
            avg = sum(lens) / len(lens)
            var = sum(abs(x - avg) for x in lens) / len(lens)
            if var < 12 and avg < 50:
                s['poetry'] = 25
    # Строфы (пустые строки между группами)
    if t.count('\n\n') >= 2 and short_lines / n_lines > 0.6:
        s['poetry'] = s.get('poetry', 0) + 10

    # --- Академическая статья ----------------------------------------
    if re.search(r'\b(реферат|диссертация|аннотация|ключевые слова|введение|заключение|список литературы|bibliography|references)\b', low):
        s['academic'] = 30
    if re.search(r'\[\d+\]|\(\d{4},\s*p\.|\bdoi:\b', low):
        s['academic'] = s.get('academic', 0) + 20
    # Сноски
    if re.search(r'\*\*|\^\^|сниск\.\s*\d|сноска', low):
        s['academic'] = s.get('academic', 0) + 10
    # Формальный регистр: мало «я», много пассива
    passive = len(re.findall(r'\b(является|представляет|заключается|осуществляется|используется)\b', low))
    if passive >= 3 and parasites < 3:
        s['academic'] = s.get('academic', 0) + passive * 2

    # --- Статья / блог ------------------------------------------------
    if re.search(r'^#{1,6}\s', t, re.M) and not speaker_marks:
        s['article'] = len(re.findall(r'^#{1,6}\s', t, re.M)) * 5
    if re.search(r'\b(читайте|подписывайтесь|лайк|комментарий|делитесь)\b', low) and not s.get('academic'):
        s['article'] = s.get('article', 0) + 8

    # --- Код / технический текст --------------------------------------
    if re.search(r'^\s*(def |class |import |from |func |func |public |private |#include)', t, re.M):
        s['code'] = 30
    if low.count('```') >= 2:
        s['code'] = s.get('code', 0) + 20
    if re.search(r'\b(function|return|null|true|false|const|let|var)\b', low) and low.count('{') >= 5:
        s['code'] = s.get('code', 0) + 15

    return s


# =====================================================================
# ОПРЕДЕЛЕНИЕ ЖАНРА
# =====================================================================

GENRE_MAP = {
    'dialogue': ('dialogue', 'dialogue'),
    'stt':      ('stt', 'speech_to_text'),
    'prose':    ('prose', 'none'),
    'poetry':   ('poetry', 'none'),
    'academic': ('academic', 'academic'),
    'article':  ('article', 'none'),
    'code':     ('code', 'none'),
}


def detect_genre(text: str) -> tuple:
    """Возвращает (genre, profile, confidence, reasons)."""
    signals = _signals(text)
    if not signals:
        return ('prose', 'none', 0.3, ['no strong signals — default prose'])

    ranked = sorted(signals.items(), key=lambda x: -x[1])
    top_genre, top_score = ranked[0]
    total = sum(signals.values())
    confidence = round(min(0.99, top_score / max(1, total) * 1.2), 2)

    genre, profile = GENRE_MAP.get(top_genre, ('prose', 'none'))
    reasons = [f'{k}: {v}' for k, v in ranked[:4]]
    return (genre, profile, confidence, reasons)


# =====================================================================
# ОПРЕДЕЛЕНИЕ РЕЖИМА СТИЛЯ
# =====================================================================

def detect_style_mode(genre: str, text: str) -> str:
    """Возвращает режим стиля."""
    low = text.lower()
    if genre == 'academic':
        return 'academic'
    if genre in ('stt', 'dialogue'):
        # Мат/жаргон → живой режим
        if re.search(r'\b(бля|хуё|хуе|пиздец|нахуй|нахрен|охренеть|капец|херня)\b', low):
            return 'literary_lively'
        return 'literary_lively'
    if genre == 'poetry':
        return 'literary'
    if genre == 'article':
        return 'light'
    return 'literary'


# =====================================================================
# ОПРЕДЕЛЕНИЕ ДЕЙСТВИЙ
# =====================================================================

def detect_actions(genre: str, text: str) -> List[str]:
    """Возвращает упорядоченный список действий."""
    actions = ['cleanup']  # всегда
    low = text.lower()

    if genre in ('stt', 'dialogue'):
        actions += ['rebuild', 'punctuate', 'fix_stt', 'remove_garbage', 'fix_repetitions',
                    'restore_brands', 'fix_terminal']
    elif genre == 'prose':
        actions += ['rebuild', 'punctuate']
    elif genre == 'poetry':
        actions += ['punctuate']  # минимально, не ломать ритм
    elif genre == 'academic':
        actions += ['rebuild', 'punctuate', 'check_terms']
    elif genre == 'article':
        actions += ['punctuate', 'typography']
    elif genre == 'code':
        actions = []  # код не редактируем как прозу

    actions += ['typography', 'audit', 'docx']

    # Цвета имён — только для диалогов
    if genre == 'dialogue':
        actions += ['colors']

    # Дедупликация с сохранением порядка
    seen = set()
    out = []
    for a in actions:
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


# =====================================================================
# ФЛАГИ СОХРАНЕНИЯ
# =====================================================================

def detect_keep_flags(genre: str, text: str) -> Dict[str, bool]:
    """Флаги: сохранять ли метки спикеров/время/мат."""
    has_speakers = bool(re.search(r'^\w+\s*\[\d{1,2}:\d{2}\]\s*\[', text, re.M))
    has_timestamps = bool(re.search(r'\[\d{1,2}:\d{2}\]', text))
    low = text.lower()
    has_mat = bool(re.search(r'\b(бля|хуё|хуе|пиздец|нахуй|нахрен|ебёт|ебан|ёбнут|блядь)\b', low))

    return {
        'keep_speakers': has_speakers,
        'keep_timestamps': has_timestamps,
        'keep_mat': has_mat or genre in ('stt', 'dialogue'),
    }


# =====================================================================
# ОПРЕДЕЛЕНИЕ ЯЗЫКА
# =====================================================================

def detect_language(text: str) -> str:
    """Простая эвристика ru/en/uk."""
    ru = len(re.findall(r'[а-яё]', text.lower()))
    uk_specific = len(re.findall(r'\b(і|ї|є|ґ)\b', text.lower()))
    en = len(re.findall(r'[a-z]', text.lower()))
    if uk_specific >= 3 and uk_specific > en * 0.1:
        return 'uk'
    if ru > en:
        return 'ru'
    if en > ru:
        return 'en'
    return 'ru'


# =====================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# =====================================================================

def analyze(text: str) -> Dict[str, Any]:
    """Полный анализ текста → план действий."""
    genre, profile, confidence, reasons = detect_genre(text)
    style_mode = detect_style_mode(genre, text)
    actions = detect_actions(genre, text)
    flags = detect_keep_flags(genre, text)
    language = detect_language(text)

    return {
        'genre': genre,
        'profile': profile,
        'style_mode': style_mode,
        'actions': actions,
        'language': language,
        'confidence': confidence,
        'reasons': reasons,
        'keep_speakers': flags['keep_speakers'],
        'keep_timestamps': flags['keep_timestamps'],
        'keep_mat': flags['keep_mat'],
    }


# =====================================================================
# CLI
# =====================================================================

if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print('Usage: python auto_detect.py <file.txt>')
        print('       python auto_detect.py --text "..."')
        sys.exit(1)

    if sys.argv[1] == '--text':
        text = ' '.join(sys.argv[2:])
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()

    result = analyze(text)
    print(json.dumps(result, indent=2, ensure_ascii=False))