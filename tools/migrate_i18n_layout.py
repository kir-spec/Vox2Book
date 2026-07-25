#!/usr/bin/env python3
"""One-off: create prompts/{ru,en,uk} and docs/{ru,en,uk} layout."""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, "prompts")
DOCS = os.path.join(ROOT, "docs")

for lang in ("ru", "en", "uk"):
    os.makedirs(os.path.join(PROMPTS, lang, "profiles"), exist_ok=True)
    os.makedirs(os.path.join(DOCS, lang), exist_ok=True)

pairs = [
    ("prompts/UNIVERSAL_EDITOR_SYSTEM.ru.md", "prompts/ru/UNIVERSAL_EDITOR_SYSTEM.md"),
    ("prompts/UNIVERSAL_EDITOR_SYSTEM.md", "prompts/en/UNIVERSAL_EDITOR_SYSTEM.md"),
]
for src, dst in pairs:
    s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    if os.path.isfile(s):
        shutil.copy2(s, d)

prof_src = os.path.join(PROMPTS, "profiles")
if os.path.isdir(prof_src):
    for name in os.listdir(prof_src):
        shutil.copy2(os.path.join(prof_src, name), os.path.join(PROMPTS, "en", "profiles", name))

for name in ("HOW_TO_WORK.md", "TECHNICAL_SPECIFICATION.md", "USER_GUIDE.md", "PROJECT_STRUCTURE.md"):
    s = os.path.join(DOCS, name)
    if os.path.isfile(s):
        shutil.copy2(s, os.path.join(DOCS, "ru", name))

start_pairs = [
    ("00_START_HERE__СКОПИРУЙ_ПРОМПТ/01_PROMPT_RU__Скопируй_в_чат.md", "prompts/ru/START_USER_PROMPT.md"),
    ("00_START_HERE__СКОПИРУЙ_ПРОМПТ/02_PROMPT_EN__Copy_into_chat.md", "prompts/en/START_USER_PROMPT.md"),
    ("00_START_HERE__СКОПИРУЙ_ПРОМПТ/03_PROMPT_UK__Skopijuj_v_chat.md", "prompts/uk/START_USER_PROMPT.md"),
]
for src, dst in start_pairs:
    s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    if os.path.isfile(s):
        shutil.copy2(s, d)

print("migration copy done")
