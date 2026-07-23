# 📚 Vox2Book — Universal Literature Processing & Publishing Engine

[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v2.1.0-green.svg)](https://github.com/kir-spec/Vox2Book/releases)

Vox2Book — это универсальный издательский комплекс нового поколения, созданный на **Rust** и интегрированный с **нейросетевыми промптами (LLM Master Prompts)** для превращения сырых устных расшифровок аудиозаписей (Whisper STT) и обычных текстов в вычитанные книги и печатные макеты в формате **DOCX**.

📖 **Подробное руководство пользователя по всем режимам работы**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

---

<details>
<summary><strong>🇬🇧 English Documentation</strong></summary>

### Overview & Workflow Options
Vox2Book offers 5 flexible workflow modes:

1. **Standalone Window GUI (`vox2book.exe`)**: Drag & drop your text or transcript file for instant single-click processing into DOCX.
2. **Local Free Offline AI (Ollama)**: Run `ollama run llama3` on your PC for 100% private offline AI proofreading.
3. **Cloud AI (ChatGPT / Claude / Gemini)**: Use our Master Prompt [`prompts/MASTER_LLM_PROMPT.md`](prompts/MASTER_LLM_PROMPT.md) in any web or API LLM interface, then format with `vox2book.exe`.
4. **Instant Offline Engine (Rust)**: High-speed 0.1-second typography and rule-based cleanup.
5. **CLI Batch Mode**: Command-line batch execution via `vox2book.exe -i file.txt -o book.docx`.

</details>

---

<details>
<summary><strong>🇷🇺 Русская документация</strong></summary>

### Варианты использования Vox2Book

1. **Графическое окно (`vox2book.exe`)**: Запуск приложения без вызова консоли, с поддержкой Drag-and-Drop и выбором файлов.
2. **Бесплатная локальная Нейросеть (Ollama AI)**: Запустите `ollama run llama3` на компьютере для бесплатной оффлайн-вычистки текста нейросетью без интернета.
3. **Облачные Нейросети (ChatGPT / Claude / Gemini)**: Скопируйте готовый мастер-промпт [`prompts/MASTER_LLM_PROMPT.md`](prompts/MASTER_LLM_PROMPT.md) в веб-версию любой нейросети, а затем сформируйте макет DOCX в `vox2book.exe`.
4. **Мгновенный автономный движок (Rust)**: Выполнение типографики, расшифровки технического сленга диктофона (`USB`, `SSD`, `Western Digital`, `ADATA`) и стилей Word за 0.1 секунды.
5. **Автоматизация через CLI**: Пакетная обработка файлов командой `vox2book.exe -i input.txt -o book.docx`.

</details>

---

<details>
<summary><strong>🇺🇦 Українська документація</strong></summary>

### Режими роботи Vox2Book

1. **Графічний віконний інтерфейс (`vox2book.exe`)**: Перетягніть файл у вікно програми для створення макета DOCX.
2. **Локальна Нейромережа (Ollama AI)**: Використовуйте `ollama run llama3` для повністю оффлайн AI-вичитування.
3. **Хмарні Нейромережі (ChatGPT / Claude)**: Використовуйте майстер-промпт [`prompts/MASTER_LLM_PROMPT.md`](prompts/MASTER_LLM_PROMPT.md).
4. **Автономний рушій Rust**: Миттєва обробка типографіки та стилів Word.

</details>
