<div align="center">

# 📚 Vox2Book — Universal Literature & Publishing Engine (Rust Edition)

[![Rust 1.75+](https://img.shields.io/badge/rust-1.75+-orange.svg)](https://www.rust-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Rustfmt](https://img.shields.io/badge/code%20style-rustfmt-000000.svg)](https://github.com/rust-lang/rustfmt)

<p align="center">
  <b>Vox2Book</b> is a high-performance, multi-genre literature processing, proofreading, and automated book publishing engine written in pure <b>Rust</b>.
  <br>
  It transforms raw voice transcriptions, prose, poetry, and plays into publication-ready <b>DOCX</b> manuscripts with zero dependencies.
</p>

</div>

---

### 🌐 Select Language / Выберите язык / Оберіть мову

[**English Documentation**](#1-english-documentation) &nbsp;•&nbsp; [**Русская документация**](#2-русскоязычная-документация) &nbsp;•&nbsp; [**Українська документація**](#3-українськомовна-документація)

---

## 1. English Documentation

<details>
<summary><b>📖 English Documentation (Click to Expand / Collapse)</b></summary>

<br>

### Overview

**Vox2Book** is a high-speed Rust software engine designed for comprehensive literary processing, text cleanup, publishing typography, quality auditing, and DOCX document generation. 

Built as a single standalone executable (`vox2book.exe`), it requires **no Python interpreter, no external dependencies, and no installation**.

---

### Core Architectural Capabilities

1. **Multi-Genre Literature Processing (`--genre`)**:
   - **`prose` (Fiction, Non-fiction, Novels)**: Chapter detection (`Chapter 1`, `Part I`), dialogue dashes (`—`), 18pt first-line paragraph indents, Times New Roman 12pt styling.
   - **`poetry` (Poetry, Rhymes, Verse)**: Stanza preservation, metric line breaks, 36pt stanza indents, Georgia 11.5pt styling without paragraph gaps.
   - **`drama` (Plays, Scripts, Theatre)**: Character names in bold uppercase (`AUTHOR.`, `CHARACTER.`), stage directions in italics/brackets `(...)`, Arial 11pt styling.
   - **`dialogue` (Voice Transcriptions, Interviews, Chat Chronicles)**: Chronological calendar day headers (`📅 19 January`), stateful speaker attribution, color-coded speaker styling.
   - **`academic` (Articles, Essays, Research Papers)**: Hierarchical H1/H2/H3 headings, double/1.5 line spacing, Times New Roman 12pt.
   - **`auto`**: Intelligent auto-detection of literature genre based on text syntax and line density.

2. **3 Flexible Launch Modes**:
   - 🖱️ **Drag-and-Drop**: Drag any `.txt`, `.md`, or folder onto `vox2book.exe` to instantly generate `book.docx`.
   - 💬 **Interactive Assistant**: Double-click `vox2book.exe` to open an interactive CLI wizard.
   - ⚡ **Command Line Interface**: `vox2book.exe --input "novel.txt" --genre prose --output "novel.docx"`.

3. **High-Speed Rust Audit & Cleanup Pipeline**:
   - **Orthography & Typography**: Guillemets (`«...»`), em-dashes (` — `), hyphenated particles (`-то`, `-нибудь`, `всё-таки`, `из-за`).
   - **STT Noise & Hallucination Purger**: Fast regex purification removing Whisper hallucinations (*Quiz河, quiero..., göra, sings*).
   - **Terminal Cut-off Control (`check_cuts`)**: Sentences cut-off prevention.

---

### Project Architecture

```
Vox2Book/
├── README.md                          # Trilingual documentation
├── Cargo.toml                         # Rust package manifest & dependencies
├── Cargo.lock                         # Locked dependency versions
├── src/                               # Core Rust engine
│   ├── main.rs                        # CLI, Drag-and-Drop & Prompt Entry
│   ├── lib.rs                         # Library entry point
│   ├── config.rs                      # Genre presets & typography patterns
│   ├── models.rs                      # Literature data structures
│   ├── extractors/                    # File readers & genre auto-detector
│   ├── cleaners/                      # Spam & STT purger
│   ├── editors/                       # Typography & genre editors
│   ├── validators/                    # Quality auditors
│   └── builders/                      # DOCX manuscript builder (docx-rs)
├── tests/                             # Rust test suite (cargo test)
│   └── universal_rust_tests.rs
└── archive/                           # Archived legacy Python implementation
    └── python_legacy_v1.zip
```

---

### Installation & Usage

#### 1. Build from Source
```bash
git clone https://github.com/kir-spec/Vox2Book.git
cd Vox2Book
cargo build --release
```

#### 2. CLI Execution Examples
```bash
# Process a Novel (Prose Mode)
./target/release/vox2book --input "novel.txt" --genre prose --output "novel.docx"

# Process a Poetry Collection
./target/release/vox2book --input "poems.txt" --genre poetry --output "poems.docx"

# Run Test Suite
cargo test
```

</details>

---

## 2. Русскоязычная документация

<details>
<summary><b>📖 Документация на русском языке (Нажмите, чтобы развернуть / свернуть)</b></summary>

<br>

### Обзор проекта

**Vox2Book** — высокопроизводительный программный комплекс и универсальный литературно-издательский конвейер на языке **Rust**. Движок предназначен для автоматической обработки, вычистки, типографики, аудита качества и генерации готовых печатных макетов книг в формате **DOCX**.

Скомпилирован в **один автономный исполняемый файл (`vox2book.exe`)**, не требующий Python, библиотек или установки.

---

### Архитектурные возможности ядра

1. **Многожанровая обработка литературы (`--genre`)**:
   - **`prose` (Проза, романы, повествования)**: выявление глав (`Глава 1`, `Часть I`), оформление диалогов с тире (`—`), абзацные отступы 18pt, *Times New Roman 12pt*.
   - **`poetry` (Поэзия, сборники стихотворений)**: сохранение строф, стихотворного размера, рифмовки, левый отступ 36pt, *Georgia 11.5pt*.
   - **`drama` (Драматургия, пьесы, сценарии)**: имена персонажей прописными жирными буквами (`АВТОР.`, `ПЕРСОНАЖ.`), ремарки в скобках курсивом, *Arial 11pt*.
   - **`dialogue` (Устные транскрибации, диалоги, интервью)**: хронологические метки дат (`📅 19 января`), привязка авторов, цветовое разделение спикеров.
   - **`academic` (Статьи, эссе, научные работы)**: иерархические заголовки H1/H2/H3, межстрочный интервал 1.5, *Times New Roman 12pt*.

2. **3 удобных режима запуска**:
   - 🖱️ **Drag-and-Drop**: перетаскивание любого файла мышкой прямо на `vox2book.exe`.
   - 💬 **Интерактивный помощник**: при обычном двойном клике откроется удобное меню.
   - ⚡ **Консоль**: `vox2book.exe --input "роман.txt" --genre prose --output "роман.docx"`.

---

### Структура проекта

```
Vox2Book/
├── README.md                          # Документация на трех языках
├── Cargo.toml                         # Спецификация Rust
├── src/                               # Исходный код Rust ядра
├── tests/                             # Автоматические тесты (cargo test)
└── archive/                           # Архив наследуемой Python версии
    └── python_legacy_v1.zip
```

#### Запуск автотестов
```bash
cargo test
```

</details>

---

## 3. Українськомовна документація

<details>
<summary><b>📖 Документація українською мовою (Натисніть, щоб розгорнути / згорнути)</b></summary>

<br>

### Огляд проєкту

**Vox2Book** — високопродуктивний програмний комплекс та універсальний літературно-видавничий конвеєр мовою **Rust**. Двигун призначений для автоматичної обробки, вичитки, типографіки, аудиту якості та генерації готових друкованих макетів книг у форматі **DOCX**.

Скомпільований в **один автономний виконуваний файл (`vox2book.exe`)**, який не потребує Python або встановлення сторонніх бібліотек.

---

### Варіанти запуску

#### 1. Збірка з вихідного коду
```bash
git clone https://github.com/kir-spec/Vox2Book.git
cd Vox2Book
cargo build --release
```

#### 2. Команди запуску
```bash
# Обробка роману (Проза)
./target/release/vox2book --input "роман.txt" --genre prose --output "роман.docx"

# Запуск тестів
cargo test
```

</details>

---

## 📄 License & Author

- **Author**: [kir-spec](https://github.com/kir-spec)
- **License**: MIT License. Open-source & free to use for literary and publishing projects.
