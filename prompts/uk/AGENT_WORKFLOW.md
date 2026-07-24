# Сценарій роботи ІІ-агента (універсальний)

Старт: [`START_USER_PROMPT.md`](START_USER_PROMPT.md)  
Системний промпт: [`UNIVERSAL_EDITOR_SYSTEM.md`](UNIVERSAL_EDITOR_SYSTEM.md)

---

## Фаза 0 — Орієнтація

1. Корінь проєкту: `AGENTS.md`, `inputs/`, `output/`.
2. Довідка з `docs/uk/HOW_TO_WORK.md`.
3. Список `inputs/raw_texts/` **та** `inputs/audio/`.
4. **Якщо лише аудіо** (`.mp3`, `.ogg`, `inputs/audio/`):
   - Vox2Book вичитує **текст** — запропонуй STT: `tools/transcribe_audio.py` **або** OpenAI API, AssemblyAI, Telegram, Descript, GigaAM… (`docs/uk/AUDIO_TRANSCRIPTION.md`).
5. Тип тексту → профіль у `profiles/` за потреби.

---

## Фаза 1 — Читання джерела

UTF-8 → cp1251. Жанр, регістр, спікери, пошкоджений STT.

---

## Фаза 2 — Запитання

Якщо не сказано «роби одразу»: стиль, заголовок, глосарій, лайка, обсяг, неясні місця STT.

---

## Фаза 3 — Обробка

Гігієна → перебудова → профіль → типографіка → 8 аудитів (`docs/uk/TECHNICAL_SPECIFICATION.md`) → `output/books/`.

---

## Фаза 4 — Звіт

Шлях до DOCX, виправлення, відкриті питання.

---

## Мова

Українська (тека `prompts/uk/`).
