import unittest
import os
import urllib.request
from utils.download_from_url import download_md_file


class TestDownloadMdFile(unittest.TestCase):

    def setUp(self):
        """Crea una cartella temporanea per i file scaricati"""
        self.test_dir = "test_md_files/"
        os.makedirs(self.test_dir, exist_ok=True)

        # Lista di URL di esempio esistenti con file Markdown reali
        self.link_list = [
            "http://raw.githubusercontent.com/01mf02/jaq/master/README.md",
            "http://raw.githubusercontent.com/0ut0flin3/Reptyl/master/README.md"
        ]

    def test_download_md_file_success(self):
        """Testa il download dei file"""
        num_downloaded = download_md_file(self.link_list, self.test_dir)

        # Verifica che il numero di file scaricati sia uguale alla lunghezza della lista di URL
        self.assertEqual(num_downloaded, len(self.link_list))

        # Verifica che i file esistano nella directory di destinazione
        for i in range(num_downloaded):
            file_path = os.path.join(self.test_dir, f"{i}.md")
            self.assertTrue(os.path.exists(file_path))

    def test_download_md_file_with_one_invalid_urls(self):
        """Testa il comportamento con URL non validi"""
        one_invalid_link = [
            "https://example.com/non_existent_file.md",  # File inesistente
            "http://raw.githubusercontent.com/01mf02/jaq/master/README.md"  # Dominio non valido
        ]

        num_downloaded = download_md_file(one_invalid_link, self.test_dir)

        # Nessun file dovrebbe essere scaricato
        self.assertEqual(num_downloaded, 1)

        num_downloaded = download_md_file(one_invalid_link, self.test_dir)

        # Solo 1 file valido dovrebbe essere scaricato
        self.assertEqual(num_downloaded, 1)

        # Verifica che almeno un file sia stato scaricato
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "0.md")))

    def test_empty_link_list(self):
        """Testa il comportamento con una lista di link vuota"""
        num_downloaded = download_md_file([], self.test_dir)
        self.assertEqual(num_downloaded, 0)

#    def tearDown(self):
#        """Elimina i file di test dopo l'esecuzione"""
#        for file in os.listdir(self.test_dir):
#            os.remove(os.path.join(self.test_dir, file))
#        os.rmdir(self.test_dir)


if __name__ == "__main__":
    unittest.main()
