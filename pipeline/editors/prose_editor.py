import re
from pipeline.editors.typography import apply_typography

def process_prose(elements):
    """
    Processes prose elements: Chapters, paragraphs, dialogues formatting.
    """
    processed = []
    
    for item in elements:
        itype = item.get('type')
        body = item.get('body', '').strip()
        
        if not body:
            continue
            
        body = apply_typography(body)
        
        if itype == 'heading':
            processed.append({'type': 'heading', 'body': body})
            continue
            
        # Format dialogue line if starts with dash
        if body.startswith('—') or body.startswith('-'):
            body = re.sub(r'^[—\-]\s*', '— ', body)
            
        if body and body[0].islower():
            body = body[0].upper() + body[1:]
            
        if not body.endswith(('.', '!', '?', '...')):
            body += '.'
            
        processed.append({
            'type': 'paragraph',
            'body': body
        })
        
    return processed
