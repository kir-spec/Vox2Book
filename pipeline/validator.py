import re
from config import WHISPER_HALLUCINATIONS

def validate_quality(messages):
    """
    Validates quality of processed messages array.
    Returns list of issue tuples: (index, issue_description, text_snippet)
    """
    issues = []
    conjunctions = {'и', 'но', 'а', 'или', 'что', 'чтобы', 'потому', 'как', 'в', 'на', 'с', 'к', 'из', 'до', 'для'}
    
    for idx, item in enumerate(messages):
        text = item.get('edited_body', '').strip()
        if not text:
            continue
            
        # 1. Unprintable / Replacement char check
        if '\ufffd' in text:
            issues.append((idx, "Contains replacement character \\ufffd", text[:60]))
            
        # 2. Conjunction cut-off check (check_cuts)
        words = re.findall(r'[а-яА-Яa-zA-Z0-9]+', text)
        if words and words[-1].lower() in conjunctions:
            issues.append((idx, f"Sentence cut off at conjunction: '{words[-1]}'", text[-60:]))
            
        # 3. Whisper hallucination check
        for pat in WHISPER_HALLUCINATIONS:
            if re.search(pat, text, flags=re.IGNORECASE):
                issues.append((idx, f"Leftover hallucination pattern: '{pat}'", text[:60]))
                
    return issues
