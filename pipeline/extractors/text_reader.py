import os
import re

def read_plain_text_file(filepath, default_genre=None):
    """
    Reads plain text or markdown files (.txt, .md).
    Detects genre if default_genre is auto or None (prose vs poetry vs drama).
    Returns list of element dicts:
      {'type': 'heading'|'paragraph'|'verse_line'|'stanza_break'|'stage_direction'|'character_name',
       'body': text, 'speaker': name_if_any}
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        
    elements = []
    
    # Check genre auto-detection hints
    has_verse_stanzas = False
    blank_lines = 0
    short_lines = 0
    drama_character_lines = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
        else:
            if len(stripped) < 50:
                short_lines += 1
            if re.match(r'^[A-ZА-ЯЁ\s]{2,30}[:.]', stripped):
                drama_character_lines += 1

    detected_genre = default_genre
    if not detected_genre or detected_genre == 'auto':
        if drama_character_lines > 5 and drama_character_lines / max(1, len(lines)) > 0.1:
            detected_genre = 'drama'
        elif short_lines > 10 and blank_lines > 5 and (short_lines + blank_lines) / max(1, len(lines)) > 0.5:
            detected_genre = 'poetry'
        else:
            detected_genre = 'prose'
            
    # Parse elements based on detected_genre
    in_stanza = False
    
    for idx, line in enumerate(lines):
        raw_line = line.rstrip('\r\n')
        stripped = raw_line.strip()
        
        if not stripped:
            if detected_genre == 'poetry':
                elements.append({'type': 'stanza_break', 'body': ''})
            continue
            
        # Check headings / chapter markers
        if re.match(r'^(#+\s*|Глава\s+\d+|Часть\s+\d+|Акт\s+\d+|Сцена\s+\d+|Chapter\s+\d+)', stripped, re.IGNORECASE):
            clean_heading = re.sub(r'^#+\s*', '', stripped)
            elements.append({'type': 'heading', 'body': clean_heading})
            continue
            
        if detected_genre == 'poetry':
            elements.append({'type': 'verse_line', 'body': stripped})
        elif detected_genre == 'drama':
            # Check character name line e.g. "КИР:" or "АНФИЯ (входит):"
            char_match = re.match(r'^([A-ZА-ЯЁ\s]{2,30})\s*(?:\((.*?)\))?[:.](.*)$', stripped)
            if char_match:
                cname, sdir, dialogue = char_match.groups()
                elements.append({'type': 'character_name', 'body': cname.strip(), 'speaker': cname.strip()})
                if sdir:
                    elements.append({'type': 'stage_direction', 'body': f"({sdir.strip()})"})
                if dialogue.strip():
                    elements.append({'type': 'paragraph', 'body': dialogue.strip(), 'speaker': cname.strip()})
            elif stripped.startswith('(') and stripped.endswith(')'):
                elements.append({'type': 'stage_direction', 'body': stripped})
            else:
                elements.append({'type': 'paragraph', 'body': stripped})
        else:  # prose
            elements.append({'type': 'paragraph', 'body': stripped})
            
    return elements, detected_genre
