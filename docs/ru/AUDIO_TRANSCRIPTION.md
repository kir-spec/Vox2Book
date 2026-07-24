# Распознавание аудио (STT) перед вычиткой

> Vox2Book **сначала** превращает речь в текст, **затем** литературно вычитывает его.  
> Встроенный скрипт (локальный Whisper): [`tools/transcribe_audio.py`](../../tools/transcribe_audio.py)

**ИИ-агент:** Vox2Book не привязан к одному движку. Если у пользователя аудио — предложите **любой** подходящий транскрибатор из таблицы ниже или встроенный скрипт. Результат всегда кладётся в `inputs/raw_texts/`.

---

## Когда использовать

| У вас есть | Действие |
|------------|----------|
| Уже готовый `.txt` / расшифровка | Сразу в `inputs/raw_texts/` → промпт Vox2Book |
| Только `.mp3`, `.ogg`, `.wav`, голосовые | **Сначала** STT (любым инструментом) |
| Папка `inputs/audio/` | Локальный скрипт или внешний сервис → `.txt` |

---

## Популярные транскрибаторы (не только Whisper)

Любой из них подходит: главное — получить **текст** и положить в `inputs/raw_texts/`.

### Облачные API и сервисы

| Сервис | Когда удобен | Как попасть в Vox2Book |
|--------|--------------|------------------------|
| **OpenAI Whisper API** (`whisper-1`) | Высокое качество, уже есть ключ OpenAI | Экспорт `.txt` → `inputs/raw_texts/` |
| **Google Cloud Speech-to-Text** | Google-экосистема, много языков | То же |
| **Azure AI Speech** | Корпоративные проекты, Microsoft | То же |
| **AWS Transcribe** | Инфраструктура Amazon | То же |
| **AssemblyAI** | Удобный REST API, диаризация спикеров | То же |
| **Deepgram** | Быстрая потоковая транскрибация | То же |
| **Speechmatics** | Точность на EU/мультиязычии | То же |
| **Rev.ai** | Интервью, подкасты | То же |
| **Gladia** | Альтернатива AssemblyAI | То же |

### Локально на ПК (бесплатно / open source)

| Инструмент | Когда удобен | Примечание |
|------------|--------------|------------|
| **faster-whisper** | **Встроен в Vox2Book** — `tools/transcribe_audio.py` | Рекомендуемый локальный вариант |
| **OpenAI Whisper** (оригинал) | `--backend whisper` в нашем скрипте | Медленнее faster-whisper |
| **whisper.cpp** | Слабый CPU, macOS/Linux без Python-тяжести | Скомпилировать, вывод в `.txt` |
| **mlx-whisper** | Mac с Apple Silicon (M1/M2/M3) | Очень быстро на Mac |
| **Vosk** | Офлайн, лёгкие модели, слабые машины | Хуже на длинных монологах |
| **GigaAM** (Сбер) | **Русский язык**, локально | Хорош для RU-речи |
| **Coqui STT** | Эксперименты, своё обучение | Для продвинутых |

### Готовые программы и «из коробки»

| Инструмент | Когда удобен |
|------------|--------------|
| **Telegram** | Голосовые уже с расшифровкой при экспорте чата |
| **Descript**, **Otter.ai**, **TurboScribe** | Подкасты, интервью, веб-интерфейс |
| **MacWhisper**, **Aiko**, **Buzz** | Десктоп-обёртки над Whisper на Mac/Win |
| **Яндекс.Браузер / Chrome** | Встроенная диктовка в поле ввода |
| **Windows Speech** / **macOS Dictation** | Короткие заметки |
| **YouTube** | Автосубтитры → скачать текст (сторонние утилиты) |
| **FFmpeg + любой STT** | Предобработка аудио перед распознаванием |

### Что предложить пользователю (шпаргалка для ИИ)

| Ситуация | Рекомендация |
|----------|--------------|
| Нет GPU, нужен простой старт | `python tools/transcribe_audio.py --install` |
| Есть ключ OpenAI | OpenAI Whisper API или наш `large-v3-turbo` локально |
| Только Mac M-series | mlx-whisper или MacWhisper → `.txt` |
| Чистый русский, офлайн | GigaAM или `faster-whisper` + `--language ru` |
| Много спикеров (подкаст) | AssemblyAI / Azure с diarization |
| Уже экспорт из Telegram | Сразу в `inputs/raw_texts/`, transcribe не нужен |

---

## Встроенный скрипт Vox2Book (faster-whisper / Whisper)

### 1. Установить зависимости (один раз)

```powershell
.\tools\install_transcribe.ps1
# или
python tools/transcribe_audio.py --install
```

### 2. Положить аудио в `inputs/audio/`

Форматы: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.opus`, `.flac`, `.webm`, `.mp4` и др.

### 3. Запустить

```powershell
.\transcribe.bat inputs\audio\ваш_файл.mp3
python tools/transcribe_audio.py inputs/audio/ --language ru
```

### 4. Вычитка

Транскрипт → **`inputs/raw_texts/имя.txt`** → [`prompts/ru/START_USER_PROMPT.md`](../../prompts/ru/START_USER_PROMPT.md).

---

## Выбор модели (локальный Whisper)

```powershell
python tools/transcribe_audio.py --list-models
```

| Модель | Когда брать |
|--------|-------------|
| `small` | Слабый ПК, без NVIDIA GPU |
| `medium` | CPU или средняя GPU |
| `large-v3` | Максимум качества |
| `large-v3-turbo` | **Рекомендуется** — баланс скорость/качество |
| `distil-large-v3` | Быстрее large |

---

## Настройки (`config/transcribe.json`)

Скопируйте [`config/transcribe.example.json`](../../config/transcribe.example.json).

| Поле | Смысл |
|------|--------|
| `backend` | `faster-whisper` или `whisper` |
| `language` | `ru`, `en`, `uk` |
| `initial_prompt` | Имена, термины — для любого Whisper-совместимого движка |
| `vad_filter` | Меньше галлюцинаций на тишине |

```powershell
python tools/transcribe_audio.py file.mp3 --prompt "Анфи, Kir, Telegram, USB, Python" --json
```

---

## Полный цикл «аудио → книга»

```
аудио (любой STT: Whisper, API, Telegram, Descript…)
    → текст в inputs/raw_texts/*.txt
    → промпт Vox2Book + ИИ
    → output/books/*.docx
```

См. [`HOW_TO_WORK.md`](HOW_TO_WORK.md), [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md`](../../prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md).
