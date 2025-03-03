import unittest
import os
from utils.parse_markdown_column import get_data_table

class TestGetDataTable(unittest.TestCase):

    def setUp(self):
        """Configura i file Markdown di test"""
        self.test_dir = "test_md_files/"  # Cartella di test
        os.makedirs(self.test_dir, exist_ok=True)  # Crea la cartella se non esiste

        self.num_file_md = 2
        self.link_list = [
            "http://raw.githubusercontent.com/a/a/master/README.md",
            "http://raw.githubusercontent.com/b/b/master/README.md"
        ]
        self.categories_json = {
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

    def test_get_data_table(self):
        """Testa get_data_table()"""
        result = get_data_table(self.num_file_md, self.link_list, self.test_dir, self.categories_json)

        # Verifica che i titoli H1 siano estratti correttamente
        self.assertEqual(result[0]["h1_titles"], ["Introduction", "Installation", "Settings"])
        self.assertEqual(result[1]["h1_titles"], ["Name of Project", "Executable", "Customization"])

        # Verifica le categorie assegnate
        self.assertEqual(result[0]["category"], ["title", "install", "configuration"])
        self.assertEqual(result[1]["category"], ["title", "install", "configuration"])

        # Verifica il conteggio dei caratteri
        self.assertEqual(result[0]["char_counts"][0], 6)  # Lunghezza "Introduction"
        self.assertEqual(result[0]["char_counts"][1], 5)  # Lunghezza "Installation"
        self.assertEqual(result[0]["char_counts"][2], 4)  # Lunghezza "Settings"

        self.assertEqual(result[1]["char_counts"][0], 3)  # Lunghezza "Name of Project"
        self.assertEqual(result[1]["char_counts"][1], 2)  # Lunghezza "Executable"
        self.assertEqual(result[1]["char_counts"][2], 1)  # Lunghezza "Customization"

#    def tearDown(self):
#        """Pulisce l'ambiente di test eliminando i file markdown creati."""
#        for file_name in self.md_files.keys():
#            os.remove(os.path.join(self.test_dir, file_name))
#        os.rmdir(self.test_dir)

if __name__ == "__main__":
    unittest.main()
