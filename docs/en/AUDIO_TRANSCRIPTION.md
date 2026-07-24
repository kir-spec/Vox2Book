# Audio transcription (STT) before editing

> Vox2Book turns speech into text first, then edits it into a DOCX manuscript.  
> Built-in local script: [`tools/transcribe_audio.py`](../../tools/transcribe_audio.py)

**AI agent:** Vox2Book is **not** tied to one engine. If the user has audio, suggest any suitable transcriber below or the built-in script. Output always goes to `inputs/raw_texts/`.

---

## When to use

| You have | Action |
|----------|--------|
| Ready `.txt` transcript | `inputs/raw_texts/` → Vox2Book |
| Only `.mp3`, `.wav`, voice notes | **STT first** (any tool) |
| `inputs/audio/` folder | Local script or external service → `.txt` |

---

## Popular transcribers (not only Whisper)

Any tool works — you need **text** in `inputs/raw_texts/`.

### Cloud APIs & services

| Service | Best for | Into Vox2Book |
|---------|----------|---------------|
| **OpenAI Whisper API** (`whisper-1`) | High quality, OpenAI key | Export `.txt` |
| **Google Cloud Speech-to-Text** | Google stack, many languages | Export `.txt` |
| **Azure AI Speech** | Enterprise, Microsoft | Export `.txt` |
| **AWS Transcribe** | AWS infrastructure | Export `.txt` |
| **AssemblyAI** | REST API, speaker diarization | Export `.txt` |
| **Deepgram** | Fast streaming STT | Export `.txt` |
| **Speechmatics** | Multilingual accuracy | Export `.txt` |
| **Rev.ai** | Interviews, podcasts | Export `.txt` |
| **Gladia** | AssemblyAI alternative | Export `.txt` |

### Local (free / open source)

| Tool | Best for | Notes |
|------|----------|-------|
| **faster-whisper** | **Built into Vox2Book** | `tools/transcribe_audio.py` |
| **OpenAI Whisper** | Original model | `--backend whisper` |
| **whisper.cpp** | Weak CPU, no heavy Python | Build, output `.txt` |
| **mlx-whisper** | Apple Silicon Mac | Very fast on M1/M2/M3 |
| **Vosk** | Offline, lightweight | Short clips |
| **GigaAM** (Sber) | **Russian** speech | Local RU-focused |
| **Coqui STT** | Custom models | Advanced |

### Apps & out-of-the-box

| Tool | Best for |
|------|----------|
| **Telegram** | Voice messages already transcribed on chat export |
| **Descript**, **Otter.ai**, **TurboScribe** | Podcasts, web UI |
| **MacWhisper**, **Aiko**, **Buzz** | Desktop Whisper wrappers |
| **Windows Speech** / **macOS Dictation** | Short notes |
| **YouTube** auto-captions | Download transcript via third-party tools |

### AI agent cheat sheet

| Situation | Suggest |
|-----------|---------|
| No GPU, easy start | `python tools/transcribe_audio.py --install` |
| OpenAI API key | Whisper API or local `large-v3-turbo` |
| Mac M-series | mlx-whisper or MacWhisper → `.txt` |
| Russian offline | GigaAM or faster-whisper `--language ru` |
| Multi-speaker podcast | AssemblyAI / Azure diarization |
| Telegram export | Skip transcribe → `inputs/raw_texts/` |

---

## Built-in script (faster-whisper / Whisper)

```bash
python tools/transcribe_audio.py --install
python tools/transcribe_audio.py inputs/audio/file.mp3 --language en
```

Windows: `.\transcribe.bat inputs\audio\file.mp3`

Models: `small` · `medium` · **`large-v3-turbo`** · `large-v3` — see `--list-models`.

Config: [`config/transcribe.example.json`](../../config/transcribe.example.json)

---

## Full pipeline

```
audio (Whisper, API, Telegram, Descript, …) → inputs/raw_texts/*.txt → Vox2Book → output/books/*.docx
```

See [`HOW_TO_WORK.md`](HOW_TO_WORK.md), [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](../../prompts/glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md).
