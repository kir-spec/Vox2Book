import json
import os
import sys
import subprocess

def main():
    print("=========================================================")
    print("   📚 Vox2Book — Direct Neural API Pipeline Launcher    ")
    print("=========================================================")

    # Ensure required folder structure exists
    os.makedirs("inputs/raw_texts", exist_ok=True)
    os.makedirs("inputs/audio", exist_ok=True)
    os.makedirs("output/books", exist_ok=True)

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

    # Determine input file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Pick first available file in inputs/raw_texts/ or fallback
        raw_files = [os.path.join("inputs/raw_texts", f) for f in os.listdir("inputs/raw_texts") if f.endswith(('.txt', '.md', '.docx'))]
        if raw_files:
            input_file = raw_files[0]
        else:
            input_file = "inputs/raw_texts/sample.txt"
            with open(input_file, "w", encoding="utf-8") as f:
                f.write("Поместите ваш исходный текст сюда.")

    # Determine output file path
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join("output/books", f"{base_name}_manuscript.docx")

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
