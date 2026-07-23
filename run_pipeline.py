import os
import sys
import argparse

from pipeline.engine import process_literature_project
from pipeline.cleaner import is_spam_message, clean_whisper_hallucinations
from pipeline.editor import proofread_text
from pipeline.validator import validate_quality
from config import PROJECT_NAME, PROJECT_DESCRIPTION

sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=f"{PROJECT_NAME} — {PROJECT_DESCRIPTION}")
    parser.add_argument("--input", default=None, help="Путь к файлу или папке входных данных (.txt, .md, .html, .docx, папка чата)")
    parser.add_argument("--output", default="output/book.docx", help="Путь к итоговому DOCX файлу")
    parser.add_argument("--genre", default="auto", choices=["auto", "prose", "poetry", "drama", "dialogue", "academic"], help="Жанровый режим обработки")
    parser.add_argument("--title", default=None, help="Заголовок книги / документа")
    parser.add_argument("--subtitle", default=None, help="Подзаголовок книги / документа")
    parser.add_argument("--speaker-map", default=None, help="Маппинг имен спикеров в формате 'Raw1=Name1,Raw2=Name2'")
    
    args = parser.parse_args()
    
    if not args.input:
        print("Пожалуйста, укажите входной файл или папку через аргумент --input")
        print("Пример: python run_pipeline.py --input book.txt --genre prose --output output/book.docx")
        sys.exit(1)
        
    speaker_mapping = None
    if args.speaker_map:
        speaker_mapping = {}
        pairs = args.speaker_map.split(",")
        for pair in pairs:
            if "=" in pair:
                k, v = pair.split("=", 1)
                speaker_mapping[k.strip()] = v.strip()
                
    process_literature_project(args.input, args.output, genre=args.genre, title=args.title, subtitle=args.subtitle)


if __name__ == '__main__':
    main()
