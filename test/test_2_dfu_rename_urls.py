import unittest
from utils.download_from_url import rename_urls

# Classe di test
class TestRenameUrls(unittest.TestCase):

    def test_rename_urls(self):
        # Lista di URL di esempio
        site_list = [
            'https://github.com/01mf02/jaq.com',
            'https://example.com/somepath',
            'http://site.com/anotherpath'
        ]

        # URL che ci aspettiamo come risultato
        expected = [
            'http://raw.githubusercontent.com/01mf02/jaq/master/README.md',
            'http://raw.exampleusercontent.com/somepath/master/README.md',
            'http://raw.siteusercontent.com/anotherpath/master/README.md'
        ]

        # Testiamo la funzione rename_urls
        result = rename_urls(site_list)
        self.assertEqual(result, expected)

    def test_empty_list(self):
        # Se la lista è vuota, il risultato dovrebbe essere anch'esso vuoto
        result = rename_urls([])
        self.assertEqual(result, [])

    def test_single_url(self):
        # Testiamo con una sola URL nella lista
        site_list = ['https://example.com/testpath']
        expected = ['http://raw.exampleusercontent.com/testpath/master/README.md']
        result = rename_urls(site_list)
        self.assertEqual(result, expected)

# Esegui i test
if __name__ == '__main__':
    unittest.main()