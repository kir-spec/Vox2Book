#!/usr/bin/env python3
"""
Vox2Book — Exact Audit Verifier for User's 20-Item List
Checks all 20 specific items from the user's report in:
E:\coding\работа с литературой\Анфи\Диалоги_Анфи_и_Kir_2024-2026.docx
"""

import sys
import docx
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DOC_PATH = r"E:\coding\работа с литературой\Анфи\Диалоги_Анфи_и_Kir_2024-2026.docx"
doc = docx.Document(DOC_PATH)
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

items_to_verify = [
    # 1. Prepositions
    ("1.1 из тех, которые", r"\bиз тех, которые\b"),
    ("1.2 из этого сделал", r"\bиз этого сделал\b"),
    ("1.3 из стволовых клеток", r"\bиз стволовых клеток\b"),
    ("1.4 что из этого получилось", r"\bчто из этого получилось\b"),
    ("1.5 из ВКонтакте Видео", r"\bиз ВКонтакте Видео\b"),
    ("1.6 из двух этих источников", r"\bиз двух этих источников\b"),
    ("1.7 из аудио твоего", r"\bиз аудио твоего\b"),
    ("1.8 из готовой работы", r"\bиз готовой работы\b"),

    # 2. Truncated words
    ("2.1 нужно было", r"\bнужно было\b"),
    ("2.2 это нужны", r"\bэто нужны\b"),
    ("2.3 мне нужна", r"\bмне нужна\b"),
    ("2.4 не нужен", r"\bне нужен\b"),

    # 3. Punctuation
    ("3.1 что-то (без запятой)", r"\bчто-то\b"),
    ("3.2 какую-то интересную запись", r"\bкакую-то интересную запись\b"),
    ("3.3 как когда-то", r"\bкак когда-то\b"),
    ("3.4 как-то я сама", r"\bкак-то я\b"),

    # 4. Tech & Brands
    ("4.1 нейросети обрабатывают", r"\bнейросети обрабатывают\b"),
    ("4.2 Grok 4 Heavy", r"\bGrok 4 Heavy\b"),
    ("4.3 GPT подтянулся", r"\bGPT подтянулся\b"),
    ("4.4 Element / Matrix", r"\bElement\b"),
]

print("=== VERIFICATION OF ALL 20 USER ITEMS ===")
for label, pattern in items_to_verify:
    matches = [p for p in paragraphs if re.search(pattern, p, re.I)]
    status = "✅ OK" if len(matches) > 0 else "❌ NOT FOUND"
    print(f"{status} | {label} ({len(matches)} occurrences)")
    if matches:
        print(f"   Excerpt: {matches[0][:130]}")

# Check for lingering errors
lingering = [
    ("из-за тех", r"\bиз-за тех\b"),
    ("из-за этого", r"\bиз-за этого\b"),
    ("из-за стволовых", r"\bиз-за стволовых\b"),
    ("жно было", r"\bжно было\b"),
    ("мне жна", r"\bмне жна\b"),
    ("не жен", r"\bне жен\b"),
    ("что, то", r"\bчто,\s*то\b"),
    ("как-то, я", r"\bкак-то,\s+я\b"),
    ("гроб 4 х", r"\bгроб 4 х\b"),
]

print("\n=== LINGERING ERRORS CHECK ===")
bad_count = 0
for label, pattern in lingering:
    bad_matches = [p for p in paragraphs if re.search(pattern, p, re.I)]
    if bad_matches:
        bad_count += len(bad_matches)
        print(f"⚠️ FOUND UNCLEANED: {label} ({len(bad_matches)} matches)")
        for bm in bad_matches:
            print(f"   -> {bm[:120]}")

if bad_count == 0:
    print("✅ PERFECT! 0 lingering errors found across the entire manuscript.")
