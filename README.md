# 📚 Vox2Book — Universal Literature Processing & Publishing Engine

[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-v2.5.0-green.svg)](https://github.com/kir-spec/Vox2Book/releases)

Vox2Book — это универсальный издательский комплекс нового поколения, созданный на **Rust** и интегрированный с **нейросетевыми промптами (LLM Master Prompts)** для превращения сырых устных расшифровок аудиозаписей (Whisper STT) и обычных текстов в вычитанные книги и печатные макеты в формате **DOCX**.

⚖️ **В чём разница между использованием «Просто Промпта» и Проектом Vox2Book?**: [docs/PROJECT_VS_PROMPT.md](docs/PROJECT_VS_PROMPT.md)  
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
├── config.json                  # 🔑 Настройка ключей API (OpenAI, DeepSeek, Claude, LM Studio, Ollama)
├── run_api_pipeline.py          # 🚀 Быстрый запуск вычистки через API
└── vox2book.exe                 # 🚀 Исполняемый графический и CLI файл проекта
```

---

<details>
<summary><strong>⚖️ В чём разница между «Просто Промптом» и Проектом Vox2Book?</strong></summary>

- **Просто Промпт в чате**: Выдает сырой текст в окне браузера. Вам нужно вручную копировать его, вставлять в Word, настраивать шрифты, отступы и исправлять кавычки. Большие книги нейросеть обрезает из-за лимита длины.
- **Проект Vox2Book**: Автоматически считывает любые файлы/папки, вычитывает через нейросети (LM Studio, Ollama, OpenAI, DeepSeek, Claude), выполняет книжную типографику (`«...»`, ` — `) и мгновенно создает готовый макет книги Word (`.docx`).

</details>

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

### Why Vox2Book vs Just a Prompt?
Read our detailed comparison guide: [docs/PROJECT_VS_PROMPT.md](docs/PROJECT_VS_PROMPT.md).
Vox2Book automates multi-encoding file reading, context streaming, typography cleanup (`«...»`, ` — `), and Word XML layout compilation into finished `.docx` book manuscripts.

</details>
