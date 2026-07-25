# AI agent workflow (universal)

User start: [`START_USER_PROMPT.md`](START_USER_PROMPT.md)  
System prompt: [`UNIVERSAL_EDITOR_SYSTEM.md`](UNIVERSAL_EDITOR_SYSTEM.md)

---

## Phase 0 — Orientation

1. Project root: `AGENTS.md`, `inputs/`, `output/`.
2. Brief guide from `docs/en/HOW_TO_WORK.md`.
3. List `inputs/raw_texts/` **and** `inputs/audio/`.
4. **If user has only audio** — suggest STT (`docs/en/AUDIO_TRANSCRIPTION.md`), then continue with text.
5. Text type → optional profile in `profiles/`.

---

## Phase 1 — Read source

UTF-8 → cp1251 fallback. Note genre, register, speakers, damaged STT.

---

## Phase 1.5 — Auto-detect (when available)

Run `tools/auto_detect.py` → plan in `output/.llm_cache/auto_plan.json`.  
Flags: **keep_mat=True by default** for dialogue/stt.

---

## Phase 2 — Questions

Unless user said “proceed”: style mode, title, glossary, **profanity (default: keep)**, scope, ambiguous STT spans.

---

## Phase 3 — Processing

1. Hygiene → remove STT junk, dedupe words  
2. Reconstruction → fix STT **in context (±10 turns)**; see [`glossary/STT_PROCESSING_ALGORITHMS.en.md`](../glossary/STT_PROCESSING_ALGORITHMS.en.md) — **no** comma-splice regex  
3. Profile if needed  
4. Typography  
5. **Phase 3.5 — Context audit** (dialogues / large STT edits):
   - Compare with source (`.bak_*`, `inputs/`) for `. But` → `, but` regression
   - Report: `output/.llm_cache/*.audit.md` or `tools/context_audit_report.md`
   - Spec: [`glossary/UNIVERSAL_EDITORIAL_SPEC.en.md`](../glossary/UNIVERSAL_EDITORIAL_SPEC.en.md)
6. 8 audits (`docs/en/TECHNICAL_SPECIFICATION.md`) + `check_stt_artifacts`  
7. DOCX → default `output/books/` **or client-specified path** (no duplicates)  
   - **prepress_book:** remove `Speaker [HH:MM] [Voice]:`, format `— reply. — Speaker.` — see `profiles/DIALOGUE_TRANSCRIPT.md`

---

## Phase 4 — Report

DOCX path, fixes, open questions.

---

## Language

English (this folder `prompts/en/`).
