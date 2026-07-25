# Структура проекта Vox2Book

## Языки

```text
prompts/ru/     ← промпты на русском
prompts/en/     ← English prompts
prompts/uk/     ← промпти українською

docs/ru/        ← документация RU
docs/en/        ← documentation EN
docs/uk/        ← документація UK
```

Старт: `prompts/<язык>/START_USER_PROMPT.md`

## Дерево

```text
работа с литературой/
├── prompts/
│   ├── README.md
│   ├── ru/ | en/ | uk/
│   │   ├── START_USER_PROMPT.md
│   │   ├── UNIVERSAL_EDITOR_SYSTEM.md
│   │   ├── AGENT_WORKFLOW.md
│   │   ├── MASTER_LLM_PROMPT.md
│   │   └── profiles/
│   └── glossary/
├── docs/
│   ├── README.md
│   └── ru/ | en/ | uk/
├── inputs/raw_texts/
├── output/books/
├── config/glossary_user.json
├── AGENTS.md
└── pipeline.py
```

## Быстрый старт

1. `inputs/raw_texts/` — исходник  
2. `prompts/ru/START_USER_PROMPT.md` — в чат  
3. `output/books/` — результат  
