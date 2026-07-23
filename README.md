# 📚 Vox2Book — Universal Literature Processing & Publishing Engine

[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v2.0.0-green.svg)](https://github.com/kir-spec/Vox2Book/releases)

Vox2Book — это специализированный измерительный и издательский комплекс нового поколения, созданный на **Rust** и интегрированный с **нейросетевыми промптами (LLM Master Prompts)** для превращения сырых устных расшифровок аудиозаписей (Whisper / Audio STT) и обычных текстов в полностью вычитанные, отредактированные книги и печатные макеты в формате **DOCX**.

---

<details>
<summary><strong>🇬🇧 English Documentation</strong></summary>

### Overview
Vox2Book is a high-performance publishing engine written in Rust that transforms raw voice transcripts (Whisper STT), plain text, Markdown, and HTML documents into beautifully formatted `.docx` manuscripts.

### Architecture
- **Neural Network LLM Engine**: Connects to Ollama (`localhost:11434`) or Cloud LLM APIs to perform deep literary editing, oral speech restructuring, term correction (e.g., *USB*, *SSD*, *Western Digital*), and filler word removal.
- **Rust Publishing Engine**: Handles multi-encoding decoding (UTF-8, Windows-1251/CP1251, UTF-8 BOM), typography (`«...»`, ` — `), and Word XML layout generation.

### Installation & Usage
1. Download `vox2book.exe` from [Releases](https://github.com/kir-spec/Vox2Book/releases).
2. Launch `vox2book.exe` (no console window will appear).
3. Drag & drop your text or audio transcript file and click **🚀 Build DOCX Manuscript**.
4. (Optional) Run `ollama run llama3` in the background for automatic 100% offline AI proofreading.

</details>

---

<details>
<summary><strong>🇷🇺 Русская документация</strong></summary>

### Описание
Vox2Book объединяет высокоскоростное макетирование на Rust с глубокой литературной вычисткой нейросетевыми алгоритмами.

### Принцип работы
1. **Нейросетевой модуль вычистки (LLM)**: Подключается к Ollama (`localhost:11434`) или внешним API, автоматически разбивает сплошной монолог на абзацы и предложения, убирает заикания, слова-паразиты и исправляет технический сленг диктофона (`"те из бы"` → `USB`, `"в стране джетал"` → `Western Digital`, `"35 размер"` → `3.5"`).
2. **Оффлайн-издательский движок (Rust)**: Работает со всеми кодировками (UTF-8, Windows-1251, BOM), выполняет профессиональную типографику и генерирует печатный макет в формате Word `.docx`.

### Быстрый запуск
- Скачайте `vox2book.exe` из раздела [Releases](https://github.com/kir-spec/Vox2Book/releases).
- Запустите программу двойным кликом (без вызова черного окна консоли).
- Загрузите текстовый файл или папку мышкой и нажмите **🚀 ВЫЧИТАТЬ ТЕКСТ И СФОРМИРОВАТЬ МАКЕТ DOCX**.

</details>

---

<details>
<summary><strong>🇺🇦 Українська документація</strong></summary>

### Опис
Vox2Book — це універсальний видавничий комплекс на Rust для автоматичного перетворення сирих аудіо-розшифровок та текстів у повністю відредаговані книжкові макети DOCX.

### Архітектура
- **Нейромережевий модуль (LLM)**: Підключається до Ollama (`localhost:11434`) для літературного вичитування, розбиття на речення та виправлення термінів.
- **Видавничий рушій (Rust)**: Виконує типографіку, обробку кодувань (UTF-8, Windows-1251) та генерацію макетів Word.

</details>

---

## 🛠️ Build & Test
```powershell
cargo test
cargo build --release
```
