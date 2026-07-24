<div align="center">

# Vox2Book

### Сырой текст → литературно вычитанная книга в Word (.docx)

**English:** Raw transcripts & drafts → publication-ready DOCX · **Українська:** Сирий текст → вичитана книга DOCX

<br/>

[![Release](https://img.shields.io/badge/Release-23.07.2026-brightgreen.svg?style=for-the-badge&logo=github)](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)
[![AI](https://img.shields.io/badge/Работает%20с-Cursor%20·%20VS%20Code%20·%20LM%20Studio%20·%20Ollama%20·%20OpenAI-0099FF.svg?style=for-the-badge)](AGENTS.md)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)

</div>

---

## Что это за проект

**Vox2Book** — это **издательский комплект для нейросетей**: готовые промпты, правила вычитки и скрипт сборки, которые превращают **любой сырой текст** в **оформленный рукописный DOCX**.

| На входе | На выходе |
|----------|-----------|
| Расшифровки Whisper / диктовки | Абзацы, диалоги, типографика |
| Черновики, статьи, эссе | Times New Roman 12, интервал 1.15 |
| Экспорты чатов, монологи | Файл в `output/books/*.docx` |

**Важно:** Vox2Book **не заменяет** распознавание речи. Сначала получите текст (Whisper, Telegram, диктофон с STT) — затем отдайте его Vox2Book на литературную правку.

**Главный принцип:** смысл автора сохраняется на 100%; исправляются орфография, синтаксис, структура и оформление. Ошибки STT правятся **только в контексте фразы**, а не слепой заменой слов.

---

## Как это работает (3 шага)

```
1. Положите исходник в inputs/raw_texts/
2. Скопируйте промпт из prompts/ru|en|uk/START_USER_PROMPT.md в чат с ИИ
3. Заберите готовый .docx из output/books/
```

Нейросеть читает инструкции из репозитория (`AGENTS.md`, системный промпт редактора, 8 аудитов качества) и правит текст как профессиональный корректор.

Опционально: `pipeline.py` — автоматическая цепочка (очистка STT → ИИ → типографика → DOCX) через OpenAI, DeepSeek, LM Studio или Ollama.

---

## С чего начать за 1 минуту

| Шаг | Действие |
|-----|----------|
| 1 | Клонируйте репозиторий и откройте папку в **Cursor**, **VS Code** или другой IDE |
| 2 | Выберите язык инструкций: [`prompts/ru/`](prompts/ru/) · [`prompts/en/`](prompts/en/) · [`prompts/uk/`](prompts/uk/) |
| 3 | Откройте **`START_USER_PROMPT.md`** в выбранной папке и вставьте текст в чат с ИИ |
| 4 | Укажите файл из `inputs/raw_texts/` (или положите его туда) |
| 5 | Получите результат в **`output/books/`** |

Краткий указатель: [`00_START_HERE__СКОПИРУЙ_ПРОМПТ/README.md`](00_START_HERE__СКОПИРУЙ_ПРОМПТ/README.md)

---

## Для кого

- Авторы, которые **наговаривают** книги и статьи в диктофон
- Редакторы расшифровок **голосовых сообщений** и интервью
- Все, кому нужен **единый стандарт** литературной вычитки в любой нейросети

Работает с **любым ИИ**: Cursor, Antigravity IDE, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude — без привязки к одному вендору.

---

## Структура репозитория

```text
Vox2Book/
├── inputs/raw_texts/     ← сюда исходники (.txt, .md, .docx)
├── output/books/         ← сюда готовые рукописи .docx
├── prompts/ru|en|uk/     ← промпты и сценарий для ИИ (по языкам)
├── prompts/glossary/     ← правила контекстной правки STT-ошибок
├── docs/ru|en|uk/        ← 8 аудитов качества, справка
├── config.json           ← настройки API (если используете pipeline.py)
├── pipeline.py           ← автоматический конвейер (опционально)
└── AGENTS.md             ← точка входа для любой нейросети
```

---

## Навигация

| | Русский | English | Українська |
|---|---------|---------|------------|
| **Старт в чате** | [START_USER_PROMPT](prompts/ru/START_USER_PROMPT.md) | [START](prompts/en/START_USER_PROMPT.md) | [START](prompts/uk/START_USER_PROMPT.md) |
| **Промпт редактора** | [UNIVERSAL_EDITOR](prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md) | [UNIVERSAL_EDITOR](prompts/en/UNIVERSAL_EDITOR_SYSTEM.md) | [UNIVERSAL_EDITOR](prompts/uk/UNIVERSAL_EDITOR_SYSTEM.md) |
| **Справка** | [docs/ru/](docs/ru/) | [docs/en/](docs/en/) | [docs/uk/](docs/uk/) |
| **STT / опечатки** | [руководство](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) | [guide](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) | [посібник](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) |

---

<details>
<summary><strong>🇬🇧 English — full description</strong></summary>

<br/>

## What Vox2Book is

**Vox2Book** is a **publishing kit for AI assistants**: prompts, editorial rules, and an optional build script that turn **raw text** into a **formatted DOCX manuscript**.

**Input:** Whisper transcripts, chat exports, drafts, articles, dialogues.  
**Output:** Edited prose in `output/books/*.docx` (Times New Roman 12, 1.15 spacing, book typography).

Vox2Book does **not** perform speech recognition — transcribe first, then edit here.

**Core rule:** preserve 100% of the author's meaning; fix grammar, structure, and layout. STT errors are corrected **in sentence context only**, never by global word replacement.

## Quick start

1. Open the repo in Cursor, VS Code, or any IDE.  
2. Pick a language folder: `prompts/en/` (or `ru/`, `uk/`).  
3. Copy `START_USER_PROMPT.md` into your AI chat.  
4. Point to a file in `inputs/raw_texts/`.  
5. Collect the result from `output/books/`.

Works with **any AI**: Cursor, LM Studio, Ollama, OpenAI, DeepSeek, Claude.

</details>

<details>
<summary><strong>🇺🇦 Українська — повний опис</strong></summary>

<br/>

## Що таке Vox2Book

**Vox2Book** — **видавничий комплект для ШІ**: промпти, правила вичитки та опційний скрипт збірки, що перетворюють **сирий текст** на **оформлений рукопис DOCX**.

**Вхід:** розшифровки Whisper, чернетки, чати, статті, діалоги.  
**Вихід:** вичитаний текст у `output/books/*.docx`.

Vox2Book **не розпізнає мовлення** — спочатку отримайте текст, потім вичитуйте тут.

**Головне правило:** зміст автора — 100%; виправляються орфографія, структура й оформлення. Помилки STT — **лише в контексті речення**.

## Швидкий старт

1. Відкрийте репозиторій у Cursor, VS Code або іншій IDE.  
2. Оберіть мову: `prompts/uk/` (або `ru/`, `en/`).  
3. Скопіюйте `START_USER_PROMPT.md` у чат із ШІ.  
4. Вкажіть файл у `inputs/raw_texts/`.  
5. Заберіть результат з `output/books/`.

</details>

<br/>

<div align="center">

**Лицензия:** [MIT](LICENSE) · **Релиз:** [23.07.2026](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)

</div>
