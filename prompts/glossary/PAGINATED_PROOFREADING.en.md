# Paginated proofreading for large DOCX (canonical)

> **Required** for documents from ~50 virtual pages upward (1000+ dialogue turns, 300+ print pages).  
> Tool: `tools/page_batch_proofread_anfi.py` · progress: client-side `.proofread_progress.json`.

---

## Iron rule

**Do not read or edit the entire document in one pass.**  
Work **sequentially in batches**: read → fix → save → record progress → **only then** the next batch.

### Forbidden

- “Finishing” remaining pages with `run-all`, global regex, or auto-STT **instead of** reading each batch.
- Jumping to page 800+ before earlier batches are read and patched.
- Marking a batch done if only a regex whitelist ran without reading the batch text.

### Allowed as a supplement (not a substitute for reading)

- Narrow auto-STT whitelist **after** manual batch reading.
- `export` / `apply` / `fill_message_paragraph` — only after a fix list from reading.

---

## One batch cycle

1. **Export** the full batch: `python tools/page_batch_proofread_anfi.py export --start <N> --pages <P>`
2. **Read the entire export** (+ 2 context turns before/after in the file).
3. **Fix list**: `msg <idx> (Speaker): before → after`.
4. **Apply** in-place; verify message count unchanged.
5. **Progress**: `last_completed_page = N+P-1`; short report.
6. Next batch: `--start N+P`.

---

## Batch size (pages per pass)

Virtual page ≈ **1800 characters** of DOCX paragraphs (turns + `📅` headers).

| Model tier | Examples | Pages **P** per pass |
|------------|----------|----------------------|
| **Full context** | Claude Opus/Sonnet, GPT-4.x, Cursor Agent, Composer, Gemini Pro | **10** |
| **Medium context** | GPT-4o mini, limited free chat tiers | **3–5** |
| **Narrow / free auto** | Kilocode auto free, small local models, strict token caps | **1–2** |

If the model **cannot** read **P** pages attentively, **lower P** — do not skip pagination.

See also: [`STT_PROCESSING_ALGORITHMS.en.md`](STT_PROCESSING_ALGORITHMS.en.md), [`../en/AGENT_WORKFLOW.md`](../en/AGENT_WORKFLOW.md) §3.1.
