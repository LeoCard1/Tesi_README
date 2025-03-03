import unittest
import csv
import os
from utils.in_out_csv import read_urls

# Classe dei test
class TestReadUrls(unittest.TestCase):

    def test_read_urls(self):
        # Creo un file CSV di test temporaneo
        test_file = 'test.csv'
        with open(test_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'https://github.com/01mf02/jaq'])
            writer.writerow(['name', 'https://github.com/0ut0flin3/Reptyl'])
            writer.writerow(['name', 'ftp://example.net'])  # Questo non sarà incluso

        # Testiamo la funzione read_urls
        result = read_urls(test_file)
        expected = ['https://github.com/01mf02/jaq', 'https://github.com/0ut0flin3/Reptyl']
        self.assertEqual(result, expected)

        # Eliminiamo il file di test temporaneo
        os.remove(test_file)

# Blocco main per eseguire i test
if __name__ == '__main__':
    unittest.main()