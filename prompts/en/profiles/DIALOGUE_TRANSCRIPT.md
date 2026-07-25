# Dialogue & Chat Transcript Profile (optional overlay)

> **Load only** for multi-speaker chats, interview transcripts, messenger exports.  
> Universal rules: [`../UNIVERSAL_EDITOR_SYSTEM.md`](../UNIVERSAL_EDITOR_SYSTEM.md)  
> Universal spec: [`../../glossary/UNIVERSAL_EDITORIAL_SPEC.en.md`](../../glossary/UNIVERSAL_EDITORIAL_SPEC.en.md)  
> STT & pre-press canon: [`../../glossary/STT_PROCESSING_ALGORITHMS.en.md`](../../glossary/STT_PROCESSING_ALGORITHMS.en.md)

---

## Two modes (user command selects)

| Mode | When | Telegram labels | Turn format |
|------|------|-----------------|-------------|
| **`raw_chat`** (default) | screen, archive, working copy | **Keep** `Speaker [18:46] [Voice]:`, time, type | export style + speaker color |
| **`prepress_book`** | “book”, “print”, “pre-press” | **Remove** time, `[Voice]`/`[Text]` | `— Reply text. — Speaker.` |

If unspecified — **raw_chat**. Pre-press only on explicit request.

Speaker names and colors — from `config/glossary_user.json`, not from prompt examples.

---

## Shared rules (both modes)

1. **Full read + context:** restore broken speech using **≥10 turns before and after** each non-trivial fix.
2. **Speaker styling (DOCX):** bold header or trailing name; **unique color** per speaker.
3. **Voice vs typed:** voice → full literary rebuild; typed → lighter edit.
4. **Profanity:** `keep_mat=True` by default; censor only on explicit command.
5. Names — `config/glossary_user.json` only.

---

## `prepress_book` mode

1. Remove `Speaker [23:41] [Voice]:`, `[Text]:`, timestamps.
2. Book dialogue: `— Reply. — Speaker.`
3. Typography: curly quotes, em dash ` — `, ellipsis `…`.
4. Keep `📅` date dividers.

---

## STT in dialogues (summary)

- Fix pauses **inside** a thought: `, what. Means` → `, what means`.
- **Do not merge** `. But` / `. Therefore` / `. If` into commas — see `STT_PROCESSING_ALGORITHMS.en.md`.
- Remove `find, something`, `And you, when`; keep `340, something rubles`.

---

## Turn agreement

- Question ↔ answer must make sense in ±10-turn window.
- Truncated turn without reply — `[cut]` or ask user.

## Context audit (before book delivery)

- Compare with `.bak_*` or `inputs/`; report `tools/context_audit_report.md`.
- Reference rebuild: `tools/contextual_rebuild_*.py` (project template).
- Full requirements: [`UNIVERSAL_EDITORIAL_SPEC.en.md`](../../glossary/UNIVERSAL_EDITORIAL_SPEC.en.md).
