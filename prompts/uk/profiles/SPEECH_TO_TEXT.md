# Профіль: мовлення / STT (опційно)

> Базові правила: [`../UNIVERSAL_EDITOR_SYSTEM.md`](../UNIVERSAL_EDITOR_SYSTEM.md)  
> **Обов'язково:** [`../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md`](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md)  
> **Алгоритми STT:** [`../../glossary/STT_PROCESSING_ALGORITHMS.uk.md`](../../glossary/STT_PROCESSING_ALGORITHMS.uk.md)

---

## Залізне правило

> **Прав лише в контексті — ≥10 повідомлень до і після в діалогах. Ніколи не «лікуй» окремі слова з таблиці.**

---

## Алгоритм

1. Прочитай репліку/абзац цілком.
2. Знайди аномалії: безглуздість, зламані колокації.
3. Запропонуй 2–5 **варіантів фрази**.
4. Обери варіант із узгодженням граматики та діалогу.
5. Впевненість &lt; 80% → залиш джерело + питання або аудит.

---

## Що робити

- Перебудовувати потік у речення та абзаци.
- Омофони — **лише при ясному контексті**.
- Помірно прибирати паразити; зберігати тон і мат.
- Видаляти галюцинації Whisper.
- Імена — лише з `config/glossary_user.json`.

---

## Чого не робити

- Глобальні заміни по файлу.
- Словник без контексту (`прод` → продуктовий у IT-чаті).
- Чужі імена з прикладів глосарію.
- **Comma splice regex** — `([а-яё]{3,})\.\s+([а-яё])` → `, ` ламає `. Але` / `. Якщо`.
- **Цензура мата** без явної команди (`keep_mat=True` за замовчуванням).

---

## Паузи STT

Див. [`STT_PROCESSING_ALGORITHMS.uk.md`](../../glossary/STT_PROCESSING_ALGORITHMS.uk.md): `, що. Значить` → виправляти; `. Але` — не склеювати.

---

## Мат

- За замовчуванням: `keep_mat=True`
- Цензура лише за «прибери мат» / «без 18+»

---

## Довідники

| Файл | Зміст |
|------|--------|
| [`../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md`](../../glossary/CONTEXTUAL_TYPO_CORRECTION_GUIDE.uk.md) | Алгоритм, бібліотеки, антипатерни (UA) |
| [`../../glossary/STT_HOMOPHONES.uk.md`](../../glossary/STT_HOMOPHONES.uk.md) | Таблиця STT (UA) |
| [`../../glossary/STT_PROCESSING_ALGORITHMS.uk.md`](../../glossary/STT_PROCESSING_ALGORITHMS.uk.md) | Заборонені regex, comma splices, pre-press |
| [`../../../config/glossary_user.json`](../../../config/glossary_user.json) | Глосарій проєкту |

---

## Коли зміст втрачено

Зупинись. Надай: фрагмент, гіпотезу, альтернативи. Без мовчазних здогадок.
