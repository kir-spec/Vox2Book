# Сценарій роботи ІІ-агента (універсальний)

Старт: [`START_USER_PROMPT.md`](START_USER_PROMPT.md)  
Системний промпт: [`UNIVERSAL_EDITOR_SYSTEM.md`](UNIVERSAL_EDITOR_SYSTEM.md)

---

## Фаза 0 — Орієнтація

1. Корінь: `AGENTS.md`, `inputs/`, `output/`.
2. `docs/uk/HOW_TO_WORK.md`.
3. Список `inputs/raw_texts/` та `inputs/audio/`.
4. Лише аудіо → запропонуй STT (`docs/uk/AUDIO_TRANSCRIPTION.md`).
5. Тип тексту → профіль у `profiles/`.

---

## Фаза 1 — Читання джерела

UTF-8 → cp1251. Жанр, регістр, спікери, битий STT.

---

## Фаза 1.5 — Автовизначення

`tools/auto_detect.py` → `output/.llm_cache/auto_plan.json`.  
Прапорці: **keep_mat=True за замовчуванням** для dialogue/stt.

---

## Фаза 2 — Питання

Якщо користувач не сказав «роби одразу»: стиль, заголовок, глосарій, **мат (за замовчуванням — зберігати)**, обсяг, неясні STT.

---

## Фаза 3 — Обробка

1. Гігієна джерела  
2. Літературна перебудова — STT **лише в контексті (±10 реплік)**; див. [`STT_PROCESSING_ALGORITHMS.uk.md`](../glossary/STT_PROCESSING_ALGORITHMS.uk.md) — **без** comma-splice regex  
3. Профіль  
4. Типографіка  
5. **Фаза 3.5 — Контекстний аудит** (діалоги / великі STT-правки):
   - Порівняння з `.bak_*` / `inputs/` на регресію `. Але` → `, але`
   - Звіт: `output/.llm_cache/*.audit.md` або `tools/context_audit_report.md`
   - ТЗ: [`glossary/UNIVERSAL_EDITORIAL_SPEC.uk.md`](../glossary/UNIVERSAL_EDITORIAL_SPEC.uk.md)
6. 8 аудитів (`docs/uk/TECHNICAL_SPECIFICATION.md`) + `check_stt_artifacts`  
7. DOCX → за замовчуванням `output/books/` **або шлях замовника** (без дублікатів)  
   - **prepress_book:** прибрати `Спікер [ГГ:ХХ] [Голосове]:`, формат `— репліка. — Спікер.`

---

## Фаза 4 — Звіт

Шлях до DOCX, що виправлено, відкриті питання.

---

## Мова

Українська (тека `prompts/uk/`).
