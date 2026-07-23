import json
import os
import sys
import subprocess

def main():
    print("=========================================================")
    print("   📚 Vox2Book — Direct Neural API Pipeline Launcher    ")
    print("=========================================================")

    config_path = "config.json"
    if not os.path.exists(config_path):
        default_config = {
            "api_provider": "openai",
            "api_key": os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"),
            "model": "gpt-4o-mini",
            "ollama_url": "http://localhost:11434",
            "genre": "prose",
            "title": "",
            "subtitle": ""
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        print(f"Created default configuration: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    print(f"Config Loaded -> Provider: {config.get('api_provider')}, Model: {config.get('model')}")

    input_file = sys.argv[1] if len(sys.argv) > 1 else "audio_1458@01-06-2026_22-44-40.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output/book_api_processed.docx"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    print(f"Processing input file: '{input_file}' -> Output: '{output_file}'")

    # Run compiled vox2book binary in CLI mode
    exe_cmd = ["vox2book.exe", "--input", input_file, "--output", output_file, "--cli"]
    if os.path.exists("vox2book.exe"):
        res = subprocess.run(exe_cmd)
        if res.returncode == 0:
            print(f"\n✅ [SUCCESS] Processing complete! DOCX manuscript saved to: {output_file}")
        else:
            print("\n❌ Error during processing.")
    else:
        print("Running cargo run -- --cli ...")
        res = subprocess.run(["cargo", "run", "--", "--input", input_file, "--output", output_file, "--cli"])

if __name__ == "__main__":
    main()
