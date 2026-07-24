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

Индекс: [`STT_HOMOPHONES.example.md`](prompts/glossary/STT_HOMOPHONES.example.md)

---

## Порядок чтения (пример для RU)

1. `AGENTS.md`
2. `prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md`
3. `docs/ru/TECHNICAL_SPECIFICATION.md`
4. `prompts/ru/AGENT_WORKFLOW.md`
5. При необходимости: `prompts/ru/profiles/`

Для EN/UK — те же файлы в `prompts/en/` или `prompts/uk/` и `docs/en/` / `docs/uk/`.

---

## Папки проекта

```text
inputs/raw_texts/     ← исходники
output/books/         ← готовые .docx
prompts/ru|en|uk/     ← промпты по языкам
docs/ru|en|uk/        ← документация по языкам
config/               ← glossary_user.json
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
