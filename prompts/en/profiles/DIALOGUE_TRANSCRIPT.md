# Dialogue & Chat Transcript Profile (optional overlay)

> **Load only** for multi-speaker chats, interview transcripts, messenger exports.  
> Universal rules: [`../UNIVERSAL_EDITOR_SYSTEM.md`](../UNIVERSAL_EDITOR_SYSTEM.md).

---

## Structure to preserve (unless user says otherwise)

- Speaker names / labels
- Timestamps (date, time) if present in source
- Message type markers ([voice], [text], [Голосовое], [Текст])
- Section headings (by day, month, chapter) if user requested them

---

## Additional rules

1. **Per-speaker consistency:** same spelling of each name throughout.
2. **Gender agreement:** align verb/adjective endings with each speaker **only when gender is known** — ask if unclear.
3. **Turn boundaries:** one message = one block; do not merge different speakers without reason.
4. **Voice vs typed:** voice lines get full literary reconstruction; typed lines get lighter edit (they are often already written).
5. **Profanity & register:** preserve each speaker's level unless user requests uniform “clean” edition.

---

## Optional chronology

If multiple source files exist (e.g. HTML chat + voice exports), merge by timestamp **only when user explicitly requests** chronological assembly.

---

## Project-specific data — NOT in this prompt

Speaker names (Kir, Anfia, etc.), relationship labels, and custom spelling rules belong in:

- `config/glossary_user.json` or
- a note from the user in chat

**Never** assume names from other users' projects.

---

## Typography for dialogue

Russian house style:

```
Анфи [18:29] [Голосовое]: Текст реплики.
Kir [18:46] [Текст]: Короткий ответ.
```

Or em-dash style if user prefers:

```
— Текст реплики, — сказала Анфи.
```

Follow user preference when stated.
