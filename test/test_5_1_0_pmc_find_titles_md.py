import unittest
from utils.parse_markdown_column import find_titles_md, categorize_title, clean_text

class TestFindTitlesMD(unittest.TestCase):

    def setUp(self):
        # Testo markdown di esempio
        self.md_text = """# Name of project
        analisi di documentazione readme per applicazioni open source.
# Installation
        this are instructions to install the app
        """

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

    def test_find_titles_md(self):
        # Chiamata alla funzione da testare
        result = find_titles_md(self.md_text, self.categories)

        # Verifica del risultato atteso
        expected_result = [
            ('Name of project', 1, 'title'),  # Normalizzato in lowercase se usiamo clean_text()
            ('Installation', 1, 'install')
        ]

        self.assertEqual(expected_result,result)

    def test_empty_md_text(self):
        # Caso in cui il testo markdown è vuoto
        result = find_titles_md("", self.categories)
        self.assertEqual(result, [])

    def test_no_matching_keywords(self):
        # Caso in cui nessun titolo corrisponde alle parole chiave
        md_text = """
# Random
        This is just some random content without keywords.
        """
        result = find_titles_md(md_text, self.categories)
        self.assertEqual([('Random', 1, None)],result)  # Associare None alla categoria quando non c'è corrispondenza


if __name__ == '__main__':
    unittest.main()
