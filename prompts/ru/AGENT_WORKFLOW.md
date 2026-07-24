# Сценарий работы ИИ-агента (универсальный)

Старт для пользователя: [`START_USER_PROMPT.md`](START_USER_PROMPT.md)  
Системный промпт: [`UNIVERSAL_EDITOR_SYSTEM.md`](UNIVERSAL_EDITOR_SYSTEM.md)

---

## Фаза 0 — Ориентация

1. Корень проекта: `AGENTS.md`, `inputs/`, `output/`.
2. Краткая справка из `docs/ru/HOW_TO_WORK.md`.
3. Список файлов в `inputs/raw_texts/` **и** `inputs/audio/`.
4. **Если есть только аудио** (`.mp3`, `.ogg`, `.wav`, папка `inputs/audio/`):
   - Vox2Book вычитывает **текст**, не слушает аудио.
   - Предложи STT: встроенный `tools/transcribe_audio.py` **или** OpenAI API, AssemblyAI, Deepgram, экспорт Telegram, Descript, MacWhisper, GigaAM… (`docs/ru/AUDIO_TRANSCRIPTION.md`).
   - После транскрипта — продолжай с `inputs/raw_texts/`.
5. Тип текста → профиль при необходимости:
   - речь → `profiles/SPEECH_TO_TEXT.md`
   - диалог → `profiles/DIALOGUE_TRANSCRIPT.md`
   - статья → `profiles/ACADEMIC_ESSAY.md`

---

## Фаза 1 — Чтение источника

1. Открыть указанный файл.
2. Кодировка: UTF-8 → cp1251.
3. Заметить: жанр, регистр, спикеры, битый STT, объём.

---

## Фаза 2 — Уточняющие вопросы

Если пользователь не сказал «делай сразу»:

1. Режим стиля: литературный / живой / академический / лёгкий?
2. Заголовок, подзаголовок, сохранять метки времени/спикеров?
3. Есть `config/glossary_user.json`?
4. Сохранять мат и сленг?
5. Один файл или вся папка?
6. Список 2–5 неясных мест STT/OCR.

---

## Фаза 3 — Обработка

1. Гигиена источника  
2. Литературная пересборка  
3. Профиль (если нужен)  
4. Типографика  
5. 8 аудитов (`docs/ru/TECHNICAL_SPECIFICATION.md`) + `check_cuts`  
6. DOCX → `output/books/`

Кэш: `output/.llm_cache/*.edited.txt`, `*.audit.md`

---

## Фаза 4 — Отчёт

Путь к DOCX, что исправлено, открытые вопросы.

---

## Язык общения

Русский (эта папка `prompts/ru/`).
