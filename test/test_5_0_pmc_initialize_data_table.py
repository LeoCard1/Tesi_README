import unittest
from utils.parse_markdown_column import initialize_data_table

class TestInitializeDataTable(unittest.TestCase):

    def test_initialize_data_table(self):
        """Testa la corretta inizializzazione della data_table"""

        num_file_md = 3
        link_list = [
            "http://raw.githubusercontent.com/a/a/master/README.md",
            "http://raw.githubusercontent.com/b/b/master/README.md",
            "http://raw.githubusercontent.com/c/c/master/README.md"
        ]

        expected_result =[{'file_name': '0.md',
                           'h1_titles': [],
                           'category': [],
                           'char_counts': [],
                           'link': 'http://raw.githubusercontent.com/a/a/master/README.md'},

                           {'file_name': '1.md',
                            'h1_titles': [],
                            'category': [],
                            'char_counts': [],
                            'link': 'http://raw.githubusercontent.com/b/b/master/README.md'},

                          {'file_name': '2.md',
                           'h1_titles': [],
                           'category': [],
                           'char_counts': [],
                           'link': 'http://raw.githubusercontent.com/c/c/master/README.md'}
        ]

        result = initialize_data_table(num_file_md, link_list)

        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
