<div align="center">

# 🚀 Vox2Book AI — From Voice Recordings to Printed Books in Seconds
### 🇷🇺 Vox2Book AI — От голосовых записей к печатным книгам за секунды
### 🇺🇦 Vox2Book AI — Від голосових записів до друкованих книг за секунди

<br/>

[![Release](https://img.shields.io/badge/Release-v7.0.0%20Trilingual%20Landing-brightgreen.svg?style=for-the-badge&logo=github)](https://github.com/kir-spec/Vox2Book/releases)
[![AI Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline%20%26%20Private-0099FF.svg?style=for-the-badge&logo=security)](https://lmstudio.ai)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Output](https://img.shields.io/badge/Format-Instant%20DOCX%20Manuscripts-blueviolet.svg?style=for-the-badge&logo=microsoftword)](output/books/)

<br/>

**🇬🇧 Transform messy, unpunctuated voice transcripts (Whisper STT) and raw drafts into crisp, beautifully formatted printed books.**  
**🇷🇺 Превратите сырые устные расшифровки монологов (Whisper STT) и черновики в вычитанные печатные книги в формате DOCX.**  
**🇺🇦 Перетворіть сирі аудіо-монологи (Whisper STT) та черновики на готові до друку книги у форматі DOCX.**

---

### 🌐 Quick Navigation & Product Guides / Быстрая навигация
[✨ **Why Vox2Book Beats Copy-Pasting Prompts**](docs/PROJECT_VS_PROMPT.md) • [📂 **Smart Workspace Layout**](docs/PROJECT_STRUCTURE.md) • [📖 **Complete User Guide**](docs/USER_GUIDE.md) • [🚀 **Download Latest Release**](https://github.com/kir-spec/Vox2Book/releases)

---

</div>

<br/>

<details>
<summary><strong>🇬🇧 English Documentation — Click to Expand / Collapse</strong></summary>

<br/>

## 🔥 Why Authors, Creators & Editors Love Vox2Book AI

Stop wasting hundreds of hours manually fixing unpunctuated dictaphone transcripts! **Vox2Book AI** acts as your personal automated publishing agency. It ingests raw speech monologues, runs them through a multi-stage virtual editorial board, cleans up technical jargon, applies publisher typography, and formats everything into a print-ready Word `.docx` manuscript.

---

## ⚡ 4 Game-Changing Features

### 🎙️ 1. From Messy Voice Monologue to Structured Chapters
Speak your thoughts naturally into any dictaphone or Whisper STT recorder. Vox2Book automatically detects sentence boundaries, removes filler words ("uh", "um", "you know"), organizes thoughts into logical paragraphs, and structures dialogues.

### 🔒 2. 100% Private, Free & Offline AI Integration
Keep your creative manuscripts completely confidential! Connect Vox2Book directly to local AI engines like **LM Studio** (`http://localhost:1234`) or **Ollama** (`http://localhost:11434`) running locally on your graphics card. No internet required, no subscription fees, no data leaks.

### 🎨 3. Publishing-Grade Typography & Word Layouts
Every compiled manuscript comes pre-formatted to professional book standards:
* **Classic Fonts**: *Times New Roman* 12pt body text with 1.15 line spacing.
* **Red-Line Indents**: Professional 18pt first-line paragraph indents.
* **Punctuation Correction**: Automatic guillemets (`«...»`), em-dashes (` — `), and particle hyphenation.

### 🧠 4. Automatic Dictaphone Jargon Purger
Whisper STT frequently mishears technical terms. Vox2Book automatically detects and replaces English dictaphone jargon:
* `"you es bee"` / `"usb drive"` ➔ `USB`
* `"es es dee"` / `"solid state drive"` ➔ `SSD`
* `"west digital"` ➔ `Western Digital`
* `"a data"` ➔ `ADATA`
* `"three point five inch"` ➔ `3.5-inch`

---

## ⚖️ Product Comparison: Vox2Book vs. Copy-Pasting Prompts in Web Chat

| Feature | 📝 Web Chat Prompt (ChatGPT / Claude) | 🚀 Vox2Book AI Publishing Suite |
| :--- | :--- | :--- |
| **Output Document** | Raw text box response. Requires hours of manual copy-pasting and styling in Word. | **Instant Finished DOCX Manuscript**: Pre-styled Word document with book margins, indents, and headers. |
| **Manuscript Length** | Gets choked and truncated by web character limits on 50+ page manuscripts. | **Unlimited Streaming Pipeline**: Automatically streams long manuscripts chunk by chunk without missing words. |
| **Data Privacy** | Sends your private manuscripts to public cloud servers. | **100% Local & Private**: Runs completely offline with LM Studio or Ollama on your PC. |
| **File Compatibility** | Fails or corrupts non-UTF8 files (Windows-1251 / CP1251). | **Universal Ingestion**: Automatically handles `.txt` (UTF-8, Windows-1251), `.docx`, `.md`, `.html`. |
| **Output Directory** | Unorganized file saving. | **Automated Export**: All finished books are neatly organized in `output/books/`. |

---

## 📂 Project Directory Architecture

```ascii
E:\coding\работа с литературой\
├── inputs/                      # 📥 INPUT DIRECTORIES
│   ├── raw_texts/               # Drop your text files & transcripts here (.txt, .md, .docx)
│   └── audio/                   # Drop your raw audio files here (.mp3, .wav, .ogg)
├── output/                      # 📤 OUTPUT DIRECTORY
│   └── books/                   # ALWAYS saves finished DOCX book manuscripts here!
├── config.json                  # 🔑 AI Gateway Settings (LM Studio, Ollama, OpenAI, DeepSeek, Claude)
└── pipeline.py                  # 🚀 Multi-Stage Virtual Editorial Board Chain
```

</details>

<br/>

<details>
<summary><strong>🇷🇺 Русская документация — Нажмите для раскрытия / сворачивания</strong></summary>

<br/>

## 🔥 Почему авторы и блогеры выбирают Vox2Book AI

Забудьте о сотнях часов рутинной ручной расшифровки и редактирования монологов с диктофона! **Vox2Book AI** — это ваше личное автоматизированное литературное издательство. Программа берет сырой устный текст, проводит его через виртуальную редакцию, исправляет ошибки распознавания речи, расставляет книжную типографику и мгновенно выдает готовый макет книги в формате Word (`.docx`).

---

## ⚡ 4 Ключевых преимущества проекта

### 🎙️ 1. Из наговоренного аудио — в готовую печатную книгу
Наговаривайте свои мысли на любой диктофон или распознаватель речи (Whisper STT). Vox2Book сам разобьет сплошной поток слов на логические главы, абзацы и диалоги, вырезав слова-паразиты («ну», «э-э», «как бы»).

### 🔒 2. 100% Конфиденциально, Бесплатно и Оффлайн
Сохраняйте полную конфиденциальность ваших книг! Vox2Book напрямую подключается к локальным нейросетям **LM Studio** (`http://localhost:1234`) и **Ollama** (`http://localhost:11434`), работающим на вашей видеокарте. Без интернета, подписок и утечек данных.

### 🎨 3. Издательская типографика и макет Word
Каждый готовый документ верстается по стандартам книгопечатания:
* **Классические шрифты**: *Times New Roman 12pt*, межстрочный интервал 1.15.
* **Красная строка**: Профессиональные отступы абзацев 18pt (0.5 дюйма).
* **Типографика**: Автоматические книжные кавычки `«ёлочки»`, длинные тире ` — ` и дефисные частицы (`из-за`, `из-под`, `всё-таки`).

### 🧠 4. Умный исправитель диктофонного сленга
Whisper часто ошибается на технических терминах. Vox2Book автоматически распознает и исправляет оговорки на русском языке:
* `"те из бы"` / `"юсб"` ➔ `USB`
* `"ссд"` ➔ `SSD-накопитель`
* `"в стране джетал"` ➔ `Western Digital`
* `"а дата"` ➔ `ADATA`
* `"35 размер"` ➔ `3.5-дюймовый`

---

## ⚖️ Сравнение: Vox2Book AI vs. Копирование промптов в браузерный чат

| Возможность | 📝 Копирование промпта в чат (ChatGPT / Claude) | 🚀 Издательский комплекс Vox2Book AI |
| :--- | :--- | :--- |
| **Итоговый документ** | Сырой текст в окне браузера. Требует часов ручной работы по копипасту и форматированию в Word. | **Готовый макет DOCX**: Завершенный файл книги с полями, шрифтами и красными строками. |
| **Объем рукописи** | Обрезает текст на полуслове при обработке книг длиннее 50 страниц. | **Потоковая обработка без ограничений**: Автоматически обрабатывает рукописи любого объема. |
| **Приватность** | Отправляет ваши личные тексты на внешние облачные сервера. | **100% Оффлайн**: Работает полностью локально через LM Studio или Ollama. |
| **Поддержка кодировок** | Превращает в кракозябры файлы в кодировке Windows-1251 (CP1251). | **Любые файлы**: Распознает `.txt` (UTF-8, Windows-1251), `.docx`, `.md`, `.html`. |
| **Сохранение результатов** | Файлы путаются или теряются в загрузках. | **Порядок в папках**: Все готовые книги автоматически сохраняются в `output/books/`. |

</details>

<br/>

<details>
<summary><strong>🇺🇦 Українська документація — Натисніть для розгортання / згортання</strong></summary>

<br/>

## 🔥 Чому автори обирають Vox2Book AI

Забудьте про сотні годин рутинного редагування монологів з диктофона! **Vox2Book AI** — це ваше особисте автоматизоване видавництво. Програма бере сирий аудіо-текст, проводить його через віртуальну редакцію, виправляє помилки розпізнавання мовлення, застосовує типографіку та зберігає готовий макет книги Word (`.docx`).

---

## ⚡ 4 Ключові переваги

### 🎙️ 1. Від диктофона до книги
Створюйте книги голосом! Vox2Book автоматично розбиває монолог на розділи, абзаци та виправляє помилки усної мови.

### 🔒 2. 100% Конфіденційно та Оффлайн
Зберігайте повну приватність за допомогою **LM Studio** та **Ollama**, що працюють локально на вашому ПК без інтернету.

### 🎨 3. Видавнича типографіка Word
Автоматичні книжкові лапки `«...»`, довгі тире ` — `, червоні рядки 18pt та шрифти *Times New Roman 12pt*.

### 🧠 4. Розумне виправлення диктофонного сленгу
Whisper часто помиляється на технічних термінах. Vox2Book автоматично розпізнає та виправляє помилки укр мовою:
* `"те із би"` / `"юсб"` ➔ `USB`
* `"ссд"` ➔ `SSD-накопичувач`
* `"вестерн діжитал"` ➔ `Western Digital`
* `"а дата"` ➔ `ADATA`
* `"3,5 дюйма"` ➔ `3.5-дюймовий`

---

## ⚖️ Збереження в `output/books/`
Усі готові вичитані книги автоматично зберігаються у папку `output/books/`.

</details>
