# STT & Dialogue Processing Algorithms (canon for scripts and AI)

> **Mandatory** for any regex scripts (`tools/apply_user_corrections_*.py`, `pipeline.py`) and for the AI editor.  
> See also: [`UNIVERSAL_EDITORIAL_SPEC.en.md`](UNIVERSAL_EDITORIAL_SPEC.en.md) (universal spec), [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md), [`../en/UNIVERSAL_EDITOR_SYSTEM.md`](../en/UNIVERSAL_EDITOR_SYSTEM.md).

---

## 0. Iron rules

1. **Context is mandatory:** before any STT fix — at least **10 messages BEFORE and 10 AFTER** the target turn; verify question ↔ answer.
2. **No global `replace()`** across the file for homophones, profanity, or brands.
3. **Profanity preserved by default** (`keep_mat=True`) for dialogues and voice notes until the user explicitly says “censor”, “kids edition”, or “no 18+”.
4. **Scripts ≠ editors:** automation only for a narrow whitelist; anything ambiguous goes to audit or human/LLM review.

---

## 1. STT pauses: period and capital letter

### Allowed fixes (inside one thought)

| Broken (Whisper pause) | Fixed |
|------------------------|-------|
| `knows, what. Means seeing` | `knows what means seeing` |
| `because. Here` | `because here` |
| `, what. Means` | `, what means` |

Rule: after a **subordinating** connector (`that`, `because`, `so that`) a period + capital → **space + lowercase** if the phrase is not finished.

### Forbidden (comma splice — merging independent sentences)

| Algorithm error | Why bad | Correct |
|-----------------|---------|---------|
| `see. But if` → `see, but if` | “But” starts a new thought | **Keep** `see. But if` |
| `hard. If you don't mind` → `hard, if you don't mind` | Second part is a new address | **Keep the period** or whitelist-only fix |
| `memory. If there is no` → `memory, if there is no` | New question/topic | **Period** before “If” |

**Forbidden regex (never use):**

```text
([а-яё]{3,})\.\s+([а-яё])  →  \1, \2
```

**Words after which a period must NOT become a comma** (independent sentence starters):

`But`, `And`, `So`, `Therefore`, `However`, `By the way`, `Listen`, `Look`, `Here`, `Well`, `I mean`, `Hi`, `OK`, `Then`, `Later`, `If`, `When`, `Anyway`, `Basically`, `Oh`.

(Russian originals: `Но`, `А`, `Поэтому`, `Кстати`, `Слушай`, `Вот`, `Если`, `Когда` — same rule.)

### Whitelisted comma-splice fixes only

- `it's hard, if you don't mind` → `it's hard. If you don't mind`
- `tactile perception, if we continue` → `tactile perception. If we continue`
- `in memory, if there is no imprint` → `in memory. If there is no imprint`

---

## 2. Intonation commas (spurious STT pauses)

### Remove

| Pattern | Example |
|---------|---------|
| Before `something` / `anything` after a **verb** | `find, something` → `find something` |
| `what, thing` / `what, ever` splits | → `something` / `whatever` |
| `And you, when` in a simple question | → `And you when` |

### Do not touch

| Pattern | Example | Reason |
|---------|---------|--------|
| Approximate number | `340, something rubles` | Colloquial estimate, not STT |
| Legal subordinate | `I know that he will come` | Normal punctuation |
| Compound with “but” | `wanted to, but couldn't` | Comma before “but” is correct |

---

## 3. Contextual STT replacements (script whitelist)

Only on **full phrase match** with ±10-turn context check:

| Source | Replacement | Context |
|--------|-------------|---------|
| `what-ever to-do` (делу) | `anything to do` | “stopped doing anything” |
| `tоручаюсь` | `поручаюсь` | responsibility |
| `vipen` / `not in vipe` | `VPN` | network, delivery |
| `if I as AI end up` | `if I as an AI end up` | AI philosophy |
| `irons` (иронах) | `neurons` (нейронах) | brain, neural nets |
| `micro USB` garble | `micro USB` | cable, speaker |
| `Type-C` garble | `Type-C` | charging, USB |
| `byedpi` / `байдипя` garble | `ByeDPI` | network bypass |
| `Logic"om` | `Logic Pro` | DAW |
| `22 microphones` (meaning “two”) | `two microphones` | only if ±10-turn context confirms “a pair” |

---

## 4. Long monologue punctuation

### Allowed (carefully)

- Voice **> 1200 chars**, few periods: insert boundaries only before clear **new-thought** markers: `Listen`, `Look`, `By the way`, `So`, `I mean` — only if no period already precedes them.
- Commas before subordinate clauses in **one** long sentence.

### Forbidden

- Mass periods before every `well`, `just`, `here` in short turns.
- Using **`this`/`it`** as a universal boundary marker.
- Punctuation without ±10 neighboring turns.
- Artifacts `,. Here` — normalize `,.` → `.`, `..` → `.`.
- Regex `but.\s+If` without `\b` — false match on `hard. If`.

### After automation

- **Manual proofread** of turns > ~1500 chars with period density < 1 per 250 chars.
- Full restoration of long blocks — by dialogue meaning, not regex alone.

### Conservative reference script

`tools/contextual_rebuild_*.py` — rebuild from backup with safe pipeline (prefer over aggressive round N cascades without audit).

---

## 5. Pre-press preparation

On “book”, “print”, “pre-press”:

1. **Remove** export junk: `Speaker [23:41] [Voice]:`, `[Text]:`, timestamps (names from project glossary).
2. **Dialogue format:** `— Reply text. — Speaker.` (italic/color per `DIALOGUE_TRANSCRIPT.md`).
3. **Typography:** curly quotes, em dash ` — `, ellipsis `…`.
4. Keep `📅` dates and section dividers.

**Raw chat** mode (screen, archive): keep speaker labels and time — unless user asked for pre-press.

---

## 6. Profanity and legal status

| Mode | Condition | Action |
|------|-----------|--------|
| **Default** | dialogue / STT | `keep_mat=True` — do not censor |
| Censor | “remove profanity”, “kids”, “no 18+” | literary substitute + report |
| 18+ print | “keep profanity for print” | keep lexicon + remind about 18+ labeling |

---

## 7. Context audit before delivery

1. Compare with source (`.bak_*` or `inputs/`) — spot-check and all regex edits.
2. Verify no mass `. But` → `, but` regression.
3. Report: `tools/context_audit_report.md` or `output/.llm_cache/*.audit.md`.
4. Template anomalies: `tools/context_audit_*.py` (project-specific).

---

## 8. Numbers, fractions, and units

| Broken | Fixed | Note |
|--------|-------|------|
| `3, 8 million` | `3.8 million` (EN) / `3,8 миллиона` (RU) | extra space |
| `1.5x` | `1.5×` (EN) / `1,5×` (RU) | locale decimal + multiply sign |
| `20 km per hour` | `20 km/h` | consistent units |
| `22 microphones` (meaning two) | `two microphones` | context ±10 turns only |

---

## 9. Tail hallucinations (Whisper)

- Trim meaningless Latin/garbage **tail** after the last complete thought.
- Do not remove legitimate brands/terms inside the body.
- If trimming is ambiguous — audit, not silent deletion.

---

## 10. Semantic restoration

- No **lost phrases** and no **meaningless fragments** recoverable from ±10 turns.
- Long monologue rebuild — keep all speaker topics; do not over-compress.
- Ambiguous spots — `[?]` or ask the client.

---

## 11. Pre-delivery checklist

- [ ] ±10 turns read for each non-trivial edit.
- [ ] No forbidden period→comma regex.
- [ ] Comma splices from §1 fixed; independent “But/Therefore” not merged.
- [ ] Commas before `something` removed only after verbs, not in `340, something`.
- [ ] Profanity untouched without explicit command.
- [ ] Pre-press: no `Speaker [HH:MM] [Voice]` in final book.
- [ ] Long monologues: improved punctuation; manual pass >1500 chars.
- [ ] Numbers §8; tails §9; meaning §10.
- [ ] Output path as client specified; no extra duplicate files.
