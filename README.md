# 📚 Vox2Book — Universal Literature Processing & Publishing Engine

[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v2.2.0-green.svg)](https://github.com/kir-spec/Vox2Book/releases)

Vox2Book — это универсальный издательский комплекс нового поколения, созданный на **Rust** и интегрированный с **нейросетевыми промптами (LLM Master Prompts)** для превращения сырых устных расшифровок аудиозаписей (Whisper STT) и обычных текстов в вычитанные книги и печатные макеты в формате **DOCX**.

📂 **Структура проекта и руководство по работе в IDE (Antigravity / Cursor / VS Code)**: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)  
📖 **Подробное руководство пользователя по всем режимам**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

---

## 📂 Структура папок проекта

```ascii
E:\coding\работа с литературой\
├── inputs/                      # 📥 ВСЕ ВХОДНЫЕ МАТЕРИАЛЫ
│   ├── raw_texts/               # Исходные текстовые файлы (.txt, .md, .docx, .html)
│   └── audio/                   # Сырые аудиозаписи (.ogg, .wav, .mp3, .m4a) для расшифровки
│
├── output/                      # 📤 ГОТОВАЯ ПРОДУКЦИЯ ДЛЯ ПЕЧАТИ
│   └── books/                   # Готовые вычитанные книги в формате Word (.docx)
│
├── prompts/                     # 🧠 ИИ-ПРОМПТЫ И ОБУЧАЮЩИЕ ИНСТРУКЦИИ
│   └── MASTER_LLM_PROMPT.md    # Мастер-промпт главного редактора для нейросетей
│
├── config.json                  # 🔑 Настройка ключей API (OpenAI, DeepSeek, Claude, Ollama)
├── run_api_pipeline.py          # 🚀 Быстрый запуск вычистки через API
└── vox2book.exe                 # 🚀 Исполняемый графический и CLI файл проекта
```

---

<details>
<summary><strong>🇷🇺 Инструкция по открытию проекта в IDE (Antigravity / Cursor / VS Code)</strong></summary>

Для работы с проектом и ИИ-ассистентами:
1. Откройте **Antigravity IDE**, **Cursor** или **VS Code**.
2. Откройте папку проекта через `File` → `Open Folder...` →Выберите `E:\coding\работа с литературой`.
3. Поместите файлы для вычистки в `inputs/raw_texts/`.
4. Запустите обработку через `python run_api_pipeline.py` или окно `vox2book.exe`.
5. Готовые вычитанные макеты DOCX появятся в папке `output/books/`.

</details>

---

<details>
<summary><strong>🇬🇧 English Documentation</strong></summary>

### Workspace Setup (Antigravity IDE / Cursor / VS Code)
1. Open your IDE and select `File` -> `Open Folder...` -> `E:\coding\работа с литературой`.
2. Put input text files into `inputs/raw_texts/` and audio into `inputs/audio/`.
3. Configure `config.json` with your preferred AI provider (`openai`, `deepseek`, `anthropic`, `ollama`).
4. Run `python run_api_pipeline.py` or launch `vox2book.exe`. Output manuscripts are saved in `output/books/`.

</details>

---

<details>
<summary><strong>🇺🇦 Українська документація</strong></summary>

### Налаштування середовища (Antigravity IDE / Cursor / VS Code)
1. Відкрийте папку проекту `E:\coding\работа с литературой` в IDE.
2. Покладіть вхідні файли у папку `inputs/raw_texts/`.
3. Налаштуйте `config.json` та запустіть `python run_api_pipeline.py` або `vox2book.exe`.
4. Готові макети книг збережуться у папці `output/books/`.

</details>
