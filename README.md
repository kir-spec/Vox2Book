<div align="center">

# 📚 Vox2Book — Universal Neural API Literature Processing Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/release-v3.0.0-green.svg?style=for-the-badge)](https://github.com/kir-spec/Vox2Book/releases)
[![AI Gateway](https://img.shields.io/badge/AI_Gateway-LM_Studio%20%7C%20Ollama%20%7C%20OpenAI%20%7C%20Claude-0099FF.svg?style=for-the-badge)](https://github.com/kir-spec/Vox2Book)

**Pure API Publishing Pipeline for Raw Voice Transcripts (Whisper STT), Manuscripts, and Book Formatting in DOCX.**

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

Vox2Book is an automated API publishing engine powered by **Neural Network APIs** (LM Studio, Ollama, OpenAI, DeepSeek, Claude). It automatically reads input transcripts from `inputs/raw_texts/` and **saves all compiled DOCX manuscripts into `output/books/`**.

---

## 📂 Structured Workspace Layout

```ascii
E:\coding\работа с литературой\
├── inputs/                      # 📥 INPUT DIRECTORIES
│   ├── raw_texts/               # Raw text transcripts (.txt, .md, .docx, .html)
│   └── audio/                   # Raw audio recordings (.ogg, .wav, .mp3, .m4a)
├── output/                      # 📤 OUTPUT DIRECTORY FOR PRINT
│   └── books/                   # ALWAYS saves formatted DOCX book manuscripts here!
├── config.json                  # 🔑 API Gateway Config (OpenAI, DeepSeek, Claude, LM Studio, Ollama)
└── run_api_pipeline.py          # 🚀 Main Neural API Publishing Script
```

---

## 🚀 Execution Example

```bash
python run_api_pipeline.py inputs/raw_texts/my_transcript.txt
```
The output manuscript will be automatically generated at `output/books/my_transcript.docx`.

</details>

<br/>

<details>
<summary><strong>🇷🇺 Русская документация — Нажмите для раскрытия</strong></summary>

<br/>

## 🎯 Обзор проекта

Vox2Book — это чистый API-конвейер для вычистки устных монологов (Whisper STT) через нейросети (**LM Studio**, **Ollama**, **OpenAI**, **DeepSeek**, **Claude**) и **автоматического сохранения готовых книг в папку `output/books/`**.

---

## 📂 Папки и выходной результат

- **Все входные материалы**: хранятся в `inputs/raw_texts/`.
- **Все готовые вычитанные книги**: автоматически сохраняются исключительно в **`output/books/`**.

---

## 🚀 Запуск вычистки через API

```bash
python run_api_pipeline.py inputs/raw_texts/мой_текст.txt
```

Готовый макет книги сохраняется в: `output/books/мой_текст.docx`.

</details>

<br/>

<details>
<summary><strong>🇺🇦 Українська документація — Натисніть для розгортання</strong></summary>

<br/>

## 🎯 Опис проекту

Vox2Book — це чистий API-конвеєр для вичитування тексту через нейромережі (**LM Studio**, **Ollama**, **OpenAI**, **DeepSeek**, **Claude**) з **автоматичним збереженням готових макетів книг у папку `output/books/`**.

---

## 🚀 Запуск через API

```bash
python run_api_pipeline.py inputs/raw_texts/my_text.txt
```
Готовий макет зберігається у: `output/books/my_text.docx`.

</details>
