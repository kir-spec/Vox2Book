import os
import sys
import argparse

from pipeline.engine import process_literature_project
from pipeline.extractor import extract_and_merge_for_years
from pipeline.cleaner import is_spam_message, clean_whisper_hallucinations
from pipeline.editor import proofread_text
from pipeline.validator import validate_quality
from pipeline.builder import create_book_docx
from config import PROJECT_NAME, PROJECT_DESCRIPTION

sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=f"{PROJECT_NAME} — {PROJECT_DESCRIPTION}")
    parser.add_argument("--input", default=r"A:\ChatExport_2026-07-20", help="Путь к файлу или папке входных данных (.txt, .md, .html, .docx, папка чата)")
    parser.add_argument("--output", default=None, help="Путь к итоговому DOCX файлу")
    parser.add_argument("--genre", default="auto", choices=["auto", "prose", "poetry", "drama", "dialogue", "academic"], help="Жанровый режим обработки")
    parser.add_argument("--title", default=None, help="Заголовок книги / документа")
    parser.add_argument("--subtitle", default=None, help="Подзаголовок книги / документа")
    
    # Backward compatibility options
    parser.add_argument("--export_dir", default=r"A:\ChatExport_2026-07-20", help="Путь к папке экспорта HTML")
    parser.add_argument("--voice_base_dir", default=r"A:\ChatExport_2026-07-20\voice_messages", help="Базовый путь к голосовым транскрипциям")
    parser.add_argument("--years", default=None, help="Года для обработки (например: 2024,2025 или 2026)")
    
    args = parser.parse_args()
    
    # If legacy --years argument is provided
    if args.years:
        years_list = [int(y.strip()) for y in args.years.split(",") if y.strip().isdigit()]
        if not years_list:
            years_list = [2024, 2025]
            
        if not args.output:
            if set(years_list) == {2024, 2025}:
                output_path = r"E:\coding\работа с литературой\Анфи\Голосовые_сообщения_2024-2025.docx"
            elif years_list == [2026]:
                output_path = r"E:\coding\работа с литературой\Анфи\Голосовые_сообщения_2026.docx"
            else:
                output_path = rf"E:\coding\работа с литературой\Анфи\Голосовые_сообщения_{'_'.join(map(str, years_list))}.docx"
        else:
            output_path = args.output
            
        years_str = "–".join(map(str, sorted(years_list))) if len(years_list) > 1 else str(years_list[0])
        sub_title = args.subtitle if args.subtitle else (f"Полная хроника общения ({years_str} гг.)\nСобеседники: Kir и Амфи" if len(years_list) > 1 else f"Полная хроника общения ({years_str} г.)\nСобеседники: Kir и Амфи")
        
        process_literature_project(args.export_dir, output_path, genre="dialogue", target_years=years_list, title=args.title, subtitle=sub_title)
        return
        
    # Default Universal Run
    input_path = args.input
    output_path = args.output if args.output else r"E:\coding\работа с литературой\Анфи\Готовая_Книга.docx"
    
    process_literature_project(input_path, output_path, genre=args.genre, title=args.title, subtitle=args.subtitle)


if __name__ == '__main__':
    main()
