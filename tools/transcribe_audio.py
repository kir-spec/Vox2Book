#!/usr/bin/env python3
"""
Vox2Book — local speech-to-text (faster-whisper / OpenAI Whisper).
Also supports external STT: OpenAI API, AssemblyAI, Deepgram, Telegram export, etc.
See docs/*/AUDIO_TRANSCRIPTION.md for the full list.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 console on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "transcribe.json"
EXAMPLE_CONFIG = PROJECT_ROOT / "config" / "transcribe.example.json"
DEFAULT_AUDIO_DIR = PROJECT_ROOT / "inputs" / "audio"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "inputs" / "raw_texts"

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".opus", ".flac", ".webm", ".mp4", ".mkv", ".aac", ".wma"}

MODELS = [
    ("tiny", "Самая быстрая, низкое качество. Только для теста."),
    ("base", "Быстро, слабое качество на русском."),
    ("small", "Баланс на CPU без GPU."),
    ("medium", "Хорошо для русского/украинского на среднем GPU или терпеливом CPU."),
    ("large-v3", "Максимальное качество OpenAI Whisper v3."),
    ("large-v3-turbo", "Лучший баланс скорость/качество (рекомендуется при наличии GPU)."),
    ("distil-large-v3", "Облегчённый large — быстрее, чуть ниже качество."),
]

BACKENDS = ("faster-whisper", "whisper")


def load_config(path: Path | None) -> dict:
    cfg_path = path or DEFAULT_CONFIG
    if cfg_path.is_file():
        with open(cfg_path, encoding="utf-8") as f:
            return json.load(f)
    if EXAMPLE_CONFIG.is_file():
        with open(EXAMPLE_CONFIG, encoding="utf-8") as f:
            return json.load(f)
    return {}


def resolve_device(device: str) -> str:
    if device and device != "auto":
        return device
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda"
    except Exception:
        pass
    return "cpu"


def resolve_compute_type(device: str, compute_type: str) -> str:
    if compute_type and compute_type != "auto":
        return compute_type
    return "float16" if device == "cuda" else "int8"


def collect_audio_paths(target: Path) -> list[Path]:
    if target.is_file():
        if target.suffix.lower() not in AUDIO_EXTENSIONS:
            raise SystemExit(f"Unsupported audio format: {target.suffix}")
        return [target]
    if not target.is_dir():
        raise SystemExit(f"Path not found: {target}")
    files = sorted(
        p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    )
    if not files:
        raise SystemExit(f"No audio files in {target} (supported: {', '.join(sorted(AUDIO_EXTENSIONS))})")
    return files


def pip_install_requirements() -> None:
    req = PROJECT_ROOT / "requirements-transcribe.txt"
    if not req.is_file():
        raise SystemExit(f"Missing {req}")
    print("Installing transcription dependencies (may take several minutes)…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])
    print("Done. Run transcribe again.")


def print_models() -> None:
    print("Available Whisper model sizes:\n")
    for name, note in MODELS:
        print(f"  {name:18} — {note}")
    print("\nBackends:")
    print("  faster-whisper  — recommended (VAD, GPU, less hallucination)")
    print("  whisper         — original openai-whisper (pip install openai-whisper)")


def transcribe_faster_whisper(
    audio_path: Path,
    *,
    model: str,
    language: str | None,
    device: str,
    compute_type: str,
    vad_filter: bool,
    initial_prompt: str | None,
) -> tuple[str, list[dict], str]:
    from faster_whisper import WhisperModel

    device = resolve_device(device)
    compute_type = resolve_compute_type(device, compute_type)
    print(f"  backend=faster-whisper model={model} device={device} compute={compute_type}")

    whisper = WhisperModel(model, device=device, compute_type=compute_type)
    segments_iter, info = whisper.transcribe(
        str(audio_path),
        language=language or None,
        vad_filter=vad_filter,
        initial_prompt=initial_prompt or None,
        condition_on_previous_text=False,
    )
    segments: list[dict] = []
    parts: list[str] = []
    for seg in segments_iter:
        text = (seg.text or "").strip()
        if text:
            parts.append(text)
            segments.append({"start": seg.start, "end": seg.end, "text": text})
    detected = getattr(info, "language", None) or language or "?"
    header_lang = detected
    return "\n".join(parts), segments, header_lang


def transcribe_openai_whisper(
    audio_path: Path,
    *,
    model: str,
    language: str | None,
    initial_prompt: str | None,
) -> tuple[str, list[dict], str]:
    import whisper

    print(f"  backend=whisper model={model}")
    whisper_model = whisper.load_model(model)
    kwargs: dict = {"verbose": False}
    if language:
        kwargs["language"] = language
    if initial_prompt:
        kwargs["initial_prompt"] = initial_prompt
    result = whisper_model.transcribe(str(audio_path), **kwargs)
    segments = [
        {"start": s.get("start"), "end": s.get("end"), "text": (s.get("text") or "").strip()}
        for s in result.get("segments", [])
    ]
    text = (result.get("text") or "").strip()
    return text, segments, result.get("language") or language or "?"


def write_transcript(
    audio_path: Path,
    text: str,
    segments: list[dict],
    *,
    output_dir: Path,
    backend: str,
    model: str,
    language: str,
    write_json: bool,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    out_txt = output_dir / f"{stem}.txt"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = (
        f"# Vox2Book transcript\n"
        f"# source: {audio_path.name}\n"
        f"# backend: {backend} | model: {model} | language: {language}\n"
        f"# created: {ts}\n"
        f"# --- edit below for literary pipeline (inputs/raw_texts → output/books) ---\n\n"
    )
    out_txt.write_text(header + text + "\n", encoding="utf-8")
    if write_json:
        out_json = output_dir / f"{stem}.segments.json"
        out_json.write_text(json.dumps(segments, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_txt


def process_one(audio_path: Path, cfg: dict, args: argparse.Namespace) -> Path:
    backend = args.backend or cfg.get("backend", "faster-whisper")
    model = args.model or cfg.get("model", "large-v3-turbo")
    language = args.language or cfg.get("language") or None
    if language == "auto":
        language = None
    device = args.device or cfg.get("device", "auto")
    compute_type = args.compute_type or cfg.get("compute_type", "auto")
    vad_filter = not args.no_vad and cfg.get("vad_filter", True)
    initial_prompt = args.prompt or cfg.get("initial_prompt") or None
    output_dir = Path(args.output_dir or cfg.get("output_dir", str(DEFAULT_OUTPUT_DIR)))
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir

    print(f"\n▶ {audio_path.name}")
    if backend == "faster-whisper":
        text, segments, lang = transcribe_faster_whisper(
            audio_path,
            model=model,
            language=language,
            device=device,
            compute_type=compute_type,
            vad_filter=vad_filter,
            initial_prompt=initial_prompt,
        )
    elif backend == "whisper":
        text, segments, lang = transcribe_openai_whisper(
            audio_path,
            model=model,
            language=language,
            initial_prompt=initial_prompt,
        )
    else:
        raise SystemExit(f"Unknown backend: {backend}")

    out = write_transcript(
        audio_path,
        text,
        segments,
        output_dir=output_dir,
        backend=backend,
        model=model,
        language=lang,
        write_json=args.json,
    )
    print(f"  → {out.relative_to(PROJECT_ROOT)} ({len(text)} chars)")
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Vox2Book: local STT (faster-whisper) → inputs/raw_texts/. See docs/*/AUDIO_TRANSCRIPTION.md for other transcribers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python tools/transcribe_audio.py --install\n"
            "  python tools/transcribe_audio.py inputs/audio/interview.mp3\n"
            "  python tools/transcribe_audio.py inputs/audio/ --model large-v3 --language ru\n"
            "  python tools/transcribe_audio.py voice.ogg --backend whisper --model medium\n"
        ),
    )
    p.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_AUDIO_DIR),
        help=f"Audio file or folder (default: {DEFAULT_AUDIO_DIR.relative_to(PROJECT_ROOT)})",
    )
    p.add_argument("--config", type=Path, default=None, help="Path to config/transcribe.json")
    p.add_argument("--backend", choices=BACKENDS, help="faster-whisper (default) or whisper")
    p.add_argument("--model", help="Whisper model size (see --list-models)")
    p.add_argument("--language", help="ISO code: ru, en, uk, or auto")
    p.add_argument("--device", choices=("auto", "cpu", "cuda"), help="Inference device")
    p.add_argument("--compute-type", dest="compute_type", help="e.g. float16, int8 (faster-whisper)")
    p.add_argument("--output-dir", dest="output_dir", help="Output folder (default: inputs/raw_texts)")
    p.add_argument("--prompt", help="initial_prompt: names, terms, expected vocabulary")
    p.add_argument("--no-vad", action="store_true", help="Disable VAD filter (faster-whisper)")
    p.add_argument("--json", action="store_true", help="Also write .segments.json with timestamps")
    p.add_argument("--install", action="store_true", help="pip install -r requirements-transcribe.txt")
    p.add_argument("--list-models", action="store_true", help="Show model recommendations")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.list_models:
        print_models()
        return 0
    if args.install:
        pip_install_requirements()
        return 0

    cfg = load_config(args.config)
    target = Path(args.path)
    if not target.is_absolute():
        target = PROJECT_ROOT / target

    try:
        audio_files = collect_audio_paths(target)
    except SystemExit as e:
        print(e, file=sys.stderr)
        print(
            "\nTip: run once with --install, then put audio in inputs/audio/\n"
            "Docs: docs/ru/AUDIO_TRANSCRIPTION.md",
            file=sys.stderr,
        )
        return 1

    print(f"Vox2Book transcribe — {len(audio_files)} file(s)")
    outputs: list[Path] = []
    for audio in audio_files:
        try:
            outputs.append(process_one(audio, cfg, args))
        except ModuleNotFoundError as e:
            print(f"\nMissing dependency: {e}", file=sys.stderr)
            print("Run:  python tools/transcribe_audio.py --install", file=sys.stderr)
            return 1

    print("\n✓ Transcripts ready for literary editing:")
    for o in outputs:
        print(f"  {o}")
    print("\nNext: open prompts/ru/START_USER_PROMPT.md (or en/uk) and run Vox2Book on the .txt file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
