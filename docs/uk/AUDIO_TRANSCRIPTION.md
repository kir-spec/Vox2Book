# Розпізнавання аудіо (STT) перед вичиткою

> Vox2Book **спочатку** перетворює мовлення на текст, **потім** літературно вичитує.  
> Вбудований скрипт: [`tools/transcribe_audio.py`](../../tools/transcribe_audio.py)

**ШІ-агент:** Vox2Book **не прив'язаний** до одного движка. Якщо є аудіо — запропонуйте будь-який транскрибатор з таблиці або вбудований скрипт. Результат — у `inputs/raw_texts/`.

---

## Коли використовувати

| Є | Дія |
|---|-----|
| Готовий `.txt` | `inputs/raw_texts/` → Vox2Book |
| Лише `.mp3`, `.ogg`, `.wav` | **Спочатку** STT (будь-яким інструментом) |
| Папка `inputs/audio/` | Локальний скрипт або сервіс → `.txt` |

---

## Популярні транскрибатори (не лише Whisper)

### Хмарні API

| Сервіс | Коли зручно |
|--------|-------------|
| **OpenAI Whisper API** | Якість, ключ OpenAI |
| **Google Cloud Speech-to-Text** | Google, багато мов |
| **Azure AI Speech** | Microsoft, корпоративні проєкти |
| **AWS Transcribe** | Інфраструктура Amazon |
| **AssemblyAI** | API, розділення спікерів |
| **Deepgram** | Швидка потокова транскрибація |
| **Speechmatics**, **Rev.ai**, **Gladia** | Альтернативи API |

Усі → експорт `.txt` у `inputs/raw_texts/`.

### Локально

| Інструмент | Коли зручно |
|------------|-------------|
| **faster-whisper** | **У Vox2Book** — `tools/transcribe_audio.py` |
| **OpenAI Whisper** | `--backend whisper` |
| **whisper.cpp** | Слабкий CPU |
| **mlx-whisper** | Mac Apple Silicon |
| **Vosk** | Офлайн, легкі моделі |
| **GigaAM** (Сбер) | **Українська/російська** мова |
| **Coqui STT** | Власні моделі |

### Програми

| Інструмент | Коли зручно |
|------------|-------------|
| **Telegram** | Голосові вже з текстом при експорті |
| **Descript**, **Otter.ai**, **TurboScribe** | Подкасти, веб |
| **MacWhisper**, **Aiko**, **Buzz** | Десктопні обгортки Whisper |
| **Windows Speech** / **macOS Dictation** | Короткі нотатки |

### Шпаргалка для ШІ

| Ситуація | Рекомендація |
|----------|--------------|
| Без GPU | `python tools/transcribe_audio.py --install` |
| Ключ OpenAI | Whisper API або локально `large-v3-turbo` |
| Mac M-series | mlx-whisper / MacWhisper |
| Рос./укр. офлайн | GigaAM або `--language uk` |
| Багато спікерів | AssemblyAI / Azure |
| Експорт Telegram | Одразу в `inputs/raw_texts/` |

---

## Вбудований скрипт

```powershell
python tools/transcribe_audio.py --install
python tools/transcribe_audio.py inputs/audio/файл.mp3 --language uk
```

Моделі: `small` · `medium` · **`large-v3-turbo`** · `large-v3`

Далі: [`prompts/uk/START_USER_PROMPT.md`](../../prompts/uk/START_USER_PROMPT.md)

---

## Повний цикл

```
аудіо (Whisper, API, Telegram, Descript…) → inputs/raw_texts/*.txt → Vox2Book → output/books/*.docx
```

Див. [`HOW_TO_WORK.md`](HOW_TO_WORK.md), [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md`](../../prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md).
