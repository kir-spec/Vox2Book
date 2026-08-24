# -*- coding: utf-8 -*-
"""Удаление реплик без контекстной связи из глав Kir и Анфи."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(r"E:\coding\работа с литературой")
BOOK_DIR = ROOT / "output" / "books" / "Kir и Анфи"
REPORT = ROOT / "output" / "books" / "_prune_orphan_report.md"

HDR_RE = re.compile(r"^(Kir|Анфи)\s+·\s+(\d{1,2}:\d{2})$")
DAY_RE = re.compile(
    r"^(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+(\d{4})$"
)
QUESTION_RE = re.compile(
    r"[?]|(?:^|\s)(почему|зачем|как|можешь|расскаж|скажи|а\s+что|что\s+это|интересно)\b",
    re.IGNORECASE,
)
SKIP_PREFIX = ("Диалоги", "Глава", "Kir и Анфи", "Декабрь 2024")

STOP = frozenset(
    """
    этот этого этой этих этом ещё уже очень просто вот если тогда может например
    потому когда который которые которое чтобы потому что ну да нет вот это что как
    там тут себе себя мне тебе тебя твой твоя твои мой моя мои он она они
    было была были есть быть был была буду будешь будем будут
    """.split()
)

GAP_MINUTES = 360
OVERLAP_MIN = 0.11
SHORT_ORPHAN_CHARS = 100


def delete_paragraph(paragraph) -> None:
    el = paragraph._element
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[а-яёa-z]{4,}", text.lower())
    return {w for w in words if w not in STOP}


def overlap(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


def minutes(time_s: str) -> int:
    h, m = map(int, time_s.split(":"))
    return h * 60 + m


def gap_minutes(day_a: str, time_a: str, day_b: str, time_b: str) -> int:
    if day_a != day_b:
        return 10_000
    gap = minutes(time_b) - minutes(time_a)
    if gap < 0:
        gap += 24 * 60
    return gap


def parse_messages(doc: Document) -> list[dict]:
    msgs: list[dict] = []
    day = ""
    day_para = None
    cur: dict | None = None

    for para in doc.paragraphs:
        t = (para.text or "").strip()
        if not t:
            continue
        if any(t.startswith(p) for p in SKIP_PREFIX):
            continue
        if DAY_RE.match(t):
            day = t
            day_para = para
            continue
        hm = HDR_RE.match(t)
        if hm:
            cur = {
                "speaker": hm.group(1),
                "time": hm.group(2),
                "day": day,
                "day_para": day_para,
                "hdr_para": para,
                "body_para": None,
                "body": "",
            }
            msgs.append(cur)
            continue
        if cur is not None and para.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
            cur["body"] = t
            cur["body_para"] = para

    return [m for m in msgs if m.get("body")]


def prev_opposite(msgs: list[dict], idx: int) -> int | None:
    sp = msgs[idx]["speaker"]
    day = msgs[idx]["day"]
    for k in range(idx - 1, -1, -1):
        if msgs[k]["speaker"] != sp and msgs[k]["day"] == day:
            return k
    return None


def first_opposite_same_day(msgs: list[dict], idx: int) -> int | None:
    sp = msgs[idx]["speaker"]
    day = msgs[idx]["day"]
    for k in range(idx + 1, len(msgs)):
        if msgs[k]["day"] != day:
            break
        if msgs[k]["speaker"] != sp:
            return k
    return None


def mark_removals(msgs: list[dict]) -> set[int]:
    remove: set[int] = set()

    for i, m in enumerate(msgs):
        if not QUESTION_RE.search(m["body"]):
            continue
        j = first_opposite_same_day(msgs, i)
        if j is None:
            remove.add(i)
            continue
        gap = gap_minutes(m["day"], m["time"], msgs[j]["day"], msgs[j]["time"])
        sim = overlap(m["body"], msgs[j]["body"])
        if gap >= GAP_MINUTES and sim < OVERLAP_MIN:
            remove.add(j)

    for j in range(len(msgs)):
        if j in remove:
            continue
        i = prev_opposite(msgs, j)
        if i is None:
            continue
        gap = gap_minutes(msgs[i]["day"], msgs[i]["time"], msgs[j]["day"], msgs[j]["time"])
        if gap < GAP_MINUTES:
            continue
        sim = overlap(msgs[i]["body"], msgs[j]["body"])
        if sim < OVERLAP_MIN and len(msgs[j]["body"]) <= SHORT_ORPHAN_CHARS:
            remove.add(j)

    for i, m in enumerate(msgs):
        if i in remove or not QUESTION_RE.search(m["body"]):
            continue
        j = first_opposite_same_day(msgs, i)
        if j is None or j in remove:
            remove.add(i)

    return remove


def prune_chapter(path: Path) -> dict:
    doc = Document(str(path))
    msgs = parse_messages(doc)
    remove_idxs = mark_removals(msgs)
    removed_log: list[str] = []

    for idx in sorted(remove_idxs, reverse=True):
        m = msgs[idx]
        removed_log.append(f"{m['day']} {m['speaker']} {m['time']}: {m['body'][:120]}")
        if m.get("body_para"):
            delete_paragraph(m["body_para"])
        if m.get("hdr_para"):
            delete_paragraph(m["hdr_para"])

    kept_days = {m["day"] for i, m in enumerate(msgs) if i not in remove_idxs}
    seen_days: set = set()
    for m in msgs:
        dp = m.get("day_para")
        if dp is None or m["day"] in seen_days:
            continue
        seen_days.add(m["day"])
        if m["day"] not in kept_days:
            delete_paragraph(dp)

    if remove_idxs:
        doc.save(str(path))

    return {
        "file": path.name,
        "before": len(msgs),
        "removed": len(remove_idxs),
        "after": len(msgs) - len(remove_idxs),
        "log": removed_log,
    }


def main() -> None:
    chapters = sorted(BOOK_DIR.glob("Глава_*.docx"))
    lines = [
        "# Удаление реплик без контекстной связи",
        "",
        f"Сгенерировано: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Разрыв ≥{GAP_MINUTES} мин в один день + overlap < {OVERLAP_MIN}: несвязанный ответ на вопрос удаляется.",
        f"- Короткая реплика (≤{SHORT_ORPHAN_CHARS} зн.) без тематической связи с предыдущей репликой другого спикера — удаляется.",
        "- Вопрос без ответа в тот же день — удаляется.",
        "",
        "## Сводка",
        "",
    ]
    total_removed = 0
    all_stats: list[dict] = []

    for path in chapters:
        if path.name.startswith("Глава_00"):
            continue
        stats = prune_chapter(path)
        all_stats.append(stats)
        total_removed += stats["removed"]
        lines.append(
            f"- `{stats['file']}`: {stats['before']} → {stats['after']} "
            f"(удалено {stats['removed']})"
        )

    for stats in all_stats:
        if stats["log"]:
            lines.extend(["", f"### {stats['file']}"])
            for row in stats["log"]:
                lines.append(f"- {row}")

    lines.extend(["", f"**Итого удалено:** {total_removed}"])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"REPORT {REPORT}")
    print(f"TOTAL_REMOVED {total_removed}")
    for stats in all_stats:
        print(f"  {stats['file']}: {stats['before']} -> {stats['after']}")


if __name__ == "__main__":
    main()
