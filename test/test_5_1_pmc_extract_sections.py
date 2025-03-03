import unittest
import os
from utils.parse_markdown_column import extract_sections

class TestExtractSections(unittest.TestCase):

    def setUp(self):
        """Configura i file Markdown di test"""
        self.test_dir = "test_md_files/"  # Cartella di test
        os.makedirs(self.test_dir, exist_ok=True)  # Crea la cartella se non esiste

        self.data_table = [{'file_name': '0.md', 'h1_titles': [], 'category': [], 'char_counts': [], 'link': 'http://raw.githubusercontent.com/a/a/master/README.md'},
                           {'file_name': '1.md', 'h1_titles': [], 'category': [], 'char_counts': [], 'link': 'http://raw.githubusercontent.com/b/b/master/README.md'}
        ]
        self.categories = {
            "prerequisites": {
                "keywords": [
                    "Prerequisites", "Requirements", "Dependencies", "Getting Started"
                ]
            },
            "title": {
                "keywords": [
                    "Title", "Name of Project", "Index", "Table of contents",
                    "Overview", "Introduction", "About", "Description",
                    "Purpose", "Summary"
                ]
            },
            "install": {
                "keywords": [
                    "Install", "Installation", "Installing", "Build",
                    "Building", "Setup", "Deployment", "Source",
                    "Download", "Binary", "Executable"
                ]
            },
            "configuration": {
                "keywords": [
                    "Config", "Settings", "Options", "Flags", "Parameters",
                    "Environment variables", "Editable values", "Custom",
                    "Paths", "Storing", "Proxies", "Customization"
                ]
            }
        }

        # Dizionario con i contenuti di test
        self.md_files = {
            "0.md": "# Introduction\nabcdef*45678\n# Installation\nabcde*6789$%&/()\n# Settings\nabcd*$%&/()=",
            "1.md": "# Name of Project\nabc**\n# Executable\nab**345678\n# Customization\na**%&/678."
        }

        # Scrive i file di test nella cartella
        for file_name, content in self.md_files.items():
            with open(self.test_dir + file_name, "w", encoding="utf-8") as f:
                f.write(content)

#    def tearDown(self):
#        """Elimina i file di test dopo l'esecuzione"""
#        for file_name in self.md_files.keys():
#            os.remove(self.test_dir + file_name)
#        os.rmdir(self.test_dir)

    def test_extract_sections(self):
        """Testa extract_sections()"""
        result = extract_sections(self.data_table, self.test_dir, self.categories)

        # Verifica che i titoli H1 siano estratti correttamente
        self.assertEqual(result[0]["h1_titles"], ["Introduction", "Installation", "Settings"])
        self.assertEqual(result[1]["h1_titles"], ["Name of Project", "Executable", "Customization"])

        # Verifica le categorie assegnate
        self.assertEqual(result[0]["category"], ["title", "install", "configuration"])
        self.assertEqual(result[1]["category"], ["title", "install","configuration"])

        # Verifica il conteggio dei caratteri
        self.assertEqual(result[0]["char_counts"][0], 6)  # Lunghezza "Introduction"
        self.assertEqual(result[0]["char_counts"][1], 5)  # Lunghezza "Installation"
        self.assertEqual(result[0]["char_counts"][2], 4)  # Lunghezza "Settings"

        self.assertEqual(result[1]["char_counts"][0], 3)  # Lunghezza "Name of Project"
        self.assertEqual(result[1]["char_counts"][1], 2)  # Lunghezza "Executable"
        self.assertEqual(result[1]["char_counts"][2], 1)  # Lunghezza "Customization"

if __name__ == "__main__":
    unittest.main()
