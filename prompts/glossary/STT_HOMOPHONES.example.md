# STT / OCR — homophone tables (all languages)

> **Not loaded automatically.**  
> **Never use as a bulk replace script.** Fix **only in sentence context**.

---

## Choose your language

| Language | Contextual guide (read first) | STT candidate table |
|----------|------------------------------|---------------------|
| 🇷🇺 Русский | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md) | [`STT_HOMOPHONES.ru.md`](STT_HOMOPHONES.ru.md) |
| 🇬🇧 English | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md) | [`STT_HOMOPHONES.en.md`](STT_HOMOPHONES.en.md) |
| 🇺🇦 Українська | [`CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md`](CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) | [`STT_HOMOPHONES.uk.md`](STT_HOMOPHONES.uk.md) |

---

## Iron rule (all languages)

> **Fix words and phrases only in context — never word-by-word, never global replace.**

1. Read the **whole sentence** (or speaker turn pair).
2. Tables list **candidates**, not automatic swaps.
3. Project names → `config/glossary_user.json` only.
4. If ambiguous → ask or audit flag.

---

## JSON format (`config/glossary_user.json`)

```json
{
  "heard": "pattern|alternate",
  "correct": "Canonical form",
  "context_hint": "when this fix applies",
  "never_replace_globally": true
}
```

Copy template from [`../../config/glossary_user.example.json`](../../config/glossary_user.example.json).

---

## Chat snippets

**RU:**
```text
Правь STT по CONTEXTUAL_TYPO_CORRECTION_GUIDE.ru.md и STT_HOMOPHONES.ru.md.
Имена — из config/glossary_user.json. Только контекст, без глобальных замен.
```

**EN:**
```text
Fix STT per CONTEXTUAL_TYPO_CORRECTION_GUIDE.en.md and STT_HOMOPHONES.en.md.
Names from config/glossary_user.json. Context-only; no global replace.
```

**UK:**
```text
Прав STT за CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md та STT_HOMOPHONES.uk.md.
Імена — з config/glossary_user.json. Лише контекст, без глобальних замін.
```
