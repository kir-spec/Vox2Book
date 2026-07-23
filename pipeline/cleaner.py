import re
from config import SPAM_KEYWORDS, SPAM_EMOJIS, WHISPER_HALLUCINATIONS

def is_spam_message(text):
    if not text:
        return True
    text_lower = text.lower()
    if any(kw.lower() in text_lower for kw in SPAM_KEYWORDS):
        return True
    if any(emoji in text for emoji in SPAM_EMOJIS):
        return True
    return False


def clean_whisper_hallucinations(text):
    if not text:
        return ""
        
    # 1. Remove unprintable / replacement chars
    text = re.sub(r'[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    
    # 2. Remove hallucination patterns
    for pat in WHISPER_HALLUCINATIONS:
        text = re.sub(pat, '', text, flags=re.IGNORECASE)
        
    # 3. Clean UI prompts
    text = re.sub(r'\bОтправить\.\s*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bЭкранный диктор озвучивает стикер:?\s*', '', text, flags=re.IGNORECASE)
    
    # 4. Remove STT word repetition loops (e.g., "На. На. На. На.", "и и и и и")
    text = re.sub(r'(\b[а-яА-Яa-zA-Z0-9]+[.!?,]?\s+)\1{2,}', r'\1', text, flags=re.IGNORECASE)
    text = re.sub(r'(\b[а-яА-Яa-zA-Z0-9]+\s+)\1{2,}', r'\1', text, flags=re.IGNORECASE)
    
    # 5. STT Phonetic & Typo Replacements
    replacements = [
        (r'\bпахевизм\b', 'пофигизм'),
        (r'\bне устранные динамики\b', 'встроенные динамики'),
        (r'\bв иглу без поводка\b', 'в загул без поводка'),
        (r'\bне жны\b', 'не нужны'),
        (r'\bне жно\b', 'не нужно'),
        (r'\bбабберест\b', 'Wildberries'),
        (r'\bвайлдберес\b', 'Wildberries'),
        (r'\bвайлдберриз\b', 'Wildberries'),
        (r'\bвидит иди файра\b', 'Edifier'),
        (r'\bежифайр\b', 'Edifier'),
        (r'\bэдифаер\b', 'Edifier'),
        (r'\bаудиент\b', 'Audient'),
        (r'\bчерез вспомогательный линии\b', 'через вспомогательную линию'),
        (r'\bсапорти\b', 'поддерживает'),
    ]
    
    for pat, repl in replacements:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        
    # 6. Trim trailing truncated conjunctions/prepositions at end of text (check_cuts)
    conjunctions = ['и', 'но', 'а', 'или', 'что', 'чтобы', 'потому', 'как', 'в', 'на', 'с', 'к', 'из', 'до', 'для']
    for conj in conjunctions:
        # Trailing comma + conj + dot e.g. ", что." -> "."
        text = re.sub(rf',\s+{conj}[.,!?\s]*$', r'.', text, flags=re.IGNORECASE)
        # Trailing after punctuation e.g. ". И." -> "."
        text = re.sub(rf'([.,!?])\s+{conj}[.,!?\s]*$', r'\1', text, flags=re.IGNORECASE)
        # Trailing space + conj + dot e.g. " в." -> "."
        text = re.sub(rf'\s+{conj}[.,!?\s]*$', r'.', text, flags=re.IGNORECASE)
        
    # Remove trailing single uppercase letters noise at end e.g. " H С."
    text = re.sub(r'\s+[A-Za-zА-Яа-я][.,!?\s]+[A-Za-zА-Яа-я]?[.,!?\s]*$', r'.', text)
    
    # Double punctuation cleanup
    text = re.sub(r',\s*\.', '.', text)
    text = re.sub(r'\.\s*\.', '.', text)
    
    return text.strip()
