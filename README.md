<div align="center">

# Vox2Book

<p>
<strong>EN</strong><br/>
Raw transcripts &amp; drafts → publication-ready DOCX<br/>
<br/>
<strong>RU</strong><br/>
Сырой текст → литературно вычитанная книга (.docx)<br/>
<br/>
<strong>UK</strong><br/>
Сирий текст → вичитана книга DOCX
</p>

<br/>

[![Release](https://img.shields.io/badge/Release-23.07.2026-brightgreen.svg?style=for-the-badge&logo=github)](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)
[![AI](https://img.shields.io/badge/AI-Cursor%20·%20VS%20Code%20·%20LM%20Studio%20·%20Ollama%20·%20OpenAI-0099FF.svg?style=for-the-badge)](AGENTS.md)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)

<br/>

[EN](#en) · [RU](#ru) · [UK](#uk) · [AGENTS.md](AGENTS.md) · [Release](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)

</div>

---

<details id="en">
<summary><strong>EN — description</strong></summary>

<br/>

## What Vox2Book is

**Vox2Book** is a **publishing kit for AI assistants**: prompts, editorial rules, and scripts that turn **raw text** into a **formatted DOCX manuscript**.

| Input | Output |
|-------|--------|
| Whisper transcripts, dictation | Paragraphs, dialogues, typography |
| Drafts, articles, essays | Times New Roman 12, 1.15 spacing |
| Chat exports, monologues | `output/books/*.docx` |

**Note:** editing works on **text**. For **audio**, run local Whisper first — see [Audio → text](#en-audio) below.

**Core rule:** preserve 100% of the author's meaning. STT fixes **in sentence context only**, never global word replacement.

## How it works (3 steps)

```
1. Put source in inputs/raw_texts/
2. Copy prompts/en/START_USER_PROMPT.md into your AI chat
3. Collect .docx from output/books/
```

Optional: `pipeline.py` — automated chain via OpenAI, DeepSeek, LM Studio, or Ollama.

## <a id="en-audio"></a>Audio → text (Whisper)

| Step | Command |
|------|---------|
| 1. Install (once) | `python tools/transcribe_audio.py --install` |
| 2. Drop files | `inputs/audio/*.mp3` (`.wav`, `.ogg`, …) |
| 3. Transcribe | `python tools/transcribe_audio.py inputs/audio/file.mp3` |
| 4. Edit | Vox2Book prompt → `inputs/raw_texts/` → `output/books/` |

Models: `small` (CPU) · `medium` · **`large-v3-turbo`** · `large-v3`  
Docs: [`docs/en/AUDIO_TRANSCRIPTION.md`](docs/en/AUDIO_TRANSCRIPTION.md)

## Quick start (1 minute)

| Step | Action |
|------|--------|
| 1 | Clone repo, open in **Cursor** or **VS Code** |
| 2 | Open [`prompts/en/START_USER_PROMPT.md`](prompts/en/START_USER_PROMPT.md) |
| 3 | Paste into AI chat, point to `inputs/raw_texts/` |
| 4 | Result in **`output/books/`** |

## Who it's for

- Authors who dictate books and articles  
- Editors of voice messages and interviews  
- Anyone who wants **one editorial standard** in any AI tool  

Works with Cursor, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude.

## Repository layout

```text
Vox2Book/
├── inputs/audio/              ← audio (.mp3, .wav…) — step 1
├── inputs/raw_texts/            ← transcripts & texts
├── output/books/                ← finished .docx
├── tools/transcribe_audio.py    ← Whisper / faster-whisper
├── prompts/en/                ← English AI prompts
├── docs/en/                     ← English docs
└── AGENTS.md                    ← entry point for any AI
```

## Links

| | EN |
|---|-----|
| Start prompt | [START_USER_PROMPT](prompts/en/START_USER_PROMPT.md) |
| Editor prompt | [UNIVERSAL_EDITOR](prompts/en/UNIVERSAL_EDITOR_SYSTEM.md) |
| Docs | [docs/en/](docs/en/) |
| STT / typos | [guide](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) |
| Audio | [Whisper](docs/en/AUDIO_TRANSCRIPTION.md) |

</details>

<details id="ru">
<summary><strong>RU — описание</strong></summary>

<br/>

## Что это за проект

**Vox2Book** — **издательский комплект для нейросетей**: промпты, правила вычитки и скрипты, которые превращают **сырой текст** в **оформленный рукописный DOCX**.

| На входе | На выходе |
|----------|-----------|
| Расшифровки Whisper / диктовки | Абзацы, диалоги, типографика |
| Черновики, статьи, эссе | Times New Roman 12, интервал 1.15 |
| Экспорты чатов, монологи | `output/books/*.docx` |

**Важно:** вычитка работает с **текстом**. Для **аудио** сначала запустите транскрибацию Whisper — см. [«Аудио → текст»](#ru-audio).

**Главный принцип:** смысл автора — 100%. Ошибки STT правятся **только в контексте фразы**, не слепой заменой слов.

## Как это работает (3 шага)

```
1. Положите исходник в inputs/raw_texts/
2. Скопируйте prompts/ru/START_USER_PROMPT.md в чат с ИИ
3. Заберите .docx из output/books/
```

Опционально: `pipeline.py` — цепочка через OpenAI, DeepSeek, LM Studio или Ollama.

## <a id="ru-audio"></a>Аудио → текст (Whisper)

| Шаг | Команда |
|-----|---------|
| 1. Установка (один раз) | `python tools/transcribe_audio.py --install` |
| 2. Положить файлы | `inputs/audio/*.mp3` (`.wav`, `.ogg`, …) |
| 3. Распознать | `.\transcribe.bat inputs\audio\файл.mp3` |
| 4. Вычитка | промпт Vox2Book → `inputs/raw_texts/` → `output/books/` |

Модели: `small` (CPU) · `medium` · **`large-v3-turbo`** · `large-v3`  
Подробно: [`docs/ru/AUDIO_TRANSCRIPTION.md`](docs/ru/AUDIO_TRANSCRIPTION.md)

## С чего начать за 1 минуту

| Шаг | Действие |
|-----|----------|
| 1 | Клонируйте репозиторий, откройте в **Cursor** или **VS Code** |
| 2 | Откройте [`prompts/ru/START_USER_PROMPT.md`](prompts/ru/START_USER_PROMPT.md) |
| 3 | Вставьте в чат с ИИ, укажите файл в `inputs/raw_texts/` |
| 4 | Результат в **`output/books/`** |

Указатель: [`00_START_HERE__СКОПИРУЙ_ПРОМПТ/README.md`](00_START_HERE__СКОПИРУЙ_ПРОМПТ/README.md)

## Для кого

- Авторы, которые **наговаривают** книги и статьи  
- Редакторы расшифровок **голосовых** и интервью  
- Все, кому нужен **единый стандарт** вычитки в любой нейросети  

Работает с Cursor, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude.

## Структура репозитория

```text
Vox2Book/
├── inputs/audio/              ← аудио (.mp3, .wav…) — шаг 1
├── inputs/raw_texts/            ← транскрипты и тексты
├── output/books/                ← готовые .docx
├── tools/transcribe_audio.py    ← Whisper / faster-whisper
├── transcribe.bat               ← ярлык Windows
├── prompts/ru/                  ← промпты на русском
├── docs/ru/                     ← документация RU
└── AGENTS.md                    ← точка входа для нейросети
```

## Ссылки

| | RU |
|---|-----|
| Старт в чате | [START_USER_PROMPT](prompts/ru/START_USER_PROMPT.md) |
| Промпт редактора | [UNIVERSAL_EDITOR](prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md) |
| Справка | [docs/ru/](docs/ru/) |
| STT / опечатки | [руководство](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) |
| Аудио | [Whisper](docs/ru/AUDIO_TRANSCRIPTION.md) |

</details>

<details id="uk">
<summary><strong>UK — опис</strong></summary>

<br/>

## Що таке Vox2Book

**Vox2Book** — **видавничий комплект для ШІ**: промпти, правила вичитки та скрипти, що перетворюють **сирий текст** на **оформлений рукопис DOCX**.

| Вхід | Вихід |
|------|-------|
| Розшифровки Whisper / диктовки | Абзаци, діалоги, типографіка |
| Чернетки, статті, есе | Times New Roman 12, інтервал 1.15 |
| Експорти чатів, монологи | `output/books/*.docx` |

**Важливо:** вичитка працює з **текстом**. Для **аудіо** спочатку запустіть транскрибацію — див. [«Аудіо → текст»](#uk-audio).

**Головне правило:** зміст автора — 100%. Помилки STT — **лише в контексті речення**.

## Як це працює (3 кроки)

```
1. Покладіть джерело в inputs/raw_texts/
2. Скопіюйте prompts/uk/START_USER_PROMPT.md у чат із ШІ
3. Заберіть .docx з output/books/
```

Опційно: `pipeline.py` — ланцюжок через OpenAI, DeepSeek, LM Studio або Ollama.

## <a id="uk-audio"></a>Аудіо → текст (Whisper)

| Крок | Команда |
|------|---------|
| 1. Встановлення | `python tools/transcribe_audio.py --install` |
| 2. Файли | `inputs/audio/*.mp3` |
| 3. Розпізнати | `python tools/transcribe_audio.py inputs/audio/файл.mp3 --language uk` |
| 4. Вичитка | промпт Vox2Book → `inputs/raw_texts/` → `output/books/` |

Моделі: `small` · `medium` · **`large-v3-turbo`** · `large-v3`  
Документація: [`docs/uk/AUDIO_TRANSCRIPTION.md`](docs/uk/AUDIO_TRANSCRIPTION.md)

## Швидкий старт (1 хвилина)

| Крок | Дія |
|------|-----|
| 1 | Клонуйте репозиторій, відкрийте в **Cursor** або **VS Code** |
| 2 | Відкрийте [`prompts/uk/START_USER_PROMPT.md`](prompts/uk/START_USER_PROMPT.md) |
| 3 | Вставте в чат, вкажіть файл у `inputs/raw_texts/` |
| 4 | Результат у **`output/books/`** |

## Для кого

- Автори, які **надиктовують** тексти  
- Редактори **голосових** та інтерв'ю  
- Усі, кому потрібен **єдиний стандарт** вичитки в будь-якому ШІ  

Працює з Cursor, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude.

## Структура репозиторію

```text
Vox2Book/
├── inputs/audio/              ← аудіо — крок 1
├── inputs/raw_texts/            ← транскрипти та тексти
├── output/books/                ← готові .docx
├── tools/transcribe_audio.py    ← Whisper / faster-whisper
├── prompts/uk/                  ← промпти українською
├── docs/uk/                     ← документація UK
└── AGENTS.md                    ← вхід для нейромережі
```

## Посилання

| | UK |
|---|-----|
| Старт | [START_USER_PROMPT](prompts/uk/START_USER_PROMPT.md) |
| Промпт редактора | [UNIVERSAL_EDITOR](prompts/uk/UNIVERSAL_EDITOR_SYSTEM.md) |
| Довідка | [docs/uk/](docs/uk/) |
| STT / опечатки | [посібник](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) |
| Аудіо | [Whisper](docs/uk/AUDIO_TRANSCRIPTION.md) |

</details>

<br/>

## Navigation / Навигация / Навігація

| | EN | RU | UK |
|---|----|----|-----|
| **Start** | [prompts/en/](prompts/en/) | [prompts/ru/](prompts/ru/) | [prompts/uk/](prompts/uk/) |
| **Docs** | [docs/en/](docs/en/) | [docs/ru/](docs/ru/) | [docs/uk/](docs/uk/) |
| **Glossary** | [STT guide](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) | [STT](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) | [STT](prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) |
| **Audio** | [Whisper](docs/en/AUDIO_TRANSCRIPTION.md) | [Whisper](docs/ru/AUDIO_TRANSCRIPTION.md) | [Whisper](docs/uk/AUDIO_TRANSCRIPTION.md) |

<div align="center">

<br/>

**License / Лицензия / Ліцензія:** [MIT](LICENSE) · **Release:** [23.07.2026](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)

</div>
