# 📖 Полное руководство пользователя Vox2Book v2.4.0

Добро пожаловать в универсальный издательский комплекс **Vox2Book**!
Программа объединяет **нейросетевой ИИ-модуль вычистки устной речи (LLM)** и **высокоскоростной верстальщик печатных макетов Word (.docx)**.

---

## 🖥️ 1. Работа с локальной нейросетью LM Studio (100% Оффлайн и Бесплатно)
**LM Studio** — одна из самых популярных программ для Windows для запуска любых нейросетей (Llama 3, Saiga, Qwen, Mistral).

1. Скачайте и запустите [LM Studio](https://lmstudio.ai).
2. Загрузите любую русскую модель (например, `saiga_llama3` или `llama-3-8b`).
3. В LM Studio перейдите на вкладку **`Developer / Local Server`** и нажмите **`Start Server`** (сервер запустится на `http://localhost:1234`).
4. Запустите `vox2book.exe` — выберите кнопку **«🖥️ LM Studio (Локально)»** и нажмите **«🚀 ВЫЧИТАТЬ ЧЕРЕЗ API»**. Vox2Book автоматически отправит монолог в LM Studio и сформирует макет книги!

---

## 🤖 2. Работа с локальной нейросетью Ollama AI (Оффлайн)
1. Установите [Ollama.com](https://ollama.com).
2. Запустите модель в консоли: `ollama run llama3`.
3. В `vox2book.exe` выберите **«🤖 Ollama (Локально)»**. Программа подключится к `http://localhost:11434`.

---

## ☁️ 3. Работа с Облачными API (OpenAI, DeepSeek, Anthropic Claude)
1. В окне `vox2book.exe` или файле `config.json` выберите провайдера:
   - **OpenAI (GPT-4o)**: `api_provider`: `"openai"`.
   - **DeepSeek API**: `api_provider`: `"deepseek"`.
   - **Anthropic Claude**: `api_provider`: `"anthropic"`.
2. Вставьте ваш `api_key` в поле ввода или в `config.json`.

---

## 📂 4. Структура папок проекта

```ascii
E:\coding\работа с литературой\
├── inputs/
│   ├── raw_texts/               # Исходные файлы для вычистки (.txt, .md, .docx)
│   └── audio/                   # Аудиозаписи для транскрипции (.ogg, .mp3, .wav)
├── output/
│   └── books/                   # Готовые макеты книг (.docx)
├── config.json                  # Настройки API (OpenAI, DeepSeek, Claude, LM Studio, Ollama)
├── run_api_pipeline.py          # Скрипт быстрой обработки через API
└── vox2book.exe                 # Исполняемый графический и CLI файл
```
