import re
from pipeline.editors.typography import apply_typography

def process_poetry(elements):
    """
    Processes poetry elements: line stanzas, rhythmic punctuation, verse capitalization.
    """
    processed = []
    
    for item in elements:
        itype = item.get('type')
        body = item.get('body', '').strip()
        
        if itype == 'stanza_break':
            processed.append({'type': 'stanza_break', 'body': ''})
            continue
            
        if not body:
            continue
            
        # Apply typography
        body = apply_typography(body)
        
        # Capitalize first letter of verse line
        if body and body[0].islower():
            body = body[0].upper() + body[1:]
            
        processed.append({
            'type': 'verse_line' if itype != 'heading' else 'heading',
            'body': body
        })
        
    return processed
