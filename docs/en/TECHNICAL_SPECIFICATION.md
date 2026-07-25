# 8 editorial audits (universal)

Format-specific rules: `prompts/en/profiles/`.  
User names/brands: `config/glossary_user.json`.

## Checklist

1. **Orthography** — spelling, hyphenated particles, detached introducers  
2. **Punctuation** — commas, «quotes» or “quotes”, em dash ` — `  
3. **Syntax** — capitals, terminal punctuation, complete clauses  
4. **Facts** — consistent proper nouns; never alter numbers/dates/quotes  
5. **Style** — author voice; remove machine junk only  
6. **Lexicon** — stutters, duplicates, obvious OCR/STT fixes when context is clear  
7. **Structure / check_cuts** — no paragraph ending on conjunction/preposition  
8. **Attribution** (if multi-speaker) — consistent names and agreement when gender/role known  

## Stream reconstruction

Split run-on speech into sentences and paragraphs; preserve 100% meaning.

STT: `prompts/en/profiles/SPEECH_TO_TEXT.md` · Dialogues: `prompts/en/profiles/DIALOGUE_TRANSCRIPT.md`
