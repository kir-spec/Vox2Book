# Как работать с Vox2Book — справка для пользователя

Vox2Book вычитывает **любой** сырой текст: расшифровки речи, черновики, статьи, рассказы, диалоги, монологи.

---

## За 1 минуту

1. Откройте папку проекта в IDE (**File → Open Folder**).
2. Положите исходник в `inputs/raw_texts/` (`.txt`, `.md`, `.docx`, `.html`).
3. Скопируйте промпт из **`prompts/ru/START_USER_PROMPT.md`**.
4. Ответьте на вопросы ИИ (или «делай сразу»).
5. Заберите `.docx` из **`output/books/`**.

---

## Что делает нейросеть

| Этап | Суть |
|------|------|
| 1 | Гигиена источника (мусор STT/OCR, кодировка) |
| 2 | Литературная пересборка: предложения, абзацы, синтаксис |
| 3 | Полировка стиля (режим на выбор) |
| 4 | Типографика («ёлочки», тире —, частицы) |
| 5 | 8 аудитов + сборка DOCX |

Универсальный промпт: `prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md`  
Профили: `prompts/ru/profiles/`  
Ваши имена и STT-правки: `config/glossary_user.json` (см. `config/glossary_user.example.json`)  
**Контекстная правка опечаток (обязательно для ИИ):** `prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md` + `STT_HOMOPHONES.ru.md` — исправлять **только в контексте предложения**, не по словам и не глобальной заменой.

---

## Типы текстов

| Тип | Профиль |
|-----|---------|
| Голос / Whisper | `prompts/ru/profiles/SPEECH_TO_TEXT.md` + `prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md` + `STT_HOMOPHONES.ru.md` |
| Диалоги / чаты | `prompts/ru/profiles/DIALOGUE_TRANSCRIPT.md` |
| Статья / эссе | `prompts/ru/profiles/ACADEMIC_ESSAY.md` |
| Обычая проза | только универсальный промпт |

---

## Стартовые фразы

Папка `00_START_HERE__СКОПИРУЙ_ПРОМПТ/` или коротко:

```text
Vox2Book: прочитай AGENTS.md и UNIVERSAL_EDITOR_SYSTEM.ru.md, дай инструкцию,
посмотри inputs/raw_texts/, задай вопросы. DOCX не пиши, пока не отвечу.
```

---

## Папки

```text
inputs/raw_texts/   ← исходники
output/books/       ← готовые .docx
config/             ← ваш глоссарий (опционально)
prompts/            ← инструкции для нейросети
```

---

## API (необязательно)

В чате Cursor/Claude агент правит сам.  
Скрипты `pipeline.py` / `run_api_pipeline.py` — нужен `config.json` (OpenAI, LM Studio, Ollama…).

---

## FAQ

**Вся папка `inputs/raw_texts/`?** — Да, по запросу; агент уточнит порядок.

**Свои имена и бренды?** — Создайте `config/glossary_user.json` из примера.

**Где полный промпт редактора?** — `prompts/UNIVERSAL_EDITOR_SYSTEM.md` (EN) / `.ru.md` (RU).
