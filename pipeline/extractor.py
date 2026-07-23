import os
import glob
import re
import html
from datetime import datetime
from bs4 import BeautifulSoup

def parse_html_chat_export(export_dir):
    """
    Parses Telegram HTML export files (messages*.html) in export_dir using stateful speaker tracking.
    Handles joined messages where Telegram omits <div class="from_name"> on consecutive messages from the same sender.
    Returns:
      audio_map: dict mapping audio_base_name (e.g. "audio_1000@06-02-2026_21-19-33")
                 to {'speaker': 'Kir'|'Амфи', 'dt': datetime, 'timestamp': 'DD.MM.YYYY HH:MM:SS'}
      text_messages: list of text message dicts from HTML belonging to Kir/Амфи.
    """
    html_files = sorted(glob.glob(os.path.join(export_dir, "messages*.html")))
    audio_map = {}
    text_messages = []
    
    current_speaker = None
    
    for fpath in html_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')
            
        msg_divs = soup.find_all('div', class_='message')
        for div in msg_divs:
            from_div = div.find('div', class_='from_name')
            if from_div:
                speaker_raw = from_div.get_text(strip=True)
                if "Music" in speaker_raw:
                    current_speaker = "Kir"
                elif "Алиса" in speaker_raw:
                    current_speaker = "Амфи"
                else:
                    current_speaker = None  # Channel / Other
                    
            if not current_speaker:
                continue
                
            date_div = div.find('div', class_='date')
            title_attr = date_div.get('title', '') if date_div else ""
            dt_match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2}):(\d{2})', title_attr)
            if not dt_match:
                continue
                
            day, month, year, hour, minute, second = dt_match.groups()
            dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            
            voice_a = div.find('a', class_='media_voice_message')
            if voice_a and voice_a.get('href'):
                href = voice_a.get('href')
                base = os.path.basename(href).replace('.ogg', '')
                audio_map[base] = {
                    'speaker': current_speaker,
                    'dt': dt,
                    'timestamp': f"{day}.{month}.{year} {hour}:{minute}:{second}",
                    'time_str': f"{hour}:{minute}"
                }
            else:
                text_div = div.find('div', class_='text')
                if text_div:
                    raw_text = text_div.get_text(separator='\n', strip=True)
                    if raw_text:
                        text_messages.append({
                            'speaker': current_speaker,
                            'dt': dt,
                            'timestamp': f"{day}.{month}.{year} {hour}:{minute}:{second}",
                            'time_str': f"{hour}:{minute}",
                            'type': 'text',
                            'body': raw_text,
                            'edited_body': raw_text
                        })
                        
    return audio_map, text_messages


def load_voice_messages_for_years(voice_base_dir, target_years, audio_map):
    """
    Loads all voice message transcription .txt files for specified target_years.
    Uses audio_map to assign speaker, exact timestamp, and time_str.
    """
    voice_files = []
    for y in target_years:
        ydir = os.path.join(voice_base_dir, str(y))
        if os.path.exists(ydir):
            voice_files.extend(sorted(glob.glob(os.path.join(ydir, "*.txt"))))
            
    messages = []
    
    for fpath in voice_files:
        base_name = os.path.basename(fpath).replace('.txt', '')
        
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            
        if "----------------------------------------" in content:
            _, body = content.split("----------------------------------------", 1)
        else:
            body = content
            
        body = body.strip()
        if not body:
            continue
            
        if base_name in audio_map:
            info = audio_map[base_name]
            speaker = info['speaker']
            dt = info['dt']
            time_str = info['time_str']
        else:
            m = re.search(r'@(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})-(\d{2})', base_name)
            if m:
                d, mth, y, h, mn, s = m.groups()
                dt = datetime(int(y), int(mth), int(d), int(h), int(mn), int(s))
                time_str = f"{h}:{mn}"
            else:
                dt = datetime(int(target_years[0]), 1, 1, 0, 0, 0)
                time_str = "00:00"
            speaker = "Kir"
            
        messages.append({
            'speaker': speaker,
            'dt': dt,
            'time_str': time_str,
            'type': 'voice',
            'body': body,
            'edited_body': body,
            'file': base_name
        })
        
    return messages


def extract_and_merge_for_years(export_dir, voice_base_dir, target_years=[2024, 2025], include_text_msgs=True):
    """
    Extracts voice and text messages for target_years, correlates with HTML export using stateful speaker tracking,
    and sorts chronologically.
    """
    audio_map, text_msgs = parse_html_chat_export(export_dir)
    voice_msgs = load_voice_messages_for_years(voice_base_dir, target_years, audio_map)
    
    all_msgs = list(voice_msgs)
    if include_text_msgs:
        # Filter text messages for target_years
        text_target = [m for m in text_msgs if m['dt'].year in target_years]
        all_msgs.extend(text_target)
        
    # Sort chronologically by datetime
    all_msgs.sort(key=lambda x: x['dt'])
    return all_msgs
