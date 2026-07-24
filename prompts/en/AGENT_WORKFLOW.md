# AI agent workflow (universal)

User start: [`START_USER_PROMPT.md`](START_USER_PROMPT.md)  
System prompt: [`UNIVERSAL_EDITOR_SYSTEM.md`](UNIVERSAL_EDITOR_SYSTEM.md)

---

## Phase 0 — Orientation

1. Project root: `AGENTS.md`, `inputs/`, `output/`.
2. Brief guide from `docs/en/HOW_TO_WORK.md`.
3. List `inputs/raw_texts/` **and** `inputs/audio/`.
4. **If user has only audio** (`.mp3`, `.wav`, `inputs/audio/`):
   - Vox2Book edits **text**, not audio.
   - Suggest STT: built-in `tools/transcribe_audio.py` **or** OpenAI API, AssemblyAI, Deepgram, Telegram export, Descript, MacWhisper, GigaAM… (`docs/en/AUDIO_TRANSCRIPTION.md`).
   - Continue with `inputs/raw_texts/` after transcription.
5. Text type → optional profile in `profiles/`.

---

## Phase 1 — Read source

UTF-8 → cp1251 fallback. Note genre, register, speakers, damaged STT.

---

## Phase 2 — Questions

Unless user said “proceed”: style mode, title, glossary, profanity, scope, ambiguous STT spans.

---

## Phase 3 — Processing

Hygiene → reconstruction → profile → typography → 8 audits (`docs/en/TECHNICAL_SPECIFICATION.md`) → `output/books/`.

---

## Phase 4 — Report

DOCX path, fixes, open questions.

---

## Language

English (this folder `prompts/en/`).
