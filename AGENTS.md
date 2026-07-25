# AGENTS.md — для любой нейросети

**Vox2Book** — литературная вычитка любых текстов → `output/books/*.docx`

---

## Выберите язык инструкций

| Язык | Промпты | Документация |
|------|---------|--------------|
| 🇷🇺 Русский | [`prompts/ru/`](prompts/ru/) | [`docs/ru/`](docs/ru/) |
| 🇬🇧 English | [`prompts/en/`](prompts/en/) | [`docs/en/`](docs/en/) |
| 🇺🇦 Українська | [`prompts/uk/`](prompts/uk/) | [`docs/uk/`](docs/uk/) |

**Старт для пользователя:** `prompts/<язык>/START_USER_PROMPT.md`  
**Главный промпт редактора:** `prompts/<язык>/UNIVERSAL_EDITOR_SYSTEM.md`  
**Сценарий агента:** `prompts/<язык>/AGENT_WORKFLOW.md`  
**8 аудитов:** `docs/<язык>/TECHNICAL_SPECIFICATION.md`

Общий глоссарий (не переводится): `config/glossary_user.json`, `prompts/glossary/`

**Контекстная правка STT/OCR (обязательно для ИИ):**

| Язык | Руководство | Таблица STT |
|------|-------------|-------------|
| RU | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md`](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) | [`STT_HOMOPHONES.ru.md`](prompts/glossary/STT_HOMOPHONES.ru.md) |
| EN | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) | [`STT_HOMOPHONES.en.md`](prompts/glossary/STT_HOMOPHONES.en.md) |
| UK | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md`](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) | [`STT_HOMOPHONES.uk.md`](prompts/glossary/STT_HOMOPHONES.uk.md) |

**Канон алгоритмов STT (regex, comma splices, pre-press, keep_mat):**

| Язык | Алгоритмы | Универсальное ТЗ |
|------|-----------|------------------|
| RU | [`STT_PROCESSING_ALGORITHMS.ru.md`](prompts/glossary/STT_PROCESSING_ALGORITHMS.ru.md) | [`UNIVERSAL_EDITORIAL_SPEC.ru.md`](prompts/glossary/UNIVERSAL_EDITORIAL_SPEC.ru.md) |
| EN | [`STT_PROCESSING_ALGORITHMS.en.md`](prompts/glossary/STT_PROCESSING_ALGORITHMS.en.md) | [`UNIVERSAL_EDITORIAL_SPEC.en.md`](prompts/glossary/UNIVERSAL_EDITORIAL_SPEC.en.md) |
| UK | [`STT_PROCESSING_ALGORITHMS.uk.md`](prompts/glossary/STT_PROCESSING_ALGORITHMS.uk.md) | [`UNIVERSAL_EDITORIAL_SPEC.uk.md`](prompts/glossary/UNIVERSAL_EDITORIAL_SPEC.uk.md) |

Индекс: [`STT_HOMOPHONES.example.md`](prompts/glossary/STT_HOMOPHONES.example.md)

**Универсальное ТЗ на вычитку (обезличенные требования заказчика):** см. таблицу выше, колонка «Универсальное ТЗ».

---

## Аудио → текст (STT)

Vox2Book **не привязан к Whisper**. Если у пользователя только аудио — предложите подходящий транскрибатор:

| Тип | Примеры |
|-----|---------|
| **Встроенный (локально)** | `python tools/transcribe_audio.py --install` — faster-whisper / Whisper |
| **Облачные API** | OpenAI Whisper API, Google STT, Azure Speech, AWS Transcribe, AssemblyAI, Deepgram, Speechmatics, Rev.ai |
| **Локальные альтернативы** | whisper.cpp, mlx-whisper (Mac), Vosk, GigaAM (RU) |
| **Уже с текстом** | Экспорт **Telegram**, Descript, Otter.ai, MacWhisper → сразу в `inputs/raw_texts/` |

Полная таблица: [`docs/ru/AUDIO_TRANSCRIPTION.md`](docs/ru/AUDIO_TRANSCRIPTION.md) · [EN](docs/en/AUDIO_TRANSCRIPTION.md) · [UK](docs/uk/AUDIO_TRANSCRIPTION.md)

---

## Порядок чтения (пример для RU)

1. `AGENTS.md`
2. `prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md`
3. `docs/ru/TECHNICAL_SPECIFICATION.md`
4. `prompts/ru/AGENT_WORKFLOW.md`
5. `docs/ru/SCENARIOS_CATALOG.md` — каталог сотен сценариев (авто-определение жанра/стиля/действий)
6. При необходимости: `prompts/ru/profiles/`

Для EN/UK — те же файлы в `prompts/en/` или `prompts/uk/` и `docs/en/` / `docs/uk/`.

---

## Авто-определение (одна фраза — полный запуск)

Программа **сама** определяет жанр, стиль и нужные действия по тексту.
Пользователю достаточно одной фразы:

```
Вычитай: [ИМЯ_ФАЙЛА или пусто]
```

- Авто-детектор: `tools/auto_detect.py` (чистая эвристика, без API)
- Каталог сценариев: `docs/ru/SCENARIOS_CATALOG.md` (100+ сценариев, 7 жанров, 50+ действий)
- Интеграция в пайплайн: `pipeline.py` → `auto_detect_plan()` → план сохраняется в `output/.llm_cache/auto_plan.json`
- Стартовый промпт: `prompts/ru/START_USER_PROMPT.md`

---

## Папки проекта

```text
inputs/raw_texts/     ← тексты для вычитки
inputs/audio/       ← аудио (сначала transcribe → raw_texts)
output/books/         ← готовые .docx
tools/transcribe_audio.py  ← Whisper / faster-whisper → raw_texts
tools/auto_detect.py       ← авто-определение жанра/стиля/действий (без API)
prompts/ru|en|uk/     ← промпты по языкам
docs/ru|en|uk/        ← документация (AUDIO_TRANSCRIPTION.md — для аудио)
docs/ru/SCENARIOS_CATALOG.md  ← каталог 100+ сценариев
config/               ← glossary_user.json, transcribe.json
```

---

## Правила

- Смысл автора 100%; не выдумывать факты  
- 8 аудитов + `check_cuts`  
- Говорить на языке папки, которую выбрал пользователь (или из `START_USER_PROMPT`)  
- Работа только в корне этого проекта  

---

## English summary

Read `prompts/en/` + `docs/en/` for English workflows. Same structure for `uk/`.

## Codebase Memory MCP

**MANDATORY: use Codebase Memory MCP graph tools FIRST — before reading files or making code changes.**

This rule applies to every request involving this codebase.

Always call `list_projects` first when you do not already know the project name, then use the `display_name` or exact `name` returned by that tool.

```json
// Step 0 — discover project names
mcp_codebase-memo_list_projects()

// Step 1 — use the project identifier returned above
mcp_codebase-memo_get_architecture({ "project": "<display_name>" })
```

### Workflow

1. Call `list_projects` to discover the correct project name.
2. Call `get_architecture(project)` to understand the codebase structure.
3. Use `search_graph` to find relevant symbols, `trace_call_path` for call chains.
4. Use `get_code_snippet` to read specific function implementations.
5. Only use `read_file` when you need exact raw content to edit a specific line.

### Available Tools (14 MCP tools)

**Indexing:**
- `index_repository(repo_path)` — Index a repository into the knowledge graph
- `list_projects` — List all indexed projects with node/edge counts
- `delete_project(project)` — Remove a project and all its graph data
- `index_status(project)` — Check indexing status

**Querying:**
- `search_graph(name_pattern, name_scope, label, file_pattern, exclude_file_pattern)` — Structured search by label, name/qualified_name, include/exclude file globs
- `trace_call_path(function_name, direction, depth)` — BFS call chain traversal
- `detect_changes(project)` — Map git diff to affected symbols + risk
- `query_graph(query)` — Execute Cypher-like graph queries (read-only)
- `get_graph_schema(project)` — Node/edge counts, relationship patterns
- `get_code_snippet(qualified_name)` — Read source code for a function
- `get_architecture(project)` — Codebase overview: languages, packages, routes, hotspots
- `search_code(pattern, project)` — Grep-like text search within indexed files
- `manage_adr(action)` — CRUD for Architecture Decision Records
- `ingest_traces(traces)` — Ingest runtime traces to validate HTTP edges
