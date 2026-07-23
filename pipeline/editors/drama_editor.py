import re
from pipeline.editors.typography import apply_typography

def process_drama(elements):
    """
    Processes drama elements: Character names (CAPS/Bold), stage directions (italics/brackets).
    """
    processed = []
    
    for item in elements:
        itype = item.get('type')
        body = item.get('body', '').strip()
        speaker = item.get('speaker')
        
        if not body:
            continue
            
        body = apply_typography(body)
        
        if itype == 'character_name':
            body_caps = body.upper()
            if not body_caps.endswith('.'):
                body_caps += '.'
            processed.append({
                'type': 'character_name',
                'body': body_caps,
                'speaker': speaker
            })
        elif itype == 'stage_direction':
            if not body.startswith('('):
                body = f"({body})"
            processed.append({
                'type': 'stage_direction',
                'body': body
            })
        else:
            if body and body[0].islower():
                body = body[0].upper() + body[1:]
            if not body.endswith(('.', '!', '?', '...')):
                body += '.'
            processed.append({
                'type': 'paragraph',
                'body': body,
                'speaker': speaker
            })
            
    return processed
