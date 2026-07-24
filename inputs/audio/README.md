# Аудио для транскрибации

Положите сюда `.mp3`, `.wav`, `.ogg`, `.m4a`, `.opus`, `.flac` и т.п.

## Вариант 1 — встроенный скрипт (Whisper / faster-whisper)

```powershell
python tools/transcribe_audio.py --install
python tools/transcribe_audio.py inputs/audio/
```

## Вариант 2 — любой другой транскрибатор

OpenAI Whisper API · Google / Azure / AWS STT · AssemblyAI · Deepgram ·  
Telegram (экспорт чата) · Descript · Otter.ai · MacWhisper · GigaAM · Vosk · mlx-whisper …

Результат — **текст** в `inputs/raw_texts/`, дальше обычный Vox2Book.

Полный список: [`docs/ru/AUDIO_TRANSCRIPTION.md`](../docs/ru/AUDIO_TRANSCRIPTION.md)
