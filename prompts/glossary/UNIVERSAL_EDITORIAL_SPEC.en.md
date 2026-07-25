# Universal Editorial Specification — STT, Dialogues, Pre-press

> **Depersonalized canon** — no tie to a specific project, file, or speaker names.  
> Applies to any speech transcripts, chat exports, and print-ready manuscripts.  
> See also: [`STT_PROCESSING_ALGORITHMS.en.md`](STT_PROCESSING_ALGORITHMS.en.md), [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md).

Other languages: [RU](UNIVERSAL_EDITORIAL_SPEC.ru.md) · [UK](UNIVERSAL_EDITORIAL_SPEC.uk.md)

---

## 0. Purpose

This document captures **quality requirements** and **typical automation failures** found in real proofreading work.  
Use it as a single spec for AI editors, manual proofreaders, and regex scripts.

**Project-specific names, brands, and places** — only from `config/glossary_user.json`, not from examples below.

---

## 1. Context and meaning (mandatory)

| ID | Requirement |
|----|-------------|
| **C-01** | Before any non-trivial STT fix — at least **10 turns BEFORE and 10 AFTER** the target fragment. |
| **C-02** | Verify **question ↔ answer** and topic within ±10 turns. |
| **C-03** | **Semantic restoration:** no meaningless fragments; no lost phrases during rebuild. |
| **C-04** | With 2+ plausible readings — **do not fix silently**; mark `[?]` or ask the client. |
| **C-05** | Large documents (300+ pp.): **100% coverage** — no skipped turns or truncated processing. |
| **C-06** | No global `replace()` across the file for homophones, brands, or profanity. |

---

## 2. STT pauses: period and capital mid-phrase

| ID | Problem | Action |
|----|---------|--------|
| **P-01** | Whisper pause splits one thought: `, that. Means` | → `, that means` (lowercase after connector) |
| **P-02** | Same after `because`, `so that`, `as` | Period + capital → space + lowercase if thought continues |
| **P-03** | Reverse error: **independent** sentences merged with a comma | Restore **period** (see §3) |

**Forbidden regex (never):**

```text
([a-z]{3,})\.\s+([a-z])  →  \1, \2
```

(Russian projects: same rule for `([а-яё]{3,})\.\s+([а-яё])`.)

---

## 3. Comma splices (merged independent sentences)

| ID | Automation error | Correct |
|----|------------------|---------|
| **S-01** | `it's hard, if you don't mind, I wanted…` | `it's hard. If you don't mind, I wanted…` |
| **S-02** | `perception, if we continue…` | `perception. If we continue…` |
| **S-03** | `in memory, if there is no imprint…` | `in memory. If there is no imprint…` |
| **S-04** | `see, but if…` (after STT pause cleanup) | **Keep** `see. But if…` |

**New-sentence starters** — do not turn their preceding period into a comma:  
`But`, `And`, `So`, `Therefore`, `However`, `By the way`, `Listen`, `Look`, `Here`, `Well`, `I mean`, `Hi`, `OK`, `Then`, `Later`, `If`, `When`, `Anyway`, `Basically`, `Oh`.

**Regex trap:** pattern `but.\s+If` falsely matches `hard. If` — use **word boundary** `\bbut\.\s+If`, not a substring inside words ending in `-ly`/`-no`.

---

## 4. Intonation commas (spurious STT pauses)

| ID | Remove | Example |
|----|--------|---------|
| **I-01** | Comma before `something` / `anything` **after a verb** | `find, something` → `find something` |
| **I-02** | Comma inside pronoun | `recording on, something` → `recording on something` |
| **I-03** | Comma in simple question | `And you, when you go to bed…` → `And you when you go to bed…` |
| **I-04** | Similar | `quickly, something to learn` → `quickly something to learn` |

| ID | **Do not touch** | Example | Reason |
|----|------------------|---------|--------|
| **I-10** | Approximate number | `340, something dollars` | Colloquial estimate |
| **I-11** | Legal subordinate | `I know that he will come` | Normal punctuation |
| **I-12** | Compound with “but” | `wanted to, but couldn't` | Comma before “but” is correct |

---

## 5. Long monologue punctuation

| ID | Requirement |
|----|-------------|
| **M-01** | Voice note **> 1200–1500 chars** with few periods — **add** boundaries between complete thoughts. |
| **M-02** | New-thought markers (carefully): `Listen`, `Look`, `By the way`, `So`, `I mean`, `Then`, `Anyway`, `Imagine`, `Suppose` — only if no period precedes them. |
| **M-03** | **Do not** insert periods before every `well`, `just`, `here` in short turns. |
| **M-04** | **Do not** use `this`/`it` as a universal boundary marker — breaks phrases like “we know this from…”. |
| **M-05** | After auto-punctuation — **manual proofread** of longest turns; normalize `,.` → `.`, `..` → `.`. |
| **M-06** | Trigger threshold: roughly **~1 period per 200–280 characters** in a long monologue; below — under-punctuated. |

---

## 6. STT mishearings (whitelist + context only)

Replacements **only on full phrase match** with ±10-turn context check.

### 6.1. Semantic

| Class | Typical glitch | Restoration |
|-------|----------------|-------------|
| Verb | `anything to-do` (делу) | `anything to do` |
| Verb | `tоручаюсь` | `поручаюсь` / `I take responsibility` |
| Noun/abbr. | `as AI I end up` garble | `if I as an AI end up` |
| Noun | `irons` (иронах) | `neurons` (нейронах) |

### 6.2. Tech and network

| Class | Typical glitch | Restoration |
|-------|----------------|-------------|
| VPN | `vipen`, `vipeon`, `not in vipe` | `VPN` |
| USB | `tivisb`, `type c` garble | `Type-C` |
| USB | `micro usb` garble | `micro USB` |
| Network | `byedpi` garble | `ByeDPI` |
| DAW | `Logic"om` | `Logic Pro` |

### 6.3. Numbers in speech

| ID | Problem | Action |
|----|---------|----------|
| **N-01** | STT digit instead of word | `22 microphones` when meaning “a pair” → `two microphones` (by context) |
| **N-02** | Extra space in fraction | `3, 8 million` → `3.8 million` (EN) / `3,8 миллиона` (RU) |
| **N-03** | Decimal separator | locale-consistent (`1.5×` EN / `1,5×` RU) |
| **N-04** | Speed units | `20 km per hour` → `20 km/h` |
| **N-05** | Percents and multipliers | one publishing standard per document |

---

## 7. Tail hallucinations (Whisper)

| ID | Requirement |
|----|-------------|
| **H-01** | Trim **meaningless Latin/garbage tail** after the last sensible phrase (random English, unrelated fragments). |
| **H-02** | Do not remove meaningful English terms and brands inside the body. |
| **H-03** | If trimming changes meaning — note in audit, do not cut silently. |

---

## 8. Profanity and legal status

| Mode | Condition | Action |
|------|-----------|--------|
| **Default** | dialogue / STT | `keep_mat=True` — **do not censor** |
| Censor | “remove profanity”, “kids”, “no 18+” | literary substitute + report |
| Print with profanity | “keep profanity for print” | keep lexicon + **remind** about 18+ labeling and sealed wrap |

---

## 9. Two dialogue modes

| Mode | When | Export labels | Turn format |
|------|------|---------------|-------------|
| **`raw_chat`** | archive, screen, working copy | **Keep** `Speaker [HH:MM] [Voice]:` | as exported |
| **`prepress_book`** | “book”, “print”, “pre-press” | **Remove** time, `[Voice]`/`[Text]` | `— Reply text. — Speaker.` |

If unspecified — **`raw_chat`**. Pre-press only on explicit command.

### Pre-press typography (`prepress_book`)

- Curly quotes; inner quotes when nested.
- Em dash ` — ` with non-breaking spaces.
- Ellipsis `…` instead of `...`.
- Keep `📅` dates and section dividers.

---

## 10. Output file and audit

| ID | Requirement |
|----|-------------|
| **O-01** | Save path — **as specified by the client**; no duplicate copies elsewhere without request. |
| **O-02** | Vox2Book default: `output/books/<name>.docx`; overridden by explicit command. |
| **O-03** | Before delivery — context audit: compare with `.bak_*` / `inputs/`, regression report. |
| **O-04** | Verify no mass `. But` → `, but` regression. |
| **O-05** | Report: `output/.llm_cache/*.audit.md` or `tools/context_audit_report.md`. |

---

## 11. Processing pipeline (recommended order)

1. Hygiene: STT junk, links, duplicates, stutters.
2. Contextual STT replacements (whitelist §6).
3. STT pauses inside phrases (§2).
4. Comma splices — whitelist fix (§3).
5. Intonation commas (§4).
6. Long monologue punctuation (§5).
7. Numbers and units (§6.3).
8. Tail hallucinations (§7).
9. Pre-press / typography (§9) — if requested.
10. Manual proofread of long turns + context audit (§10).

Conservative script template: `tools/contextual_rebuild_*.py` (project-specific; not aggressive round-N cascades without audit).

---

## 12. Delivery checklist

- [ ] C-01…C-06: context and meaning.
- [ ] P-01…P-03, S-01…S-04: pauses and comma splices.
- [ ] I-01…I-04 without false I-10…I-12.
- [ ] M-01…M-06: long monologues.
- [ ] §6 whitelist STT; §7 tails; §6.3 numbers.
- [ ] §8 profanity per mode.
- [ ] §9 raw_chat / prepress_book mode.
- [ ] §10 audit and output path.
