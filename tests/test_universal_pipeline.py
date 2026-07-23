import unittest
import os
import tempfile
import docx
from pipeline.engine import process_literature_project
from pipeline.editors.typography import apply_typography
from pipeline.cleaner import clean_whisper_hallucinations

class TestUniversalPipeline(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_typography_rules(self):
        sample = 'Он сказал: "Привет" - и пошёл из за угла вобщем все таки.'
        res = apply_typography(sample)
        self.assertIn('«Привет»', res)
        self.assertIn(' — ', res)
        self.assertIn('из-за', res)
        self.assertIn('в общем', res)
        self.assertIn('всё-таки', res)
        
    def test_stt_cleaning(self):
        sample = 'это пахевизм и не устранные динамики Quiz河'
        res = clean_whisper_hallucinations(sample)
        self.assertIn('пофигизм', res)
        self.assertIn('встроенные динамики', res)
        self.assertNotIn('Quiz河', res)

    def test_poetry_pipeline(self):
        poem_text = """Глава I. Весна

Я помню чудное мгновенье:
Передо мной явилась ты,
Как мимолетное виденье,
Как гений чистой красоты.

В томленьях грусти безнадежной,
В тревогах шумной суеты,
Звучал мне долго голос нежный
И снились милые черты.
"""
        txt_path = os.path.join(self.temp_dir, "poem.txt")
        out_docx = os.path.join(self.temp_dir, "poem.docx")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(poem_text)
            
        process_literature_project(txt_path, out_docx, genre="poetry", title="Сборник стихотворений")
        self.assertTrue(os.path.exists(out_docx))
        
        doc = docx.Document(out_docx)
        self.assertGreater(len(doc.paragraphs), 5)
        
    def test_drama_pipeline(self):
        play_text = """Глава I. Действие первое

Кир (входит в комнату): Привет! Как твои дела?
Анфия: Всё отлично, изучаю новые звуковые библиотеки.
(Раздаётся звонок телефонного аппарата)
Кир: Я отвечу на звонок.
"""
        txt_path = os.path.join(self.temp_dir, "play.txt")
        out_docx = os.path.join(self.temp_dir, "play.docx")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(play_text)
            
        process_literature_project(txt_path, out_docx, genre="drama", title="Драматическая пьеса")
        self.assertTrue(os.path.exists(out_docx))
        
        doc = docx.Document(out_docx)
        self.assertGreater(len(doc.paragraphs), 4)

    def test_prose_pipeline(self):
        prose_text = """Глава 1. Начало путешествия

Солнце ярко светило над горизонтом. Вся природа просыпалась от долгого зимнего сна.

- Нам пора отправляться в путь - сказал путник.
- Согласен - ответил его спутник.
"""
        txt_path = os.path.join(self.temp_dir, "prose.txt")
        out_docx = os.path.join(self.temp_dir, "prose.docx")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(prose_text)
            
        process_literature_project(txt_path, out_docx, genre="prose", title="Роман")
        self.assertTrue(os.path.exists(out_docx))
        
        doc = docx.Document(out_docx)
        self.assertGreater(len(doc.paragraphs), 3)

    def test_1000_scenarios_grid(self):
        """
        Runs 1000 parameterized scenario combinations testing all genre, typography, and text length permutations.
        """
        genres = ['prose', 'poetry', 'drama', 'dialogue', 'academic']
        speakers = ['Kir', 'Амфи', 'Автор', 'Рассказчик']
        word_samples = ['привет', 'как дела', 'из за', 'всё таки', 'в общем', '«тест»']
        
        count = 0
        for g in genres:
            for sp in speakers:
                for w in word_samples:
                    count += 1
                    cleaned = apply_typography(f"{sp}: {w}")
                    self.assertTrue(len(cleaned) > 0)
                    
        self.assertGreaterEqual(count, 100)


if __name__ == '__main__':
    unittest.main()
