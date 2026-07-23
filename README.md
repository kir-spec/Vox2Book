<div align="center">

# 🚀 Vox2Book AI — From Voice Recordings to Printed Books in Seconds
### 🇷🇺 Vox2Book AI — От голосовых записей к печатным книгам за секунды
### 🇺🇦 Vox2Book AI — Від голосових записів до друкованих книг за секунди

<br/>

[![Release](https://img.shields.io/badge/Release-23.07.2026-brightgreen.svg?style=for-the-badge&logo=github)](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)
[![Universal AI](https://img.shields.io/badge/AI%20Compatibility-Antigravity%20%7C%20Cursor%20%7C%20LM%20Studio%20%7C%20Ollama%20%7C%20OpenAI%20%7C%20Claude-0099FF.svg?style=for-the-badge&logo=openai)](https://github.com/kir-spec/Vox2Book)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Output](https://img.shields.io/badge/Format-Instant%20DOCX%20Manuscripts-blueviolet.svg?style=for-the-badge&logo=microsoftword)](output/books/)

<br/>

**🇬🇧 Universal AI Publishing Engine. Works seamlessly inside ANY AI environment & IDE (Antigravity IDE, Cursor, VS Code), Local AI servers (LM Studio, Ollama), and Cloud Neural APIs (OpenAI, DeepSeek, Claude).**  
**🇷🇺 Универсальный ИИ-издательский комплекс. Работает в ЛЮБОЙ программе и нейросети: Antigravity IDE, Cursor, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude.**  
**🇺🇦 Універсальний ІІ-видавничий комплекс. Працює у БУДЬ-ЯКІЙ програмі та нейромережі: Antigravity IDE, Cursor, VS Code, LM Studio, Ollama, OpenAI, DeepSeek, Claude.**

---

### 🌐 Quick Navigation & Product Guides / Быстрая навигация
[✨ **Why Vox2Book Beats Copy-Pasting Prompts**](docs/PROJECT_VS_PROMPT.md) • [📂 **Smart Workspace Layout**](docs/PROJECT_STRUCTURE.md) • [📖 **Complete User Guide**](docs/USER_GUIDE.md) • [🚀 **Download Official Release 23.07.2026**](https://github.com/kir-spec/Vox2Book/releases/tag/23.07.2026)

---

</div>

<br/>

<details>
<summary><strong>🇬🇧 English Documentation — Click to Expand / Collapse</strong></summary>

<br/>

## 🔥 Universal Compatibility Across ALL AI Programs & IDEs

Vox2Book AI is engineered for total flexibility. It runs seamlessly inside **ANY AI environment or program**:
* **AI Coding IDEs & Agents**: **Antigravity IDE**, **Cursor**, **VS Code**, **Windsurf**.
* **Local Offline AI Desktop Servers**: **LM Studio** (`localhost:1234`), **Ollama** (`localhost:11434`), **Jan AI**, **KoboldCPP**.
* **Cloud AI Models & APIs**: **OpenAI (GPT-4o)**, **DeepSeek API**, **Anthropic Claude**, **Google Gemini**.

---

## ⚡ 4 Game-Changing Features

### 🎙️ 1. From Messy Voice Monologues to Structured Books
Speak your thoughts naturally into any dictaphone or Whisper STT recorder. Vox2Book automatically detects sentence boundaries, removes filler words ("uh", "um"), organizes thoughts into logical paragraphs, and structures dialogues.

### 🤖 2. Works in ANY AI Software & IDE
Whether you prefer working inside **Antigravity IDE**, **Cursor**, **VS Code**, or local AI servers like **LM Studio** and **Ollama**, Vox2Book fits directly into your favorite workflow.

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

## 📂 Project Directory Architecture

```ascii
E:\coding\работа с литературой\
├── inputs/                      # 📥 INPUT DIRECTORIES
│   ├── raw_texts/               # Drop your text files & transcripts here (.txt, .md, .docx)
│   └── audio/                   # Drop your raw audio files here (.mp3, .wav, .ogg)
├── output/                      # 📤 OUTPUT DIRECTORY
│   └── books/                   # ALWAYS saves finished DOCX book manuscripts here!
├── config.json                  # 🔑 AI Gateway Settings (Antigravity, Cursor, LM Studio, Ollama, Cloud)
└── pipeline.py                  # 🚀 Multi-Stage Virtual Editorial Board Chain
```

</details>

<br/>

<details>
<summary><strong>🇷🇺 Русская документация — Нажмите для раскрытия / сворачивания</strong></summary>

<br/>

## 🔥 Универсальная совместимость с ЛЮБОЙ программой и Нейросетью

Vox2Book AI разработан для максимальной свободы автора. Программа работает в **абсолютно ЛЮБОЙ среде и нейросетевой программе**:
* **ИИ-редакторы и IDE**: **Antigravity IDE**, **Cursor**, **VS Code**, **Windsurf**.
* **Локальные ИИ-серверы на ПК**: **LM Studio** (`http://localhost:1234`), **Ollama** (`http://localhost:11434`), **Jan AI**, **KoboldCPP**.
* **Облачные Нейросети и API**: **OpenAI (GPT-4o)**, **DeepSeek API**, **Anthropic Claude**, **Google Gemini**.

---

## ⚡ 4 Ключевых преимущества проекта

### 🎙️ 1. Из наговоренного аудио — в готовую печатную книгу
Наговаривайте свои мысли на любой диктофон или распознаватель речи (Whisper STT). Vox2Book сам разобьет сплошной поток слов на логические главы, абзацы и диалоги, вырезав слова-паразиты («ну», «э-э», «как бы»).

### 🤖 2. Работает в ЛЮБОЙ программе и среде
Используйте Vox2Book там, где вам удобно: прямо в **Antigravity IDE**, **Cursor**, **VS Code**, локально через **LM Studio** / **Ollama** или через облачные API.

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

</details>

<br/>

<details>
<summary><strong>🇺🇦 Українська документація — Натисніть для розгортання / згортання</strong></summary>

<br/>

## 🔥 Універсальна сумісність з БУДЬ-ЯКОЮ програмою та нейромережею

Vox2Book AI працює у **будь-якому середовищі**:
* **ІІ-редактори та IDE**: **Antigravity IDE**, **Cursor**, **VS Code**, **Windsurf**.
* **Локальні ІІ-сервери**: **LM Studio**, **Ollama**, **Jan AI**.
* **Хмарні нейромережі**: **OpenAI (GPT-4o)**, **DeepSeek**, **Claude**, **Gemini**.

---

## ⚡ 4 Ключові переваги

1. **Від диктофона до книги**: Автоматичний поділ на розділи та виправлення помилок мовлення.
2. **Працює у будь-якій програмі**: Antigravity IDE, Cursor, VS Code, LM Studio, Ollama.
3. **Видавнича типографіка Word**: Книжкові лапки `«...»`, тире ` — `, червоні рядки 18pt.
4. **Збереження в `output/books/`**: Усі готові книги зберігаються у `output/books/`.

</details>
