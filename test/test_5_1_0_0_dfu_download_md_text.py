import unittest
import os
from utils.parse_markdown_column import download_md_text


class TestDownloadMdText(unittest.TestCase):

    def setUp(self):
        """Configura l'ambiente di test creando una cartella con file Markdown di prova."""
        self.test_dir = "test_md_files/"  # Cartella di test con i file Markdown
        os.makedirs(self.test_dir, exist_ok=True)  # Crea la cartella se non esiste

        # Crea alcuni file Markdown di prova
        self.existing_file = os.path.join(self.test_dir, "example.md")
        self.corrupted_file = os.path.join(self.test_dir, "corrupted.md")

        with open(self.existing_file, "w", encoding="utf-8") as f:
            f.write("# Test File\nThis is a test file for download_md_text.")

        # File con contenuto che causa errore di decodifica (simuliamo contenuto corrotto)
        with open(self.corrupted_file, "wb") as f:
            f.write(b"\xff\xfe\xfa")  # Dati non validi in UTF-8

    def test_download_md_text_success(self):
        """Verifica che un file Markdown venga letto correttamente."""
        result = download_md_text(self.existing_file)

        # Il testo letto dovrebbe corrispondere al contenuto del file
        expected_text = "# Test File\nThis is a test file for download_md_text."
        self.assertEqual(result.strip(), expected_text)

    def test_download_md_text_file_not_found(self):
        """Verifica il comportamento quando il file non esiste."""
        non_existent_file = os.path.join(self.test_dir, "missing.md")

        result = download_md_text(non_existent_file)

        # La funzione dovrebbe restituire una stringa vuota
        self.assertEqual(result, "")

    def test_download_md_text_unicode_error(self):
        """Verifica il comportamento con un file corrotto (errore di decodifica)."""
        result = download_md_text(self.corrupted_file)

        # La funzione dovrebbe restituire una stringa vuota in caso di errore di decodifica
        self.assertEqual(result, "")

#    def tearDown(self):
#       """Ripulisce i file di test dopo l'esecuzione."""
#       for file in os.listdir(self.test_dir):
#            os.remove(os.path.join(self.test_dir, file))
#        os.rmdir(self.test_dir)


if __name__ == "__main__":
    unittest.main()
