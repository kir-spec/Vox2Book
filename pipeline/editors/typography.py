import re

def apply_typography(text):
    """
    Applies Russian publishing typography rules to text.
    """
    if not text:
        return ""
        
    # Russian Guillemets «...»
    text = re.sub(r'(\s|^)"([^"]+)"(\s|[.,!?:;]|$)', r'\1«\2»\3', text)
    
    # Em-dash for dialogues and pauses
    text = re.sub(r'(\s+)-\s+', r' — ', text)
    
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
    text = re.sub(r'\bтоесть\b', 'то есть', text, flags=re.IGNORECASE)
    text = re.sub(r'\bврядли\b', 'вряд ли', text, flags=re.IGNORECASE)
    text = re.sub(r'\bкакбудто\b', 'как будто', text, flags=re.IGNORECASE)
    
    # Punctuation Spacing
    text = re.sub(r'\s+([.,!?:;])', r'\1', text)
    text = re.sub(r'([.,!?:;])(?=[а-яА-Яa-zA-Z])', r'\1 ', text)
    
    # Double spaces
    text = re.sub(r' +', ' ', text).strip()
    
    return text
