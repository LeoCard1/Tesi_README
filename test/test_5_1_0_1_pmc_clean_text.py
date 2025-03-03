import unittest
from utils.parse_markdown_column import clean_text


import unittest

class TestFunzioneCleanText(unittest.TestCase):

    def test_rimuovi_link_markdown(self):
        md_text = "Questo è un link [test](http://example.com)"
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "Questo  un link")

    def test_rimuovi_tag_html(self):
        md_text = "Questo è un <b>test</b> con HTML"
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "Questo  un test con HTML")

    def test_rimuovi_link_web(self):
        md_text = "Visita il mio sito: http://example.com"
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "Visita il mio sito")

    def test_rimuovi_caratteri_non_ascii(self):
        md_text = "Ecco un emoji 🐛 e un carattere speciale ñ"
        cleaned_text = clean_text(md_text)
        # Ora l'emoji e il carattere ñ verranno rimossi
        self.assertEqual(cleaned_text, "Ecco un emoji  e un carattere speciale")

    def test_tieni_solo_lettere_e_spazi(self):
        md_text = "Solo lettere e numeri 1234"
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "Solo lettere e numeri")

    def test_stringa_vuota(self):
        md_text = ""
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "")

    def test_nessuna_modifica_necessaria(self):
        md_text = "Test senza modifiche"
        cleaned_text = clean_text(md_text)
        self.assertEqual(cleaned_text, "Test senza modifiche")

if __name__ == '__main__':
    unittest.main()