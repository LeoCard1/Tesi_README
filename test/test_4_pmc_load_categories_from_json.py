import json
import unittest
from unittest.mock import mock_open, patch
from utils.parse_markdown_column import load_categories_from_json  # Classe di test

class TestLoadCategoriesFromJson(unittest.TestCase):

    # Verifica che la funzione legga correttamente un file json e restituisca un dizionario Python
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "prerequisites": {
            "keywords": [
                "Prerequisites",
                "Requirements",
                "Dependencies",
                "Getting Started"
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
        },
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
        "configuration": {
            "keywords": [
                "Config",
                "Settings",
                "Options",
                "Flags",
                "Parameters",
                "Environment variables",
                "Editable values",
                "Custom",
                "Paths",
                "Storing",
                "Proxies",
                "Customization"
            ]
        },
        "documentation": {
            "keywords": [
                "Docs",
                "Guide",
                "Manual",
                "Wiki",
                "Manpage",
                "Api",
                "Details",
                "FAQ",
                "Tutorial"
            ]
        },
        "features": {
            "keywords": [
                "Features",
                "Functionality",
                "Capabilities",
                "Key Features",
                "Building blocks",
                "Characteristics",
                "Attributes",
                "Highlights",
                "Cool Stuff",
                "Syntax",
                "Goals"
            ]
        }
    }))
    def test_load_categories_from_json_success(self, mock_file):
        # Definiamo il percorso del file JSON (qui non è importante perché stiamo usando mock_open)
        json_file = 'categories.json'

        # Chiamata alla funzione
        result = load_categories_from_json(json_file)

        # Verifica che la funzione open venga chiamata con il nome del file e le modalità giuste
        # cioè json.load sia stato chiamato con il file aperto
        mock_file.assert_called_with(json_file, 'r', encoding='utf-8')

        # Confronta il risultato della funzione con il dizionario che ci aspettiamo
        expected_result = {
            "prerequisites": {
                "keywords": [
                    "Prerequisites",
                    "Requirements",
                    "Dependencies",
                    "Getting Started"
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
            },
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
            "configuration": {
                "keywords": [
                    "Config",
                    "Settings",
                    "Options",
                    "Flags",
                    "Parameters",
                    "Environment variables",
                    "Editable values",
                    "Custom",
                    "Paths",
                    "Storing",
                    "Proxies",
                    "Customization"
                ]
            },
            "documentation": {
                "keywords": [
                    "Docs",
                    "Guide",
                    "Manual",
                    "Wiki",
                    "Manpage",
                    "Api",
                    "Details",
                    "FAQ",
                    "Tutorial"
                ]
            },
            "features": {
                "keywords": [
                    "Features",
                    "Functionality",
                    "Capabilities",
                    "Key Features",
                    "Building blocks",
                    "Characteristics",
                    "Attributes",
                    "Highlights",
                    "Cool Stuff",
                    "Syntax",
                    "Goals"
                ]
            }
        }

        self.assertEqual(expected_result, result)

    @patch("builtins.open", new_callable=mock_open, read_data='{"category1": "Books"}')
    def test_load_categories_from_json_empty(self, mock_file):
        # Caso in cui il JSON contiene solo una categoria
        json_file = 'categories.json'

        # Chiamata alla funzione
        result = load_categories_from_json(json_file)

        # Verifica che json.load sia stato chiamato con il file aperto
        mock_file.assert_called_with(json_file, 'r', encoding='utf-8')

        # Verifica che il risultato sia corretto
        expected_result = {"category1": "Books"}
        self.assertEqual(expected_result, result)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_categories_from_json_invalid_json(self, mock_json_load, mock_file):
        # Caso in cui il JSON è malformato e genera un errore
        json_file = 'invalid_categories.json'

        # Verifica che venga sollevata una json.JSONDecodeError
        with self.assertRaises(json.JSONDecodeError):
            load_categories_from_json(json_file)

        # Verifica che il file sia stato aperto correttamente
        mock_file.assert_called_with(json_file, 'r', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open)
    def test_load_categories_from_json_file_not_found(self, mock_file):
        # Simuliamo un errore in cui il file non esiste (FileNotFoundError)
        mock_file.side_effect = FileNotFoundError

        # Verifica che venga sollevata una FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_categories_from_json('non_existing_file.json')


if __name__ == '__main__':
    unittest.main()