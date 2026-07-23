import os
import glob
from pipeline.extractors.text_reader import read_plain_text_file
from pipeline.extractor import extract_and_merge_for_years

def extract_content(input_path, genre="auto", target_years=None, speaker_mapping=None):
    """
    Universal extractor entry point.
    Determines input type (directory vs file; HTML vs STT TXT vs Plain Text vs Markdown).
    Returns: (elements_list, genre)
    """
    if os.path.isdir(input_path):
        # Check if it's a Telegram HTML export directory or voice directory
        html_files = glob.glob(os.path.join(input_path, "messages*.html"))
        if html_files or "voice_messages" in os.listdir(input_path):
            voice_dir = os.path.join(input_path, "voice_messages") if os.path.exists(os.path.join(input_path, "voice_messages")) else input_path
            years = target_years if target_years else [2024, 2025, 2026]
            raw_msgs = extract_and_merge_for_years(input_path, voice_dir, target_years=years, include_text_msgs=True)
            elements = []
            for m in raw_msgs:
                elements.append({
                    'type': 'message',
                    'speaker': m.get('speaker', 'Unknown'),
                    'time_str': m.get('time_str', '00:00'),
                    'msg_type': m.get('type', 'voice'),
                    'dt': m.get('dt'),
                    'body': m.get('body', '')
                })
            return elements, 'dialogue'
            
    # File handling (.txt, .md, .html, .docx)
    if os.path.isfile(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext in ('.txt', '.md'):
            elements, detected_genre = read_plain_text_file(input_path, default_genre=genre)
            final_genre = genre if genre and genre != 'auto' else detected_genre
            return elements, final_genre
            
    # Default empty
    return [], genre if genre else 'prose'
