<div align="center">

# 📚 Vox2Book — Universal Literature Processing & Automated Publishing Engine

[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg?style=for-the-badge&logo=rust)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/release-v2.6.0-green.svg?style=for-the-badge)](https://github.com/kir-spec/Vox2Book/releases)
[![AI Providers](https://img.shields.io/badge/AI_Gateway-LM_Studio%20%7C%20Ollama%20%7C%20OpenAI%20%7C%20Claude-0099FF.svg?style=for-the-badge)](https://github.com/kir-spec/Vox2Book)

**Next-Generation Hybrid AI & Rust Publishing Pipeline for Raw Voice Transcripts (Whisper STT), Manuscripts, and Book Formatting in DOCX.**

---

### 🌐 Quick Navigation & Documentation
[⚖️ **Project vs Prompt Comparison**](docs/PROJECT_VS_PROMPT.md) • [📂 **Project Directory Structure**](docs/PROJECT_STRUCTURE.md) • [📖 **Complete User Guide**](docs/USER_GUIDE.md) • [🚀 **Latest Releases**](https://github.com/kir-spec/Vox2Book/releases)

---

</div>

<br/>

<details>
<summary><strong>🇬🇧 English Documentation (Primary Language) — Click to Expand</strong></summary>

<br/>

## 🎯 Executive Overview

Vox2Book is an automated, enterprise-grade publishing suite built in **Rust** and powered by **LLM Neural Master Prompts**. It bridges the gap between raw, unpunctuated oral voice transcriptions (Whisper STT, dictaphone recordings) and polished, print-ready Word manuscripts (`.docx`).

---

## ⚖️ Why Use the Vox2Book Project Engine vs. Just a Prompt in ChatGPT?

| Feature / Capability | 📝 Copy-Pasting a Prompt into ChatGPT / Claude | 🚀 The Vox2Book Automated Project Engine |
| :--- | :--- | :--- |
| **1. Output Formatting** | Returns raw unformatted Markdown in a browser chat. Requires hours of manual copy-pasting, setting indents, margins, and Word styles. | **Automated Professional DOCX Compilation**: Generates a finished Word manuscript with proper book styles (*Times New Roman*, *Georgia*, *Arial*), 18pt indents, and running headers. |
| **2. Book Volume & Multi-Part Limit** | Web chat windows choke and truncate multi-page books or long 100-page manuscripts due to token limits. | **Streamed Chunking without Limits**: Automatically splits long books into optimal chunks, streams them through the Neural API, and merges them seamlessly. |
| **3. Privacy & 100% Offline AI** | Requires sending private personal voice recordings to public cloud servers abroad. | **100% Offline AI Integration**: Connects locally to **LM Studio** (`localhost:1234`) or **Ollama** (`localhost:11434`) on your graphics card without internet. |
| **4. Encoding & File Support** | Web chats only accept manually typed or pasted text. Non-UTF8 files (e.g. Windows-1251 / CP1251) get corrupted. | **Multi-Format & Multi-Encoding Ingestion**: Reads `.txt` (UTF-8, Windows-1251, BOM), `.docx`, `.md`, `.html`, and recursive folder batches. |
| **5. AI Conversational Cleanup** | AI models in web chats add conversational fluff (*"Here is your edited text..."*). | **Automated Sanitization**: Strips AI conversation filler, purges Whisper STT hallucinations (`Quiz河`), and sanitizes raw transcripts. |
| **6. Publishing Typography** | Web LLMs leave straight quotes `""` and hyphens `-`. | **Publisher Typography Engine**: Automatically converts quotes to Russian guillemets `«...»`, hyphens to em-dashes ` — `, and hyphenates particles (`из-за`, `-то`). |
| **7. Workflow Speed** | Hours of manual copy-pasting for each chapter. | **Single-Click & Scriptable**: Drag & drop into `vox2book.exe` or execute `python run_api_pipeline.py`. |

---

## 📂 Structured Workspace Layout

```ascii
E:\coding\работа с литературой\
├── inputs/                      # 📥 INPUT DIRECTORIES
│   ├── raw_texts/               # Raw text transcripts (.txt, .md, .docx, .html)
│   └── audio/                   # Raw audio recordings (.ogg, .wav, .mp3, .m4a)
├── output/                      # 📤 OUTPUT DIRECTORY FOR PRINT
│   └── books/                   # Formatted DOCX book manuscripts
├── prompts/                     # 🧠 NEURAL MASTER PROMPTS
│   └── MASTER_LLM_PROMPT.md    # Lead Literary Editor System Prompt
├── config.json                  # 🔑 API Gateway Config (OpenAI, DeepSeek, Claude, LM Studio, Ollama)
├── run_api_pipeline.py          # 🚀 Python API Pipeline Launcher
└── vox2book.exe                 # 🚀 Standalone Desktop GUI & CLI Executable
```

---

## 🚀 Supported AI Providers

1. **🖥️ LM Studio (Local Offline)**: `http://localhost:1234/v1` (OpenAI-compatible local server)
2. **🤖 Ollama AI (Local Offline)**: `http://localhost:11434` (`llama3`, `saiga`, `qwen`)
3. **☁️ OpenAI API**: `https://api.openai.com` (`gpt-4o`, `gpt-4o-mini`)
4. **☁️ DeepSeek API**: `https://api.deepseek.com` (`deepseek-chat`)
5. **☁️ Anthropic Claude API**: `https://api.anthropic.com` (`claude-3-5-sonnet`)

</details>

<br/>

<details>
<summary><strong>🇷🇺 Русская документация — Нажмите для раскрытия</strong></summary>

<br/>

## 🎯 Обзор проекта

Vox2Book — это специализированный измерительный и издательский комплекс нового поколения, созданный на **Rust** и интегрированный с **нейросетевыми промптами (LLM Master Prompts)** для превращения сырых устных расшифровок аудиозаписей (Whisper STT) и обычных текстов в полностью вычитанные книги и печатные макеты в формате **DOCX**.

---

## ⚖️ В чём разница между «Просто Промптом» и Проектом Vox2Book?

| Критерий | 📝 Только Промпт в чате браузера | 🚀 Полноценный проект Vox2Book |
| :--- | :--- | :--- |
| **1. Итоговый результат** | Выдает текст в окне браузера. Вам нужно вручную копировать его, вставлять в Word, настраивать шрифты и отступы. | **Готовая книга в формате Word (.docx)**: Автоматически создаёт готовый печатный макет с книжными шрифтами (*Times New Roman*, *Georgia*, *Arial*), красными строками 18pt, полями и заголовками. |
| **2. Работа с большими книгами** | В чате браузера есть жесткий лимит на длину ответа. Рукопись в 50–200 страниц нейросеть обрезает на полуслове. | **Потоковая обработка без лимитов**: Vox2Book автоматически разбивает большие книги на чанки, отправляет по API и объединяет в единый документ без потери текста. |
| **3. Конфиденциальность** | Отправляет ваши личные записи на зарубежные сервера в облако. | **100% Оффлайн на вашем ПК**: Работает локально через **LM Studio** или **Ollama** без интернета и утечки данных. |
| **4. Поддержка кодировок** | Файлы в русской кодировке Windows-1251 (CP1251) превращаются в кракозябры. | **Чтение любых кодировок**: Автоматически читает `.txt` (UTF-8, Windows-1251, BOM), `.docx`, `.md`, `.html` и папки. |
| **5. Очистка от мусора** | Нейросеть в чате приписывает личные фразы: *«Вот ваш вычитанный текст...»*. | **Автоматическая санитария**: Вырезает галлюцинации Whisper (`Quiz河`) и фразы нейросети, оставляя чистый текст книги. |
| **6. Типографика** | Нейросеть оставляет обычные кавычки `""` и дефисы `-`. | **Издательская корректура**: Преобразует кавычки в книжные `«ёлочки»`, тире в длинные ` — `, а также частицы (`из-за`, `-то`). |
| **7. Скорость** | Часы ручной работы по копипасту каждой главы из чата в Word. | **Запуск в 1 клик**: Перетащили файл в `vox2book.exe` или запустили `python run_api_pipeline.py`. |

---

## 🛠️ Инструкция по работе в IDE (Antigravity / Cursor / VS Code)

1. Откройте **Antigravity IDE**, **Cursor** или **VS Code**.
2. Откройте папку проекта через `File` → `Open Folder...` →Выберите `E:\coding\работа с литературой`.
3. Поместите файлы для вычистки в `inputs/raw_texts/`.
4. Настройте `config.json` (LM Studio, Ollama, OpenAI, DeepSeek, Claude) и запустите `python run_api_pipeline.py` или окно `vox2book.exe`.
5. Готовые вычитанные макеты DOCX появятся в папке `output/books/`.

</details>

<br/>

<details>
<summary><strong>🇺🇦 Українська документація — Натисніть для розгортання</strong></summary>

<br/>

## 🎯 Опис проекту

Vox2Book — це універсальний видавничий комплекс нового покоління на **Rust**, інтегрований з **нейромережевими промптами (LLM Master Prompts)** для перетворення сирих аудіо-розшифровок (Whisper STT) та текстів у повністю відредаговані книжкові макети у форматі **DOCX**.

---

## ⚖️ Порівняння: «Просто Промпт» vs Повноцінний проект Vox2Book

- **Просто Промпт у чаті**: Видає сирий текст у браузері. Потрібно вручну копіювати його у Word, налаштовувати шрифти та відступи.
- **Проект Vox2Book**: Автоматично зчитує будь-які файли та кодування (UTF-8, Windows-1251), вичитує через нейромережі (**LM Studio**, **Ollama**, **OpenAI**, **DeepSeek**, **Claude**), виконує книжкову типографіку (`«...»`, ` — `) та створює готовий макет книги Word (`.docx`).

---

## 🛠️ Налаштування середовища (Antigravity IDE / Cursor / VS Code)

1. Відкрийте папку проекту `E:\coding\работа с литературой` в IDE.
2. Покладіть вхідні файли у папку `inputs/raw_texts/`.
3. Налаштуйте `config.json` та запустіть `python run_api_pipeline.py` або `vox2book.exe`.
4. Готові макети книг збережуться у папці `output/books/`.

</details>
