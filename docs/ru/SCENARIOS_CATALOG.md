# Каталог сценариев Vox2Book

> **Цель:** модуль `tools/auto_detect.py` + этот каталог покрывают сотни реальных ситуаций.
> Программа сама определяет жанр, стиль и нужные действия — пользователь даёт **одну фразу**.
>
> Каталог организован как матрица: **Жанр × Признаки → План действий**.
> Каждая строка — обобщённый сценарий (без привязки к конкретному тексту).

---

## Как пользоваться

1. Пользователь пишет одну фразу (см. `prompts/ru/START_USER_PROMPT.md`).
2. Программа читает файл, запускает `auto_detect.analyze(text)`.
3. По жанру и признакам из каталога ниже формируется план.
4. План выполняется автоматически (или уточняется у пользователя).

---

## Матрица жанров (7 базовых)

| ID жанра | Описание | Профиль | Режим стиля |
|----------|----------|---------|-------------|
| `prose` | Проза, рассказ, мемуары | none | literary |
| `dialogue` | Диалог, чат, переписка | dialogue | literary_lively |
| `stt` | Расшифровка речи (Whisper/диктовка) | speech_to_text | literary_lively |
| `poetry` | Поэзия, стихи | none | literary |
| `academic` | Статья, диссертация, реферат | academic | academic |
| `article` | Блог-пост, статья, лонгрид | none | light |
| `code` | Код, технический текст | none | — (не редактируется как проза) |

---

## Сценарии по жанрам (детализация признаков → действий)

### prose — Проза

| # | Признаки в тексте | Доп. действия | Флаги |
|---|-------------------|---------------|-------|
| 1 | Главы, абзацы, прямая речь автора | rebuild, punctuate | — |
| 2 | «Глава N», «Эпилог», «Пролог» | rebuild, punctuate, keep_structure | — |
| 3 | Мемуары, много «я», хронология | rebuild, punctuate, keep_timeline | — |
| 4 | Короткий рассказ (< 3000 слов) | punctuate, typography | — |
| 5 | Роман/повесть (> 3000 слов) | rebuild, punctuate, split_chapters | — |
| 6 | Проза с матом | rebuild, punctuate, keep_mat=True | keep_mat |
| 7 | Проза с диалогами героев (не чат!) | rebuild, punctuate, format_dialogue | — |
| 8 | Сказка/детская проза | rebuild, punctuate, simplify_register | — |
| 9 | Фантастика/фэнтези, термины мира | rebuild, punctuate, check_terms | — |
| 10 | Историческая проза, даты/имена | rebuild, punctuate, check_facts | — |
| 11 | Эпистолярный жанр (письма) | rebuild, punctuate, format_letters | — |
| 12 | Проза с примесью STT (надиктовано) | fix_stt, rebuild, punctuate | — |
| 13 | Проза с OCR-ошибками (скан) | fix_ocr, rebuild, punctuate | — |
| 14 | Дневник/записи | rebuild, punctuate, keep_dates | — |
| 15 | Проза с цитатами на других языках | rebuild, punctuate, keep_quotes | — |

### dialogue — Диалог / чат

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 16 | Метки спикеров + время | colors, keep_speakers, keep_timestamps | keep_speakers, keep_timestamps |
| 17 | Только имена, без времени | colors, keep_speakers | keep_speakers |
| 18 | [Голосовое]/[Текст] смешанные | fix_stt, rebuild, fix_terminal | keep_speakers |
| 19 | Пересылки новостей/ссылок | keep_links, fix_terminal | — |
| 20 | Мат в голосовых | keep_mat=True | keep_mat |
| 21 | > 2 спикеров | colors, multi_speaker_palette | keep_speakers |
| 22 | Деловая переписка (без мата) | rebuild, punctuate, formal_register | keep_mat=False |
| 23 | Семейный чат | rebuild, punctuate, keep_mat | keep_mat |
| 24 | Технический чат (IT) | restore_brands, fix_stt, keep_jargon | — |
| 25 | Чат с эмодзи | keep_emoji, fix_terminal | — |
| 26 | Чат с аудио-сообщениями (STT) | fix_stt, remove_garbage, fix_repetitions | — |
| 27 | Форум/комментарии | rebuild, punctuate, keep_threads | — |
| 28 | Интервью (вопрос-ответ) | rebuild, punctuate, format_qa | — |
| 29 | Допрос/протокол | rebuild, punctuate, formal_register | — |
| 30 | Групповой чат с упоминаниями @ | keep_mentions, colors | keep_speakers |

### stt — Расшифровка речи

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 31 | Длинные строки без пунктуации | rebuild, punctuate | — |
| 32 | Галлюцинации Whisper | remove_garbage | — |
| 33 | Дублирования слов | fix_repetitions | — |
| 34 | Искажённые бренды | restore_brands | — |
| 35 | Слова-призраки | fix_stt, mark_unknown | — |
| 36 | Омофоны | fix_stt (contextual) | — |
| 37 | IT code-switching | restore_brands, keep_jargon | — |
| 38 | Один спикер (монолог) | rebuild, punctuate | — |
| 39 | Несколько спикеров | colors, keep_speakers | keep_speakers |
| 40 | Речь с матом | keep_mat=True | keep_mat |
| 41 | Лекция/выступление | rebuild, punctuate, academic_register | — |
| 42 | Подкаст | rebuild, punctuate, keep_speakers | keep_speakers |
| 43 | Диктовка голосовых сообщений | fix_stt, rebuild, punctuate | — |
| 44 | Аудиодневник | rebuild, punctuate, keep_dates | — |
| 45 | Стенограмма заседания | rebuild, punctuate, formal_register | — |
| 46 | Речь с акцентом/диалектом | rebuild, punctuate, keep_dialect | — |
| 47 | Детская речь | rebuild, punctuate, simplify_register | — |
| 48 | Речь пожилого человека | rebuild, punctuate, keep_register | — |
| 49 | Речь с паузами-словами («э-э») | reduce_fillers, keep_tone | — |
| 50 | Речь с повторами для акцента | fix_repetitions, keep_emphasis | — |

### poetry — Поэзия

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 51 | Короткие строки, строфы | punctuate (minimal) | — |
| 52 | Стихи с рифмой | keep_rhythm, punctuate | — |
| 53 | Верлибр (свободный стих) | punctuate, keep_structure | — |
| 54 | Песенные тексты | keep_rhythm, punctuate, keep_chorus | — |
| 55 | Хайку/танка | keep_structure, punctuate | — |
| 56 | Эпическая поэма | rebuild, punctuate, keep_stanzas | — |
| 57 | Стихи с матом | keep_mat=True | keep_mat |
| 58 | Детские стихи | punctuate, simplify_register | — |
| 59 | Стихи надиктованы (STT) | fix_stt, keep_rhythm | — |
| 60 | Стихи с OCR-ошибками | fix_ocr, keep_rhythm | — |

### academic — Академический текст

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 61 | Реферат/курсовая | rebuild, punctuate, check_terms | — |
| 62 | Диссертация | rebuild, punctuate, check_terms, check_facts | — |
| 63 | Статья с DOI/ссылками | keep_references, check_terms | — |
| 64 | Аннотация/введение/заключение | rebuild, punctuate, keep_structure | — |
| 65 | Список литературы | keep_references, format_bibliography | — |
| 66 | Формулы/нотации | keep_formulas, check_terms | — |
| 67 | Таблицы/графики (описания) | keep_tables, punctuate | — |
| 68 | Научный английский (RU+EN) | keep_terms, punctuate | — |
| 69 | Сноски/примечания | keep_footnotes, punctuate | — |
| 70 | Тезисы конференции | rebuild, punctuate, check_terms | — |

### article — Статья / блог

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 71 | Markdown-заголовки # | keep_structure, punctuate | — |
| 72 | Блог-пост с призывами | punctuate, keep_cta | — |
| 73 | Лонгрид с подзаголовками | rebuild, punctuate, keep_structure | — |
| 74 | SEO-статья с ключами | punctuate, keep_keywords | — |
| 75 | Новостная статья | punctuate, formal_register | — |
| 76 | Обзор/рецензия | rebuild, punctuate | — |
| 77 | Инструкция/how-to | keep_steps, punctuate | — |
| 78 | Колонка/мнение | rebuild, punctuate, keep_voice | — |
| 79 | Интервью-статья | rebuild, punctuate, format_qa | — |
| 80 | Репортаж | rebuild, punctuate, keep_quotes | — |

### code — Код / технический текст

| # | Признаки | Доп. действия | Флаги |
|---|----------|---------------|-------|
| 81 | Исходный код | skip (не редактировать) | — |
| 82 | README/документация кода | punctuate, keep_code_blocks | — |
| 83 | Комментарии в коде | punctuate_comments | — |
| 84 | Техническая спецификация | rebuild, punctuate, check_terms | — |
| 85 | Changelog/release notes | keep_structure, punctuate | — |

---

## Смешанные / краевые сценарии

| # | Ситуация | Жанр | Действия |
|---|----------|------|----------|
| 86 | Проза + надиктовано | prose + stt | fix_stt, rebuild, punctuate |
| 87 | Диалог + STT | dialogue + stt | fix_stt, colors, fix_terminal |
| 88 | Статья + STT | article + stt | fix_stt, punctuate, keep_structure |
| 89 | Поэзия + STT | poetry + stt | fix_stt, keep_rhythm |
| 90 | Академический + STT | academic + stt | fix_stt, rebuild, check_terms |
| 91 | Дневник + OCR | prose + ocr | fix_ocr, rebuild, punctuate |
| 92 | Чат + аудио + текст + ссылки | dialogue + stt | fix_stt, keep_links, colors, fix_terminal |
| 93 | Письма + стихи внутри | prose + poetry | split, prose→rebuild, poetry→keep_rhythm |
| 94 | Мемуары + фотографии-описания | prose | rebuild, punctuate, keep_captions |
| 95 | Стенограмма + список присутствующих | stt + academic | rebuild, punctuate, formal_register |
| 96 | Рецепт (список шагов) | article | keep_steps, punctuate |
| 97 | Проповедь/речь | stt | rebuild, punctuate, keep_register |
| 98 | Аудиокнига (надиктованная) | stt + prose | fix_stt, rebuild, punctuate |
| 99 | Театральная пьеса | prose | rebuild, punctuate, format_stage |
| 100 | Сценарий (кино/видео) | prose | rebuild, punctuate, format_screenplay |

---

## Фразы пользователя → ожидаемое поведение

> Пользователь даёт **одну** фразу. Программа определяет жанр по **тексту**, а не по фразе.
> Фраза может лишь подсказать приоритет или ограничение.

| Фраза пользователя | Что программа делает |
|--------------------|---------------------|
| «Вычитай» | Полный авто-анализ + все действия по жанру |
| «Сделай книгу» | Авто-анализ + docx + (colors если диалог) |
| «Только пунктуацию» | Авто-анализ → только punctuate + typography |
| «Убери мусор» | Авто-анализ → cleanup + remove_garbage + fix_repetitions |
| «Не трогай мат» | keep_mat=True принудительно |
| «Убери мат» | keep_mat=False принудительно |
| «Сохрани стиль автора» | style_mode=literary_lively, минимум rebuild |
| «Академический стиль» | style_mode=academic принудительно |
| «Разбей на главы» | split_chapters (если > 3000 слов) |
| «Сделай красиво» | Все действия + typography + docx |
| «Быстро» | Только cleanup + punctuate + typography |
| «Глубоко» | Все действия + полный аудит |
| «Переведи в книгу» | Авто-анализ + docx + цвета (если диалог) |
| «Вычитай и оформи» | Все действия + docx |
| «Только опечатки» | cleanup + fix_stt (контекстно) |
| «Сделай читаемым» | rebuild + punctuate (для STT) |
| «Не меняй слова» | Только punctuate + typography |
| «Восстанови бренды» | restore_brands |
| «Убери повторы» | fix_repetitions |
| «Проверь обрывы» | fix_terminal + check_cuts |

---

## Действия (справочник)

| Действие | Описание | Связанный аудит |
|----------|----------|-----------------|
| `cleanup` | Удаление артефактов, нормализация пробелов/кодировки | 1, 5 |
| `rebuild` | Литературная пересборка сплошного потока в предложения/абзацы | 3 |
| `punctuate` | Восстановление пунктуации | 2 |
| `fix_stt` | Контекстная правка STT-ошибок (омофоны, слова-призраки) | 1, 6 |
| `remove_garbage` | Удаление машинного мусора (служебные пометки, галлюцинации) | 1, 8 |
| `fix_repetitions` | Сведение дублирований слов («я я» → «я») | 6 |
| `restore_brands` | Восстановление брендов/программ по контексту | 4 |
| `fix_terminal` | Добавление терминальных знаков | 7 |
| `fix_ocr` | Правка OCR-ошибок (перестановки букв, е/ё) | 1 |
| `typography` | Типографика (кавычки, тире, частицы) | 2 |
| `check_terms` | Проверка единообразия терминов | 4 |
| `check_facts` | Проверка дат/имён (без выдумывания) | 4 |
| `audit` | 8 аудитов + check_cuts + check_terminal + check_repetitions + check_stt_artifacts | 1–8 |
| `docx` | Компиляция в .docx | — |
| `colors` | Цветовая разметка имён спикеров | 8 |
| `keep_links` | Сохранение ссылок как есть | 4 |
| `keep_emoji` | Сохранение эмодзи | 4 |
| `keep_structure` | Сохранение заголовков/разделов | 7 |
| `split_chapters` | Разбивка на главы (по указанию) | 7 |
| `format_dialogue` | Оформление прямой речи (тире/кавычки) | 2 |
| `format_qa` | Оформление вопрос-ответ | 2 |
| `format_letters` | Оформление писем | 2 |
| `format_bibliography` | Оформление списка литературы | 4 |
| `keep_references` | Сохранение ссылок/DOI | 4 |
| `keep_footnotes` | Сохранение сносок | 4 |
| `keep_formulas` | Сохранение формул | 4 |
| `keep_tables` | Сохранение таблиц | 4 |
| `keep_mentions` | Сохранение @упоминаний | 4 |
| `keep_dates` | Сохранение дат/хронологии | 4 |
| `keep_quotes` | Сохранение цитат на др. языках | 4 |
| `keep_captions` | Сохранение подписей к фото | 4 |
| `keep_threads` | Сохранение веток форума | 7 |
| `keep_code_blocks` | Сохранение блоков кода | 4 |
| `keep_rhythm` | Сохранение ритма (поэзия) | 7 |
| `keep_stanzas` | Сохранение строф | 7 |
| `keep_chorus` | Сохранение припевов | 7 |
| `keep_cta` | Сохранение призывов (CTA) | 4 |
| `keep_keywords` | Сохранение SEO-ключей | 4 |
| `keep_steps` | Сохранение шагов/нумерации | 7 |
| `keep_voice` | Сохранение голоса автора | 5 |
| `keep_dialect` | Сохранение диалекта | 5 |
| `keep_register` | Сохранение регистра речи | 5 |
| `keep_jargon` | Сохранение жаргона | 5 |
| `keep_emphasis` | Сохранение эмфазы (акценты) | 5 |
| `reduce_fillers` | Умеренное убирание паразитов | 5 |
| `simplify_register` | Упрощение регистра (детское) | 5 |
| `formal_register` | Формальный регистр | 5 |
| `academic_register` | Академический регистр | 5 |
| `multi_speaker_palette` | Палитра для >2 спикеров | 8 |
| `mark_unknown` | Пометка `[?]` нерешённых мест | 8 |
| `format_stage` | Оформление пьесы (ремарки) | 2 |
| `format_screenplay` | Оформление сценария | 2 |
| `keep_mat` | Флаг: сохранять мат | 5 |
| `keep_speakers` | Флаг: сохранять имена спикеров | 8 |
| `keep_timestamps` | Флаг: сохранять время | 8 |

---

## Алгоритм выбора сценария

```
1. auto_detect.analyze(text) → genre, signals
2. Найти базовый жанр в матрице (7 базовых)
3. Найти уточняющий сценарий в таблице жанра (по признакам)
4. Применить фразы-модификаторы пользователя (keep_mat, style и т.д.)
5. Собрать итоговый список действий (с дедупликацией и порядком)
6. Выполнить по порядку: cleanup → fix_stt → remove_garbage → fix_repetitions
   → restore_brands → rebuild → punctuate → fix_terminal → typography
   → audit → colors → docx
```

---

## Расширение каталога

Каталог **открыт для расширения**. Чтобы добавить сценарий:
1. Опиши признаки (регулярки/эвристики) в `tools/auto_detect.py` → `_signals()`.
2. Добавь строку в таблицу жанра в этом файле.
3. При необходимости — новое действие в справочник выше.

Программа не требует жёсткого списка — `auto_detect.py` работает по весам сигналов,
поэтому новые жанры/признаки добавляются без переработки архитектуры.