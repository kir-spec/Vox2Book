#!/usr/bin/env python3
"""
Vox2Book — local speech-to-text (Parakeet / faster-whisper / OpenAI Whisper).
Also supports external STT: OpenAI API, AssemblyAI, Deepgram, Telegram export, etc.
See docs/*/AUDIO_TRANSCRIPTION.md for the full list.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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

BACKENDS = ("parakeet", "faster-whisper", "whisper")
PARAKEET_MODEL_ID = "nemo-parakeet-tdt-0.6b-v3"
DEFAULT_PARAKEET_MODEL_DIR = PROJECT_ROOT / "models" / "parakeet-tdt-0.6b-v3-int8"

_PARAKEET_MODEL: Any = None
_PARAKEET_VAD: Any = None


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


def pip_install_requirements(parakeet: bool = False) -> None:
    req = PROJECT_ROOT / (
        "requirements-transcribe-parakeet.txt" if parakeet else "requirements-transcribe.txt"
    )
    if not req.is_file():
        raise SystemExit(f"Missing {req}")
    label = "Parakeet (onnx-asr)" if parakeet else "Whisper"
    print(f"Installing {label} dependencies (may take several minutes)…")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])
    print("Done. Run transcribe again.")


def print_models() -> None:
    print("Backends:\n")
    print("  parakeet        — NVIDIA Parakeet TDT 0.6B v3 (NOT Whisper)")
    print("                    ru/uk/en + 22 EU langs, punctuation, CPU int8, ~17× faster than Whisper large")
    print("  faster-whisper  — OpenAI Whisper via CTranslate2 (GPU/CUDA)")
    print("  whisper         — original openai-whisper\n")
    print("Whisper model sizes (--backend faster-whisper / whisper):\n")
    for name, note in MODELS:
        print(f"  {name:18} — {note}")


def load_audio_mono_f32(audio_path: Path, sample_rate: int = 16000) -> Any:
    import numpy as np

    cmd = [
        "ffmpeg",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(audio_path),
        "-f",
        "f32le",
        "-acodec",
        "pcm_f32le",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "pipe:1",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or b"").decode("utf-8", errors="replace").strip()
        raise SystemExit(f"ffmpeg failed for {audio_path.name}: {stderr or e}") from e
    if not proc.stdout:
        raise SystemExit(f"No audio decoded from {audio_path}")
    return np.frombuffer(proc.stdout, dtype=np.float32).copy()


def get_parakeet_model(model_dir: Path, quantization: str) -> Any:
    global _PARAKEET_MODEL
    if _PARAKEET_MODEL is None:
        import onnx_asr

        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"  loading Parakeet from {model_dir} (quantization={quantization})…")
        _PARAKEET_MODEL = onnx_asr.load_model(
            PARAKEET_MODEL_ID,
            model_dir,
            quantization=quantization,
        )
    return _PARAKEET_MODEL


def get_parakeet_vad() -> Any:
    global _PARAKEET_VAD
    if _PARAKEET_VAD is None:
        import onnx_asr

        _PARAKEET_VAD = onnx_asr.load_vad("silero")
    return _PARAKEET_VAD


def transcribe_parakeet(
    audio_path: Path,
    *,
    model_dir: Path,
    quantization: str,
    language: str | None,
    vad_filter: bool,
) -> tuple[str, list[dict], str]:
    model = get_parakeet_model(model_dir, quantization)
    print(f"  backend=parakeet model={PARAKEET_MODEL_ID} quantization={quantization}")
    audio = load_audio_mono_f32(audio_path)
    recognize_kwargs: dict[str, str] = {}
    if language:
        recognize_kwargs["language"] = language

    parts: list[str] = []
    segments: list[dict] = []

    if vad_filter:
        adapter = model.with_vad(get_parakeet_vad(), batch_size=1)
        results = adapter.recognize(audio, **recognize_kwargs)
        # onnx_asr 0.12 yields a single SegmentResult per VAD segment (not batches)
        if not isinstance(results, list):
            results = [results]
        for seg in results:
            # tolerate a nested list/batch shape defensively
            if isinstance(seg, (list, tuple)):
                inner = seg
            else:
                inner = [seg]
            for s in inner:
                text = (getattr(s, "text", "") or "").strip()
                if text:
                    parts.append(text)
                    segments.append(
                        {"start": getattr(s, "start", None), "end": getattr(s, "end", None), "text": text}
                    )
    else:
        text = (model.recognize(audio, **recognize_kwargs) or "").strip()
        if text:
            parts.append(text)

    lang_display = language or "auto"
    return "\n".join(parts), segments, lang_display


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
    backend = args.backend or cfg.get("backend", "parakeet")
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
    parakeet_model_dir = Path(
        args.parakeet_model_dir or cfg.get("parakeet_model_dir", str(DEFAULT_PARAKEET_MODEL_DIR))
    )
    if not parakeet_model_dir.is_absolute():
        parakeet_model_dir = PROJECT_ROOT / parakeet_model_dir
    parakeet_quant = args.parakeet_quantization or cfg.get("parakeet_quantization", "int8")

    print(f"\n▶ {audio_path.name}")
    if backend == "parakeet":
        text, segments, lang = transcribe_parakeet(
            audio_path,
            model_dir=parakeet_model_dir,
            quantization=parakeet_quant,
            language=language,
            vad_filter=vad_filter,
        )
        model_label = f"{PARAKEET_MODEL_ID}-{parakeet_quant}"
    elif backend == "faster-whisper":
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
        model=model_label if backend == "parakeet" else model,
        language=lang,
        write_json=args.json,
    )
    print(f"  → {out.relative_to(PROJECT_ROOT)} ({len(text)} chars)")
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Vox2Book: local STT (Parakeet / faster-whisper) → inputs/raw_texts/. See docs/*/AUDIO_TRANSCRIPTION.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python tools/transcribe_audio.py --install-parakeet\n"
            "  python tools/transcribe_audio.py inputs/audio/voice.ogg --backend parakeet --language ru\n"
            "  python tools/transcribe_audio.py inputs/audio/ --backend parakeet\n"
            "  python tools/transcribe_audio.py --install\n"
            "  python tools/transcribe_audio.py inputs/audio/ --backend faster-whisper --model large-v3-turbo\n"
        ),
    )
    p.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_AUDIO_DIR),
        help=f"Audio file or folder (default: {DEFAULT_AUDIO_DIR.relative_to(PROJECT_ROOT)})",
    )
    p.add_argument("--config", type=Path, default=None, help="Path to config/transcribe.json")
    p.add_argument("--backend", choices=BACKENDS, help="parakeet (default), faster-whisper, or whisper")
    p.add_argument("--model", help="Whisper model size when using whisper backends (see --list-models)")
    p.add_argument(
        "--parakeet-model-dir",
        dest="parakeet_model_dir",
        help="Parakeet ONNX cache dir (default: models/parakeet-tdt-0.6b-v3-int8)",
    )
    p.add_argument(
        "--parakeet-quantization",
        dest="parakeet_quantization",
        default=None,
        help="Parakeet quantization: int8 (CPU default) or fp16",
    )
    p.add_argument("--language", help="ISO code: ru, en, uk, or auto")
    p.add_argument("--device", choices=("auto", "cpu", "cuda"), help="Inference device")
    p.add_argument("--compute-type", dest="compute_type", help="e.g. float16, int8 (faster-whisper)")
    p.add_argument("--output-dir", dest="output_dir", help="Output folder (default: inputs/raw_texts)")
    p.add_argument("--prompt", help="initial_prompt: names, terms, expected vocabulary")
    p.add_argument("--no-vad", action="store_true", help="Disable VAD filter (faster-whisper)")
    p.add_argument("--json", action="store_true", help="Also write .segments.json with timestamps")
    p.add_argument("--install", action="store_true", help="pip install Whisper stack (requirements-transcribe.txt)")
    p.add_argument(
        "--install-parakeet",
        action="store_true",
        help="pip install Parakeet stack (requirements-transcribe-parakeet.txt)",
    )
    p.add_argument("--list-models", action="store_true", help="Show model recommendations")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.list_models:
        print_models()
        return 0
    if args.install_parakeet:
        pip_install_requirements(parakeet=True)
        return 0
    if args.install:
        pip_install_requirements(parakeet=False)
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
            if (args.backend or cfg.get("backend", "parakeet")) == "parakeet":
                print("Run:  python tools/transcribe_audio.py --install-parakeet", file=sys.stderr)
            else:
                print("Run:  python tools/transcribe_audio.py --install", file=sys.stderr)
            return 1

    print("\n✓ Transcripts ready for literary editing:")
    for o in outputs:
        print(f"  {o}")
    print("\nNext: open prompts/ru/START_USER_PROMPT.md (or en/uk) and run Vox2Book on the .txt file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
