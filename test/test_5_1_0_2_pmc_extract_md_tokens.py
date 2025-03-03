import unittest
from markdown_it import MarkdownIt
from utils.parse_markdown_column import extract_md_tokens

class TestExtractMdTokens(unittest.TestCase):
    def test_intestazione(self):
        """Testa se un'intestazione Markdown viene riconosciuta"""
        md_text = "# Titolo"
        tokens = extract_md_tokens(md_text)
        self.assertGreater(len(tokens), 0)  # Controlla che ci siano token
        self.assertEqual(tokens[0].type, "heading_open")  # Verifica che il primo token sia un'intestazione

    def test_testo_grassetto(self):
        """Verifica se il testo in grassetto viene riconosciuto"""
        md_text = "**grassetto**"
        tokens = extract_md_tokens(md_text)
        self.assertTrue((token.type == "strong_open" for token in tokens))

    def test_lista_puntata(self):
        """Verifica se una lista puntata viene riconosciuta"""
        md_text = "- Elemento 1\n- Elemento 2"
        tokens = extract_md_tokens(md_text)
        self.assertTrue(any(token.type == "bullet_list_open" for token in tokens))

    def test_stringa_vuota(self):
        """Controlla che una stringa vuota restituisca una lista vuota"""
        md_text = ""
        tokens = extract_md_tokens(md_text)
        self.assertEqual(tokens, [])

    def test_paragrafo(self):
        """Verifica se un paragrafo viene riconosciuto"""
        md_text = "Questo è un paragrafo."
        tokens = extract_md_tokens(md_text)
        self.assertTrue(any(token.type == "paragraph_open" for token in tokens))

# Avvia i test
if __name__ == "__main__":
    unittest.main()
