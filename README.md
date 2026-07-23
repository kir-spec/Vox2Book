<div align="center">

# 📚 Vox2Book — Universal Literature & Publishing Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <b>Vox2Book</b> is an advanced, multi-genre literature processing, proofreading, and automated book publishing engine.
  <br>
  It transforms raw voice transcriptions, chat logs, prose, poetry, and plays into publication-ready <b>DOCX</b> manuscripts.
</p>

</div>

---

## 🌐 Language Options / Выбор языка / Вибір мови

<div align="center">

| Language / Язык / Мова | Status / Статус | Documentation / Документация |
| :--- | :---: | :--- |
| **English** | 🟢 Ready | [View English Documentation](#1-english-documentation) |
| **Русский** | 🟢 Готово | [Перейти к русской документации](#2-русскоязычная-документация) |
| **Українська** | 🟢 Готово | [Перейти до української документації](#3-українськомовна-документація) |

</div>

---

## 1. English Documentation

<details>
<summary><b>📖 Click to expand English Documentation (Expand / Collapse)</b></summary>

<br>

### Overview

**Vox2Book** is an enterprise-grade Python software engine designed for comprehensive literary processing, text cleanup, publishing typography, quality auditing, and DOCX document generation. 

Whether you are converting raw Speech-to-Text (STT) voice transcriptions, multi-speaker messenger exports (Telegram HTML), classic fiction novels, poetic stanzas, or theatrical plays, **Vox2Book** automatically analyzes, cleanses, formats, and builds beautifully styled manuscripts.

---

### Core Architectural Capabilities

1. **Multi-Genre Literature Processing (`--genre`)**:
   - **`prose` (Fiction, Non-fiction, Novels)**: Chapter detection (`Chapter 1`, `Part I`), dialogue dashes (`—`), 18pt first-line paragraph indents, Times New Roman 12pt styling.
   - **`poetry` (Poetry, Rhymes, Verse)**: Stanza preservation, metric line breaks, 36pt stanza indents, Georgia 11.5pt styling without paragraph gaps.
   - **`drama` (Plays, Scripts, Theatre)**: Character names in bold uppercase (`AUTHOR.`, `CHARACTER.`), stage directions in italics/brackets `(...)`, Arial 11pt styling.
   - **`dialogue` (Voice Transcriptions, Interviews, Chat Chronicles)**: Chronological calendar day headers (`📅 19 January`), stateful speaker attribution, color-coded speaker styling, metadata time tags (`[18:29] [Voice]:`).
   - **`academic` (Articles, Essays, Research Papers)**: Hierarchical H1/H2/H3 headings, double/1.5 line spacing, Times New Roman 12pt.
   - **`auto`**: Intelligent auto-detection of literature genre based on text syntax and line density.

2. **Stateful Speaker Attribution Engine**:
   - Maintains continuous speaker state tracking across joined message blocks in Telegram HTML exports (where consecutive messages omit explicit sender names).
   - Accurately maps profiles using custom `--speaker-map` with zero attribution loss.

3. **8-Stage Publishing Audit & Cleanup Pipeline**:
   - **Orthography Audit**: Hyphenated particles (`-то`, `-нибудь`, `всё-таки`, `из-за`), separate spelling of introductory phrases.
   - **Punctuation Audit**: Russian guillemets (`«...»`), em-dashes (` — `), conjunction comma placement.
   - **Syntax & Stream-of-Consciousness Restructuring**: Splits unpunctuated continuous oral speech into clear, grammatically complete sentences.
   - **Brand & Proper Name Protection**: White-list protection for technical terms, audio gear, and software (*Telegram, Windows, Apple, iPad, iPhone, YouTube, Audient, Yamaha, Edifier, LitRes, Spotify, Deezer, XLR*).
   - **STT Noise & Hallucination Purger**: Eliminates Whisper hallucinations (*Quiz河, quero..., göra, sings, DimaTorzok*), removes UI artifacts (*"Send.", "Screen reader..."*), corrects phonetic STT glitches (*"пахевизм" → "пофигизм"*).
   - **Terminal Cut-off Control (`check_cuts`)**: Prevents sentences from abruptly ending on conjunctions/prepositions.
   - **Gender Agreement**: Validates past-tense verb endings per speaker gender.

4. **1000+ Automated Scenario Test Suite**:
   - Full test coverage included in `tests/test_universal_pipeline.py`.

---

### Project Architecture

```
Vox2Book/
├── README.md                          # Trilingual documentation
├── requirements.txt                   # Dependencies (python-docx, beautifulsoup4)
├── config.py                          # Global configuration, genre presets, white-lists
├── run_pipeline.py                    # Main CLI & API entry point
├── pipeline/                          # Core engine package
│   ├── engine.py                      # Master Orchestration Pipeline
│   ├── extractors/                    # Multi-format Input Extractors
│   │   ├── auto_extractor.py          # Auto-detects input file formats
│   │   ├── telegram_html.py           # Messenger HTML export parser
│   │   └── text_reader.py             # Plain Text, Markdown & Book parser
│   ├── cleaners/                      # Spam & Noise Purification
│   ├── editors/                       # Genre Literary Editors & Typography
│   │   ├── prose_editor.py            # Fiction & Prose Processor
│   │   ├── poetry_editor.py           # Verse & Stanza Processor
│   │   ├── drama_editor.py            # Play & Script Processor
│   │   └── typography.py              # Russian Typography Engine
│   ├── validators/                    # Quality & Cut-off Auditors
│   │   └── quality_validator.py       # Sentence integrity & check_cuts
│   └── builders/                      # Layout Generators
│       └── docx_builder.py            # Multi-genre DOCX Builder
└── tests/                             # Automated Test Suite
    └── test_universal_pipeline.py
```

---

### Installation & Usage

#### 1. Installation
```bash
git clone https://github.com/kir-spec/Vox2Book.git
cd Vox2Book
pip install -r requirements.txt
```

#### 2. CLI Execution Examples

- **Process a Book / Novel (Prose Mode)**:
  ```bash
  python run_pipeline.py --input "novel.txt" --genre prose --title "My Novel" --output "output/novel.docx"
  ```

- **Process a Poetry Collection (Poetry Mode)**:
  ```bash
  python run_pipeline.py --input "poems.txt" --genre poetry --title "Selected Poems" --output "output/poems.docx"
  ```

- **Process a Play / Script (Drama Mode)**:
  ```bash
  python run_pipeline.py --input "script.txt" --genre drama --title "Three-Act Play" --output "output/play.docx"
  ```

- **Process Messenger & STT Dialogue Chronicles**:
  ```bash
  python run_pipeline.py --input "chat_export/" --genre dialogue --title "Oral Chronicle" --output "output/dialogues.docx"
  ```

#### 3. Run Automated Unit Tests
```bash
python -m unittest discover -s tests
```

</details>

---

## 2. Русскоязычная документация

<details>
<summary><b>📖 Нажмите для разворота русской документации (Развернуть / Свернуть)</b></summary>

<br>

### Обзор проекта

**Vox2Book** — профессиональный программный комплекс и универсальный литературно-издательский конвейер на языке Python. Движок предназначен для автоматической обработки, вычистки, типографики, аудита качества и генерации готовых печатных макетов книг в формате **DOCX**.

**Vox2Book** одинаково успешно работает с надиктованными голосовыми расшифровками (Speech-to-Text), логами мессенджеров (Telegram HTML), художественной прозой, поэзией, драматургией и академическими статьями.

---

### Архитектурные возможности ядра

1. **Многожанровая обработка литературы (`--genre`)**:
   - **`prose` (Проза, романы, повествования)**: автоматическое выявление глав (`Глава 1`, `Часть I`), оформление диалогов с тире (`—`), абзацные отступы 18pt, гарнитура *Times New Roman 12pt*.
   - **`poetry` (Поэзия, сборники стихотворений)**: сохранение строф, стихотворного размера, рифмовки, левый отступ строф 36pt, гарнитура *Georgia 11.5pt* без межстрочных разрывов.
   - **`drama` (Драматургия, пьесы, сценарии)**: имена персонажей прописными жирными буквами (`АВТОР.`, `ПЕРСОНАЖ.`), ремарки в скобках курсивом `(...)`, гарнитура *Arial 11pt*.
   - **`dialogue` (Устные транскрибации, диалоги, интервью)**: хронологические метки дат (`📅 19 января`), привязка авторов, цветовое разделение спикеров, метаданные времени (`[18:29] [Голосовое]:`).
   - **`academic` (Статьи, эссе, научные работы)**: иерархические заголовки H1/H2/H3, межстрочный интервал 1.5, *Times New Roman 12pt*.
   - **`auto`**: интеллектуальное автоопределение жанра на основе структуры текста.

2. **Сквозное отслеживание состояния спикеров (`Stateful Tracking`)**:
   - Корректная обработка объединённых (`joined`) сообщений в экспортах Telegram HTML (где у последовательных сообщений одного автора отсутствует явный заголовок имени).
   - Точная гибкая привязка профилей с помощью параметра `--speaker-map` без потери данных.

3. **Обязательный 8-этапный издательский аудит**:
   - **Орфография**: дефисное написание частиц (`-то`, `-нибудь`, `всё-таки`, `из-за`), раздельное написание вводных слов (`в общем`, `то есть`, `вряд ли`).
   - **Типографика**: кавычки-ёлочки (`«...»`), длинное тире (` — `), коррекция знаков препинания.
   - **Синтаксис монологов**: разбор сплошного устного потока речи без точек на законченные предложения.
   - **Белые списки брендов и имён**: защита технических терминов и брендов (*Telegram, Windows, Apple, iPad, iPhone, YouTube, Audient, Yamaha, Edifier, LitRes, Spotify, Deezer, XLR*).
   - **Очистка шумов STT и галлюцинаций**: удаление артефактов Whisper (*Quiz河, quero..., göra, sings, DimaTorzok*), удаление дикторских меток (*"Отправить.", "Экранный диктор..."*), коррекция опечаток STT (*"пахевизм" → "пофигизм"*).
   - **Контроль обрывов фраз (`check_cuts`)**: пресечение обрывов предложений на союзах и предлогах.
   - **Гендерное согласование**: проверка окончаний глаголов прошедшего времени по полу спикера.

---

### Варианты запуска

#### 1. Установка
```bash
git clone https://github.com/kir-spec/Vox2Book.git
cd Vox2Book
pip install -r requirements.txt
```

#### 2. Команды запуска

- **Обработка книги / романов (Проза)**:
  ```bash
  python run_pipeline.py --input "роман.txt" --genre prose --title "Мой Роман" --output "output/роман.docx"
  ```

- **Обработка поэтического сборника (Поэзия)**:
  ```bash
  python run_pipeline.py --input "стихи.txt" --genre poetry --title "Сборник стихов" --output "output/стихи.docx"
  ```

- **Обработка пьесы (Драматургия)**:
  ```bash
  python run_pipeline.py --input "пьеса.txt" --genre drama --title "Пьеса" --output "output/пьеса.docx"
  ```

- **Обработка хроник мессенджеров и транскрибаций**:
  ```bash
  python run_pipeline.py --input "чат_экспорт/" --genre dialogue --title "Устная хроника" --output "output/диалоги.docx"
  ```

#### 3. Запуск автоматических тестов
```bash
python -m unittest discover -s tests
```

</details>

---

## 3. Українськомовна документація

<details>
<summary><b>📖 Натисніть для розгортання української документації (Розгорнути / Згорнути)</b></summary>

<br>

### Огляд проєкту

**Vox2Book** — професійний програмний комплекс та універсальний літературно-видавничий конвеєр мовою Python. Двигун призначений для автоматичної обробки, вичитки, типографіки, аудиту якості та генерації готових друкованих макетів книг у форматі **DOCX**.

**Vox2Book** одинаково успішно працює з надиктованими голосовими розшифровками (Speech-to-Text), логами месенджерів (Telegram HTML), художньою прозою, поезією, драматургією та академічними статтями.

---

### Архітектурні можливості ядра

1. **Багатожанрова обробка літератури (`--genre`)**:
   - **`prose` (Проза, романи, повісті)**: автоматичне виявлення розділів (`Глава 1`, `Частина I`), оформлення діалогів із тире (`—`), абзацні відступи 18pt, гарнітура *Times New Roman 12pt*.
   - **`poetry` (Поезія, збірки віршів)**: збереження строф, віршованого розміру, римування, лівий відступ строф 36pt, гарнітура *Georgia 11.5pt* без міжрядкових розривів.
   - **`drama` (Драматургія, п'єси, сценарії)**: імена персонажів великими жирними літерами (`АВТОР.`, `ПЕРСОНАЖ.`), ремарки в дужках курсивом `(...)`, гарнітура *Arial 11pt*.
   - **`dialogue` (Усні транскрипції, діалоги, інтерв'ю)**: хронологічні позначки дат (`📅 19 січня`), прив'язка авторів, колірний поділ спікерів, метадані часу (`[18:29] [Голосовое]:`).
   - **`academic` (Статті, есе, наукові праці)**: ієрархічні заголовки H1/H2/H3, міжрядковий інтервал 1.5, *Times New Roman 12pt*.
   - **`auto`**: інтелектуальне автовизначення жанру на основі структури тексту.

2. **Наскрізне відстеження стану спікерів (`Stateful Tracking`)**:
   - Коректна обробка об'єднаних (`joined`) повідомлень в експортах Telegram HTML (де у послідовних повідомленнях одного автора відсутній явлений заголовок імені).
   - Точна прив'язка профілів за допомогою параметра `--speaker-map` із нульовою втратою даних.

3. **Обов'язковий 8-етапний видавничий аудит**:
   - **Орфографія**: дефісне написання часток (`-то`, `-небудь`, `все-таки`, `з-за`), роздільне написання вступних слів.
   - **Типографіка**: лапки-ялинки (`«...»`), довге тире (` — `), корекція розділових знаків.
   - **Синтаксис монологів**: розбір суцільного усного потоку мовлення без крапок на закінчені пропозиції.
   - **Білі списки брендів та імен**: захист технічних термінів та брендів (*Telegram, Windows, Apple, iPad, iPhone, YouTube, Audient, Yamaha, Edifier, LitRes, Spotify, Deezer, XLR*).
   - **Очищення шумів STT та галюцинацій**: видалення артефактів Whisper (*Quiz河, quero..., göra, sings, DimaTorzok*), видалення дикторських позначок (*"Отправить.", "Экранный диктор..."*), корекція помилок STT.
   - **Контроль обривів фраз (`check_cuts`)**: припинення обривів речень на сполучниках і прийменниках.
   - **Гендерне узгодження**: перевірка закінчень дієслів минулого часу за статтю спікера.

---

### Варианти запуску

#### 1. Встановлення
```bash
git clone https://github.com/kir-spec/Vox2Book.git
cd Vox2Book
pip install -r requirements.txt
```

#### 2. Команди запуску

- **Обробка книги / романів (Проза)**:
  ```bash
  python run_pipeline.py --input "роман.txt" --genre prose --title "Мій Роман" --output "output/роман.docx"
  ```

- **Обробка поетичної збірки (Поезія)**:
  ```bash
  python run_pipeline.py --input "вірші.txt" --genre poetry --title "Збірка віршів" --output "output/вірші.docx"
  ```

- **Обробка п'єси (Драматургія)**:
  ```bash
  python run_pipeline.py --input "п'єса.txt" --genre drama --title "П'єса" --output "output/п'єса.docx"
  ```

- **Обробка хронік месенджерів та транскрипцій**:
  ```bash
  python run_pipeline.py --input "чат_експорт/" --genre dialogue --title "Усна хроніка" --output "output/діалоги.docx"
  ```

#### 3. Запуск автоматичних тестів
```bash
python -m unittest discover -s tests
```

</details>

---

## 📄 License & Author

- **Author**: [kir-spec](https://github.com/kir-spec)
- **License**: MIT License. Open-source & free to use for literary and publishing projects.
