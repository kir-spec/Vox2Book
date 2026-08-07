# Contextual typo & STT correction guide (for AI)

> **REQUIRED READING** before editing speech transcripts, OCR, or drafts.  
> Use with [`../en/UNIVERSAL_EDITOR_SYSTEM.md`](../en/UNIVERSAL_EDITOR_SYSTEM.md) and [`../en/profiles/SPEECH_TO_TEXT.md`](../en/profiles/SPEECH_TO_TEXT.md).  
> **Universal editorial spec (depersonalized client requirements):** [`UNIVERSAL_EDITORIAL_SPEC.en.md`](UNIVERSAL_EDITORIAL_SPEC.en.md)

Other languages: [RU](CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) · [UK](CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md)

---

## Iron rule (non-negotiable)

> **Fix words and phrases ONLY in context — never in isolation, like autocorrect.**

| Forbidden | Why |
|-----------|-----|
| Scanning text and “fixing” every suspicious word from a dictionary | Homophones and STT errors are often **grammatically valid** but **semantically wrong** |
| Global find-and-replace `X → Y` across the file | The same misheard token can mean different things in different places |
| Trusting spell-check / SymSpell / Hunspell without context | They rank by spelling, not **utterance meaning** |
| Silent guessing when context does not fit | Leave source and ask the user |

**Minimum context:**
1. **Full sentence** (better: paragraph or adjacent speaker turns)
2. **Dialogue window:** **≥10 messages before and 10 after** the broken STT phrase
3. **Topic** (health, IT, relationships, work…)
4. **Speaker** (if labeled)
5. **Project glossary** (`config/glossary_user.json`)

**STT pauses:** fix inside one thought (`, what. Means` → `, what means`); **never** merge independent sentences (`. But if` must keep the period). Canon: [`STT_PROCESSING_ALGORITHMS.en.md`](STT_PROCESSING_ALGORITHMS.en.md).

**Intonation commas:** remove after verbs (`find, something`); **do not touch** `340, something rubles`.

If **2+ plausible readings** remain — **do not edit**; flag in audit or ask.

---

## Algorithm (for AI)

```
1. Read the paragraph / turn whole — grasp intent.
2. Mark anomalies: nonsense, broken collocations, agreement breaks, wrong jargon.
3. Formulate 2–5 candidates — whole phrases, not single dictionary swaps.
4. Pick the reading where:
   - the sentence sounds natural when spoken;
   - grammar agrees (tense, person, number);
   - the neighboring turn still fits (question ↔ answer).
5. If confidence < 80% — keep source + [?] or ask the user.
```

**Examples (context decides):**

| STT source | Bad (no context) | Good (in context) |
|------------|------------------|-------------------|
| “I have a fever laying in bed” | “laying” → always wrong | “lying in bed” (rest); “laying” only if placing objects |
| “need to buy a mouse” | animal | computer peripheral if IT topic |
| “pushed to prod” | grocery production | software **production** deploy in dev chat |
| “their going to merge” | leave as-is | “they’re going to merge” only if grammar clearly broken |

---

## Error types (what to look for)

### 1. Homophones & phonetic substitutions (STT / dictation)
Sound alike, spelled differently: *there/their/they’re*, *right/write*.

### 2. Fused / split words from pauses
*“alot”*, *“in to”* vs *“into”* — sometimes style, sometimes error; judge by meaning.

### 3. Names, brands, place names
Whisper mangles rare names — **only from user glossary**, not example projects.

### 4. Code-switching & tech jargon
Mixed EN + other languages; phonetic Cyrillic for Latin terms; slang (*ship it*, *prod*, *LGTM*).

### 5. Whisper hallucinations
“Subscribe to the channel”, subtitle boilerplate, unrelated language — **delete without asking**.

### 6. OCR / keyboard typos
Adjacent-key swaps (*teh → the*), missing letters — fix only if word **does not fit the topic**.

### 7. Homographs (same spelling, different meaning)
*lead* (metal vs guide), *bass* (fish vs low sound), *tear* (rip vs drop) — **neighbor words decide**.

---

## Open resources (reference only — not blind substitution)

| Resource | What it provides | Link |
|----------|------------------|------|
| **guychuk/typos-misspellings-homophones** | Typos + homophones dataset | https://huggingface.co/datasets/guychuk/typos-misspellings-homophones-dataset |
| **JamSpell** | Context n-gram corrector (`FixFragment`) | https://github.com/bakwc/JamSpell |
| **SymSpell** | Fast edit distance (weak alone on homophones) | https://github.com/wolfgarbe/SymSpell |
| **LanguageTool** | Grammar + style rules | https://languagetool.org/ |
| **GitHubTypoCorpusRu** | Typos in commits (mixed EN) | via spellcheck benchmarks |
| **ai-forever/spellcheck_benchmark** | Sentence-level RU pairs (useful for Cyrillic in mixed text) | https://huggingface.co/datasets/ai-forever/spellcheck_benchmark |

**For AI:** even JamSpell and LanguageTool fail on homophones and jargon. You are a **meaning-aware editor**, not a `replace()` pipeline.

---

## Common STT pairs (candidates — not auto-replace!)

> “When valid” column = **required context**. Without it — do not change.

### Health, home, emotions

| Heard | Possibly meant | When valid |
|-------|----------------|------------|
| laying / lieing | lying (reclining) | illness, rest |
| fever / temp | fever / temperature | body, not weather |
| charger / charging | charger | phone, laptop |
| mouse | mouse | computer vs animal |

### Tech (see also [`STT_HOMOPHONES.en.md`](STT_HOMOPHONES.en.md))

| Heard | Possibly | Context |
|-------|----------|---------|
| you es bee / usb | USB | cable, port |
| ess ess dee | SSD | storage |
| prod / production | production | deploy, not grocery |
| get / git | Git | version control |
| docker / docket | Docker | containers |
| kafka | Kafka | queues, backend |
| wrecked | React | UI framework (phonetic confusion) |

### Oral markers (usually keep)

| Heard | Note |
|-------|------|
| uh, um, like, you know | Reduce moderately |
| gonna, wanna, kinda | Keep in casual dialogue |
| profanity | **Do not remove** without user request |

### Homophone classics (phrase-level only)

| Pair | Context clue |
|------|--------------|
| there / their / they're | location vs possession vs “they are” |
| your / you're | possession vs “you are” |
| its / it's | possession vs “it is” |
| then / than | time vs comparison |
| affect / effect | verb vs result noun |
| accept / except | receive vs exclude |

---

## OCR / keyboard confusion matrix

Common swaps: **e↔a**, **i↔e**, **o↔p**, **m↔n**, **rn↔m** (*clown → crown*).  
Check whether the word exists **in this topic**; if not, search meaning across the **whole sentence**.

---

## Anti-patterns (real AI editor mistakes)

1. **`their` → `there`** everywhere — wrong without grammar check in context.
2. **`prod` → product** in a software deploy thread — breaks meaning.
3. **`mouse` → pet** in a PC setup discussion.
4. **Stripping slang/profanity** without user request — breaks Vox2Book contract.
5. **Importing names** from example glossaries into unrelated projects.
6. **“Correcting” intentional dialect** to standard English without being asked.
7. **Comma splice regex** — `([а-яё]{3,})\.\s+([а-яё])` → `, ` breaks `. But` / `. If`.
8. **Global comma removal before “something”** — breaks `340, something rubles`.

---

## Project files

| File | Purpose |
|------|---------|
| [`STT_HOMOPHONES.en.md`](STT_HOMOPHONES.en.md) | Extended EN candidate table |
| [`../../config/glossary_user.json`](../../config/glossary_user.json) | **This** project's names and fixes |
| [`../en/profiles/SPEECH_TO_TEXT.md`](../en/profiles/SPEECH_TO_TEXT.md) | Voice profile |
| [`../en/profiles/DIALOGUE_TRANSCRIPT.md`](../en/profiles/DIALOGUE_TRANSCRIPT.md) | Multi-speaker alignment |
| [`STT_PROCESSING_ALGORITHMS.en.md`](STT_PROCESSING_ALGORITHMS.en.md) | Regex canon, pre-press, keep_mat |

---

## Pre-delivery checklist

- [ ] Every fix verified **in the sentence**, not from a dictionary alone.
- [ ] Adjacent turns still match (Q/A).
- [ ] Names from `glossary_user.json`, not invented.
- [ ] Ambiguous spans in `output/.llm_cache/*.audit.md`.
- [ ] STT hallucinations removed.
- [ ] No global replace across the file unless user explicitly ordered it.
- [ ] No mass `. But` → `, but` regression.
- [ ] Profanity not censored without explicit command (`keep_mat=True` default).

