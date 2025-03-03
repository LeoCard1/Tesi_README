import unittest
import json

from pkg_resources import non_empty_lines

from utils.parse_markdown_column import categorize_title

class TestCategorizeTitle(unittest.TestCase):

    def setUp(self):
        self.categories = {
            "install": {
                "keywords": [
                    "Install",
                    "Installation",
                    "Installing",
                    "Build",
                    "Building",
                    "Setup",
                    "Deployment",
                    "Source",
                    "Download",
                    "Binary",
                    "Executable"
                ]
            },
            "title": {
                "keywords": [
                  "Title",
                  "Name of Project",
                  "Index",
                  "Table of contents",
                  "Overview",
                  "Introduction",
                  "About",
                  "Description",
                  "Purpose",
                  "Summary"
                ]
              }
        }

    '''
    Test ok: all'interno dello stesso titolo ci sono parole di categorie diverse 
    esso viene correttamente classificato grazie alla modifica alla funzione categorize_title
    che associa il titolo alla prima parola presente nel titolo
    '''

    def test_categorize_title_found(self):
        # Test quando la categoria è trovata
        title = "Installation description dependencies"
        result = categorize_title(title, self.categories)
        self.assertEqual(result, "install")


    def test_categorize_title_not_found(self):
        # Test quando la categoria non è trovata
        title = "Cooking recipes for beginners"
        result = categorize_title(title, self.categories)
        self.assertIsNone(result)

    def test_categorize_title_case_insensitive(self):
        # Test per verificare che la funzione non faccia distinzione tra maiuscole e minuscole
        title = "Installation,download"
        result = categorize_title(title, self.categories)
        self.assertEqual(result, "install")

    def test_categorize_title_multiple_keywords(self):
        # Test con più parole chiave che potrebbero corrispondere
        title = "overview, introduction"
        result = categorize_title(title, self.categories)
        self.assertEqual(result, "title")

    def test_empty_title(self):
        # Test quando il titolo è vuoto
        title = ""
        result = categorize_title(title, self.categories)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
