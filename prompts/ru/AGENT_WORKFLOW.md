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

## Фаза 1.5 — Авто-определение (ОБЯЗАТЕЛЬНО)

> Программа **сама** определяет жанр, стиль и план действий по тексту.
> Пользователю не нужно указывать жанр/профиль/стиль вручную.

1. Запустить `tools/auto_detect.py` (или `pipeline.py` → `auto_detect_plan()`).
2. Результат — план: жанр, профиль, стиль, действия, флаги (keep_speakers, keep_mat и т.д.).
3. План сохраняется в `output/.llm_cache/auto_plan.json`.
4. Если уверенность < 0.5 — показать план пользователю и уточнить.
5. Если уверенность >= 0.5 — продолжить автоматически (по AGENTS.md пользователь дал одну фразу).
6. Каталог сценариев: `docs/ru/SCENARIOS_CATALOG.md` (100+ сценариев, 7 жанров, 50+ действий).

### Что определяется автоматически:
- **Жанр**: prose / dialogue / stt / poetry / academic / article / code
- **Профиль промпта**: speech_to_text / dialogue / academic / none
- **Режим стиля**: literary / literary_lively / academic / light
- **Действия**: cleanup, rebuild, punctuate, fix_stt, remove_garbage, fix_repetitions, restore_brands, fix_terminal, typography, audit, docx, colors
   - **Флаги**: keep_speakers, keep_timestamps, **keep_mat=True по умолчанию** для dialogue/stt

---

## Фаза 2 — Уточняющие вопросы

> По умолчанию (при фразе «Вычитай») — **не задавать**, программа всё определила сама.

Если пользователь не сказал «делай сразу»:

1. Режим стиля: литературный / живой / академический / лёгкий?
2. Заголовок, подзаголовок, сохранять метки времени/спикеров?
3. Есть `config/glossary_user.json`?
4. Сохранять мат и сленг? **По умолчанию — да** (`keep_mat=True`); цензура только по явной команде.
5. Один файл или вся папка?
6. Список 2–5 неясных мест STT/OCR.

---

## Фаза 3 — Обработка

1. Гигиена источника  
   - Удалить машинный мусор (служебные пометки STT/OCR, галлюцинации, дублирующие строки)
   - Свести дублирования слов («я я» → «я»), кроме осмысленных авторских повторов
   - Нормализовать пробелы и кодировку
2. Литературная пересборка  
   - Разбить поток на предложения/абзацы; восстановить синтаксис
   - Восстановить бренды/программы по контексту (сохраняя разговорные названия, если это стиль речи)
   - Исправить STT-ошибки **только по контексту** (±10 реплик); см. [`glossary/STT_PROCESSING_ALGORITHMS.ru.md`](../glossary/STT_PROCESSING_ALGORITHMS.ru.md) — **не** использовать comma-splice regex
3. Профиль (если нужен)  
4. Типографика  
5. **Фаза 3.5 — Контекстный аудит** (для диалогов / крупных STT-правок):
   - Сравнить с исходником (`.bak_*`, `inputs/`) на массовые регрессии (`. Но` → `, но`).
   - Отчёт: `output/.llm_cache/*.audit.md` или `tools/context_audit_report.md`.
   - Эталон консервативной пересборки: `tools/contextual_rebuild_*.py`; аудит: `tools/context_audit_*.py`.
   - Универсальное ТЗ: [`glossary/UNIVERSAL_EDITORIAL_SPEC.ru.md`](../glossary/UNIVERSAL_EDITORIAL_SPEC.ru.md).
6. 8 аудитов (`docs/ru/TECHNICAL_SPECIFICATION.md`) + `check_cuts` + `check_terminal` + `check_repetitions` + `check_stt_artifacts`  
   - **check_terminal**: терминальный знак в каждом сообщении (включая заголовки, ссылки, короткие реплики)
   - **check_repetitions**: нет дублирований одного слова подряд
   - **check_stt_artifacts**: нет остаточного машинного мусора, comma-splice регрессии (`. Но` → `, но`)
7. DOCX → путь по умолчанию `output/books/` **или путь, указанный заказчиком** (без дубликатов)
   - Режим **prepress_book**: убрать `Спикер [ЧЧ:ММ] [Голосовое]:`, формат `— реплика. — Спикер.` — см. `profiles/DIALOGUE_TRANSCRIPT.md`

Кэш: `output/.llm_cache/*.edited.txt`, `*.audit.md`

---

## Фаза 4 — Отчёт

Путь к DOCX, что исправлено, открытые вопросы.

---

## Язык общения

Русский (эта папка `prompts/ru/`).
