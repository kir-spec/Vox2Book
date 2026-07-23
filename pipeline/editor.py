import re

def proofread_text(text, speaker="Kir"):
    """
    Performs literary proofreading, typography formatting, punctuation, 
    and gender agreement for a transcript paragraph.
    """
    if not text:
        return ""
        
    # Remove stutters (duplicated words)
    text = re.sub(r'\b([а-яА-Яa-zA-Z]+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    
    # Hyphenated particles: -то, -нибудь, всё-таки, из-за, из-под, более-менее
    text = re.sub(r'\b(кое|где|кто|что|когда|как|куда)\s+то\b', r'\1-то', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(где|кто|что|когда|как|куда)\s+нибудь\b', r'\1-нибудь', text, flags=re.IGNORECASE)
    text = re.sub(r'\bвсё\s+таки\b', 'всё-таки', text, flags=re.IGNORECASE)
    text = re.sub(r'\bвсе\s+таки\b', 'всё-таки', text, flags=re.IGNORECASE)
    text = re.sub(r'\bиз\s+за\b', 'из-за', text, flags=re.IGNORECASE)
    text = re.sub(r'\bиз\s+под\b', 'из-под', text, flags=re.IGNORECASE)
    text = re.sub(r'\bболее\s+менее\b', 'более-менее', text, flags=re.IGNORECASE)
    
    # Separate spelling for introductory phrases
    text = re.sub(r'\bвобщем\b', 'в общем', text, flags=re.IGNORECASE)
    text = re.sub(r'\bвобщем\b', 'в общем', text, flags=re.IGNORECASE)
    text = re.sub(r'\bтоесть\b', 'то есть', text, flags=re.IGNORECASE)
    text = re.sub(r'\bврядли\b', 'вряд ли', text, flags=re.IGNORECASE)
    text = re.sub(r'\bкакбудто\b', 'как будто', text, flags=re.IGNORECASE)
    
    # Russian Guillemets «...»
    text = re.sub(r'(\s|^)"([^"]+)"(\s|[.,!?:;]|$)', r'\1«\2»\3', text)
    
    # Em-dash
    text = re.sub(r'(\s+)-\s+', r' — ', text)
    
    # Commas before conjunctions if missing (common conjunctions: что, чтобы, потому что, если, когда, но, а)
    text = re.sub(r'(?<![.,!?:;—\s])\s+(что|чтобы|потому что|так как|если|когда|который|которая|которое|которые)\b', r', \1', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<![.,!?:;—\s])\s+(но|зато)\b', r', \1', text, flags=re.IGNORECASE)
    
    # Punctuation Spacing
    text = re.sub(r'\s+([.,!?:;])', r'\1', text)
    text = re.sub(r'([.,!?:;])(?=[а-яА-Яa-zA-Z])', r'\1 ', text)
    
    # Double spaces
    text = re.sub(r' +', ' ', text).strip()
    
    # Capitalize start of sentences
    def capitalize_match(match):
        punct = match.group(1)
        space = match.group(2)
        char = match.group(3)
        return punct + space + char.upper()
        
    text = re.sub(r'([.!?])(\s+)([а-яa-z])', capitalize_match, text)
    
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
        
    if text and not text.endswith(('.', '!', '?', '...')):
        text += '.'
        
    return text
