# Speech-to-Text Profile (optional overlay)

> Universal rules: [`../UNIVERSAL_EDITOR_SYSTEM.md`](../UNIVERSAL_EDITOR_SYSTEM.md)  
> **Required:** [`../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md)  
> Tables: [`../../glossary/STT_HOMOPHONES.en.md`](../../glossary/STT_HOMOPHONES.en.md) · [RU guide](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) · [UK guide](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md)

---

## Iron rule

> **Fix only in context — full sentence, paragraph, adjacent speaker turns. Never word-by-word from a table.**

Spell-checkers (JamSpell, Yandex.Speller, SymSpell, Hunspell) suggest candidates; they do **not** replace meaning-aware editing.

---

## Algorithm (short)

1. Read the whole utterance — intent first.
2. Mark anomalies: nonsense, broken collocations, wrong jargon.
3. Propose 2–5 **phrase-level** candidates.
4. Pick the reading that fits grammar and dialogue flow.
5. Confidence &lt; 80% → keep source + question or audit note.

---

## Additional rules

1. **Re-sentence aggressively** — oral flow must become readable prose.
2. **Homophones:** fix only when context is unambiguous; otherwise flag for user.
3. **Filler words:** reduce moderately; keep tone and profanity unless asked.
4. **Numbers & units:** normalize only when standard in target genre.
5. **Latin brands & tech:** restore conventional spelling **in context** (USB, Bluetooth, production, etc.).

---

## Do not

| Mistake | Example |
|---------|---------|
| Global replace | same swap everywhere in file |
| Dictionary without context | `prod` → grocery in a dev chat |
| Mechanical swap | homophone table without reading the sentence |
| Foreign glossary | names from examples in another project |

---

## Reference files

| File | Content |
|------|---------|
| [`../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) | Algorithm, libraries, anti-patterns |
| [`../../glossary/STT_HOMOPHONES.en.md`](../../glossary/STT_HOMOPHONES.en.md) | Large EN STT table |
| [`../../glossary/STT_HOMOPHONES.example.md`](../../glossary/STT_HOMOPHONES.example.md) | Index ru / en / uk |
| [`../../../config/glossary_user.json`](../../../config/glossary_user.json) | **This** project's names and fixes |

---

## STT hallucinations — always delete

- “Subscribe to the channel” / «Подписывайтесь на канал»
- “Thanks for watching” / subtitle credits
- Dictation UI junk, repeated phrase loops

---

## When meaning is lost

Stop and ask. Provide: original fragment, best guess, alternatives. No silent guesses on plot-critical or technical passages.
