#!/usr/bin/env python3
"""
Vox2Book — Virtual Editorial Board & Neural Pipeline
Multi-Stage Automated Chain of Filters and Virtual Proofreaders:
Stage 1: STT & Slang Purger (Noise & Jargon Cleanup)
Stage 2: Literary Stylist & Rhythm Corrector (Neural LLM Proofreader)
Stage 3: Publisher Typography & Dialogue Corrector (Guillemets, Em-dashes, Particles)
Stage 4: Sentence Cut-off & Quality Auditor
Stage 5: Professional Book Layout Compiler (.docx) -> output/books/
"""

import os
import re
import json
import sys
import urllib.request
import urllib.error

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH


# =====================================================================
# STAGE 1: STT & Technical Slang Purger (Первичный корректор)
# =====================================================================
SLANG_DICTIONARY = [
    (r'\b(те из бы|юсб)\b', 'USB'),
    (r'\b(ссд|с с д)\b', 'SSD-накопитель'),
    (r'\b(а дата|адата)\b', 'ADATA'),
    (r'\b(35 размер|3 5 размер|3,5 размер)\b', '3.5-дюймовый'),
    (r'\b(планктом)\b', 'планктон'),
    (r'\b(в стране джетал|вестерн диджитал)\b', 'Western Digital'),
    (r'\b(трансценд|трансенд)\b', 'Transcend'),
    (r'\b(самсунг)\b', 'Samsung'),
    (r'\b(виндовс|винда)\b', 'Windows'),
]

HALLUCINATIONS = [
    "Quiz河", "DimaTorzok", "Субтитры сделал", "Продолжение следует...",
    "Благодарю за просмотр", "Редактор субтитров", "Подписывайтесь на канал"
]

def stage1_stt_cleanup(raw_text: str) -> str:
    """Stage 1: Removes STT noise, hallucinations, and fixes technical slang."""
    text = raw_text
    for h in HALLUCINATIONS:
        text = text.replace(h, "")
    
    for pattern, replacement in SLANG_DICTIONARY:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
    return text.strip()


# =====================================================================
# STAGE 2: Neural LLM Literary Stylist (Второй корректор — ИИ)
# =====================================================================
SYSTEM_PROMPT = """Ты — главный редактор литературного издательства.
Твоя задача — взять сырую устную расшифровку аудиозаписи (Whisper STT transcript) и превратить её в вычитанный, чистый и грамотный литературный текст.

ПРАВИЛА:
1. Разбей сплошной монолог на логические абзацы и четкие предложения с правильной пунктуацией.
2. Исправь все ошибочные технические термины и оговорки устной речи.
3. Удали слова-паразиты ("ну", "э-э", "как бы", "значит").
4. Сохрани авторский смысл, но сделай стиль литературным.
5. Верни ТОЛЬКО вычитанный готовый текст книги без вводных фраз."""

def stage2_neural_stylist(text: str, config: dict) -> str:
    """Stage 2: Passes text through Neural LLM (OpenAI, DeepSeek, Claude, LM Studio, Ollama)."""
    provider = config.get("api_provider", "openai").lower()
    api_key = config.get("api_key", "").strip() or os.environ.get("OPENAI_API_KEY", "")
    model = config.get("model", "")

    if provider in ["openai", "deepseek", "lmstudio"]:
        if provider == "deepseek":
            url = "https://api.deepseek.com/chat/completions"
            model_name = model or "deepseek-chat"
        elif provider == "lmstudio":
            base_url = config.get("lmstudio_url", "http://localhost:1234").rstrip("/")
            url = f"{base_url}/v1/chat/completions"
            model_name = model or "local-model"
        else:
            url = "https://api.openai.com/v1/chat/completions"
            model_name = model or "gpt-4o-mini"

        if provider != "lmstudio" and (not api_key or "YOUR_API_KEY" in api_key):
            print(f"[Stage 2 Notice] No API Key configured for {provider}. Passing to Stage 3.")
            return text

        headers = {"Content-Type": "application/json"}
        if provider != "lmstudio" and api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[Stage 2 Notice] Neural API ({provider}): {e}. Passing to Stage 3.")
            return text

    elif provider in ["anthropic", "claude"]:
        if not api_key or "YOUR_API_KEY" in api_key:
            print("[Stage 2 Notice] No API Key for Anthropic. Passing to Stage 3.")
            return text
            
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": model or "claude-3-5-sonnet-20240620",
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": text}]
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["content"][0]["text"].strip()
        except Exception as e:
            print(f"[Stage 2 Notice] Anthropic API: {e}. Passing to Stage 3.")
            return text

    elif provider == "ollama":
        ollama_url = config.get("ollama_url", "http://localhost:11434").rstrip("/")
        url = f"{ollama_url}/api/generate"
        payload = {
            "model": model or "llama3",
            "prompt": f"{SYSTEM_PROMPT}\n\nИсходный текст:\n{text}",
            "stream": False
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("response", "").strip()
        except Exception as e:
            print(f"[Stage 2 Notice] Ollama: {e}. Passing to Stage 3.")
            return text

    return text


# =====================================================================
# STAGE 3: Publisher Typography & Dialogue Corrector (Третий корректор)
# =====================================================================
def stage3_publisher_typography(text: str) -> str:
    """Stage 3: Applies Russian publisher typography, guillemets, em-dashes, and particle hyphenation."""
    if not text:
        return ""
    # Guillemets «...»
    text = re.sub(r'"([^"]+)"', r'«\1»', text)
    # Em-dashes
    text = re.sub(r' - ', ' — ', text)
    # Particles
    text = re.sub(r'\b(из|из за)\b', 'из-за', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(из под)\b', 'из-под', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(все таки|всё таки)\b', 'всё-таки', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(в обшем|вобщем)\b', 'в общем', text, flags=re.IGNORECASE)
    return text


# =====================================================================
# STAGE 4: Quality Auditor & Sentence Cut-off Guard (Фильтры валидации)
# =====================================================================
def stage4_quality_auditor(text: str) -> list:
    """Stage 4: Audits text for potential cut-off sentences or missing end punctuation."""
    issues = []
    paragraphs = text.split("\n\n")
    for idx, para in enumerate(paragraphs):
        para_clean = para.strip()
        if para_clean and not para_clean[-1] in ['.', '!', '?', '…', '»', ':']:
            issues.append(f"Paragraph #{idx+1} ends without terminal punctuation: '{para_clean[-30:]}'")
    return issues


# =====================================================================
# STAGE 5: Professional Book Layout Compiler (Верстальщик DOCX)
# =====================================================================
def stage5_build_docx(text: str, output_path: str, title: str = ""):
    """Stage 5: Compiles manuscript DOCX into output/books/."""
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title Page
    if title:
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_title.add_run(title)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(24)
        run.font.bold = True
        doc.add_paragraph()

    # Process Body Paragraphs
    paragraphs = text.split("\n\n")
    for para_str in paragraphs:
        para_clean = para_str.strip()
        if not para_clean:
            continue
            
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15

        # Format dialogues
        if para_clean.startswith("-") or para_clean.startswith("—"):
            para_clean = "— " + para_clean.lstrip("-—").strip()

        run = p.add_run(para_clean)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"✨ [SUCCESS] Finished Manuscript compiled to: '{output_path}'")


# =====================================================================
# AUTOMATED PIPELINE EXECUTION ENGINE
# =====================================================================
def process_manuscript_chain(input_path: str = None, output_path: str = None):
    """Runs the complete multi-stage proofreading pipeline chain."""
    os.makedirs("inputs/raw_texts", exist_ok=True)
    os.makedirs("inputs/audio", exist_ok=True)
    os.makedirs("output/books", exist_ok=True)

    config_path = "config.json"
    if not os.path.exists(config_path):
        default_config = {
            "api_provider": "openai",
            "api_key": os.environ.get("OPENAI_API_KEY", ""),
            "model": "gpt-4o-mini",
            "ollama_url": "http://localhost:11434",
            "lmstudio_url": "http://localhost:1234",
            "genre": "prose",
            "title": "",
            "subtitle": ""
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if not input_path:
        raw_files = [os.path.join("inputs/raw_texts", f) for f in os.listdir("inputs/raw_texts") if f.endswith(('.txt', '.md', '.docx'))]
        if raw_files:
            input_path = raw_files[0]
        else:
            input_path = "inputs/raw_texts/sample.txt"
            with open(input_path, "w", encoding="utf-8") as f:
                f.write("Поместите ваш текст сюда.")

    if not output_path:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join("output/books", f"{base_name}.docx")

    print(f"--- 🎭 Starting Virtual Editorial Board Chain ---")
    print(f"Input: '{input_path}' -> Target Output: '{output_path}'")

    # Read Input
    raw_bytes = open(input_path, "rb").read()
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw_text = raw_bytes.decode("cp1251", errors="ignore")

    # Pipeline Chain Execution
    print("Stage 1/5: Purging STT noise & technical slang...")
    text_s1 = stage1_stt_cleanup(raw_text)

    print(f"Stage 2/5: Neural LLM Proofreading ({config.get('api_provider')})...")
    text_s2 = stage2_neural_stylist(text_s1, config)

    print("Stage 3/5: Publisher Typography & Dialogue Formatting...")
    text_s3 = stage3_publisher_typography(text_s2)

    print("Stage 4/5: Quality Auditor & Sentence Cut-off Check...")
    issues = stage4_quality_auditor(text_s3)
    if issues:
        print(f"  [Auditor Warning] Found {len(issues)} potential cut-off issues.")
    else:
        print("  [Auditor OK] Quality audit passed with 0 issues.")

    print("Stage 5/5: Compiling DOCX Manuscript...")
    stage5_build_docx(text_s3, output_path, config.get("title", ""))

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else None
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    process_manuscript_chain(in_file, out_file)
