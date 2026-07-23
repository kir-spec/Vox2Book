import os
from pipeline.extractors.auto_extractor import extract_content
from pipeline.cleaner import is_spam_message, clean_whisper_hallucinations
from pipeline.editors.typography import apply_typography
from pipeline.editors.poetry_editor import process_poetry
from pipeline.editors.drama_editor import process_drama
from pipeline.editors.prose_editor import process_prose
from pipeline.editor import proofread_text
from pipeline.validator import validate_quality
from pipeline.builders.docx_builder import build_docx_document
from config import PROJECT_NAME

def process_literature_project(input_path, output_path, genre="auto", target_years=None, title=None, subtitle=None):
    """
    Vox2Book Engine — Universal pipeline entry point processing any literature type
    (prose, poetry, drama, dialogue, academic).
    """
    print(f"=== {PROJECT_NAME} Engine ===")
    print(f"Input path: {input_path}")
    print(f"Target genre: {genre}")
    
    # 1. Extraction & Auto-detection
    raw_elements, final_genre = extract_content(input_path, genre=genre, target_years=target_years)
    print(f"Detected genre: {final_genre}, extracted elements: {len(raw_elements)}")
    
    # 2. Genre-specific editing & typography
    edited_elements = []
    
    if final_genre == 'dialogue':
        for item in raw_elements:
            body = item.get('body', '')
            if is_spam_message(body):
                continue
            body = clean_whisper_hallucinations(body)
            speaker = item.get('speaker', 'Kir')
            body = proofread_text(body, speaker=speaker)
            if body:
                item['edited_body'] = body
                edited_elements.append(item)
    elif final_genre == 'poetry':
        edited_elements = process_poetry(raw_elements)
    elif final_genre == 'drama':
        edited_elements = process_drama(raw_elements)
    else:  # prose / academic
        edited_elements = process_prose(raw_elements)
        
    # 3. Quality Validation
    issues = validate_quality(edited_elements)
    print(f"Validation completed. Issues found: {len(issues)}")
    
    # 4. DOCX Build
    build_docx_document(edited_elements, output_path, genre=final_genre, title=title, subtitle=subtitle)
    print(f"[{PROJECT_NAME} SUCCESS] Processed {len(edited_elements)} elements -> Saved to: {output_path}")
    return edited_elements
