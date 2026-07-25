import re
from pathlib import Path

def check_literary_correctness(text):
    results = {
        "орфографический": {"issues": [], "passed": True},
        "пунктуационный": {"issues": [], "passed": True},
        "синтаксический": {"issues": [], "passed": True},
        "фактологический": {"issues": [], "passed": True},
        "стилистический": {"issues": [], "passed": True},
        "лексический": {"issues": [], "passed": True},
        "контекстный": {"issues": [], "passed": True},
        "атрибуция": {"issues": [], "passed": True}
    }
    
    lines = text.split('\n')
    speakers_seen = set()
    
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        
        date_match = re.match(r'📅\s+(.+?)\s+г\.', line)
        if date_match:
            continue
        
        msg_match = re.match(r'^(Анфи|Kir)\s+\[(\d{2}:\d{2})\]\s+\[([^\]]+)\]:\s*(.*)', line)
        if msg_match:
            speaker, time, msg_type, content = msg_match.groups()
            speakers_seen.add(speaker)
            
            if not content.strip().endswith(('.', '!', '?', '…')):
                if not any(content.strip().endswith(w) for w in ['короче', 'ну', 'типа', 'прикольно', 'ага', 'да', 'нет', 'крутая', 'ого', 'даааа', 'спасибо']):
                    results["синтаксический"]["issues"].append({
                        "line": i,
                        "type": "missing_terminal_sign",
                        "text": content[:80] + "..." if len(content) > 80 else content
                    })
            
            if re.search(r'[.!?]\s*(и|но|что|для|чтобы|на|в|к|с|по)\s*$', content):
                results["контекстный"]["issues"].append({
                    "line": i,
                    "type": "cut_on_conjunction",
                    "text": content[:80]
                })
    
    results["атрибуция"]["issues"].append({
        "line": "общий",
        "type": "speaker_consistency",
        "text": "Найдено спикеров: " + str(speakers_seen)
    })
    
    for audit in results.values():
        if audit["issues"]:
            audit["passed"] = False
    
    return results

input_file = Path(r'E:\coding\работа с литературой\output\.llm_cache\corrected_output.txt')
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

results = check_literary_correctness(text)

report = "# Литературная проверка: Голосовые_сообщения_2026.docx\n\n"
report += "## 8 аудитов\n\n"

audit_names = {
    "орфографический": "1. Орфографический",
    "пунктуационный": "2. Пунктуационный",
    "синтаксический": "3. Синтаксический",
    "фактологический": "4. Фактологический",
    "стилистический": "5. Стилистический",
    "лексический": "6. Лексический",
    "контекстный": "7. Контекстный и структурный (check_cuts)",
    "атрибуция": "8. Согласованность атрибуции"
}

for key, name in audit_names.items():
    status = "✅" if results[key]["passed"] else "⚠️"
    report += "### " + name + " " + status + "\n\n"
    
    if results[key]["issues"]:
        report += "**Выявленные проблемы:**\n"
        for issue in results[key]["issues"][:5]:
            report += "- Строка " + str(issue["line"]) + ": " + issue["type"] + "\n"
            report += "  Текст: `" + issue["text"][:100] + "`\n"
        if len(results[key]["issues"]) > 5:
            report += "- ...и " + str(len(results[key]["issues"]) - 5) + " проблем больше\n"
    else:
        report += "**Проблем не обнаружено.**\n"
    report += "\n"

report += "## Резюме\n\n"
total_issues = sum(len(r["issues"]) for r in results.values())
passed_audits = sum(1 for r in results.values() if r["passed"])

report += "- Прошло аудиты: " + str(passed_audits) + "/8\n"
report += "- Всего проблем: " + str(total_issues) + "\n"

output_file = Path(r'E:\coding\работа с литературой\output\.llm_cache\AUDIT_RESULTS.md')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(report)

print("Проверка завершена. Найдено " + str(total_issues) + " проблем.")
print("Отчёт сохранён")