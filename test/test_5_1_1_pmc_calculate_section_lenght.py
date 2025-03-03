import unittest
import re

def clean_text(md_text):
    # Rimuove i link Markdown (es. [test](http://example.com))
    md_text = re.sub(r'\[.*?\]\(.*?\)', '', md_text)
    # Rimuove i tag HTML
    md_text = re.sub(r'<.*?>', '', md_text)
    # Rimuove link a siti web
    md_text = re.sub(r'http[s]?://\S+', '', md_text)
    # Rimuove emoji e caratteri non alfanumerici inclusi emoji e caratteri speciali
    md_text = re.sub(r'[^\x00-\x7F]+', '', md_text)
    # Rimuove tutto tranne lettere e spazi
    md_text = re.sub(r'[^a-zA-Z\s]', '', md_text)
    # Rimuove gli spazi all'inizio e alla fine del titolo
    md_text = md_text.strip()
    return md_text

def calculate_section_length(md_text, h_title, next_h_title):
    # Trova l'inizio della sezione
    section_start = md_text.find(h_title) + len(h_title)

    # Verifica che il titolo corrente sia stato trovato
    if section_start == -1:
        raise ValueError(f"Titolo '{h_title}' non trovato nel testo.")

    # Determina dove finisce la sezione (il prossimo titolo o la fine del testo)
    if next_h_title and next_h_title != h_title:
        section_end = md_text.find("# " + next_h_title)
        if section_end == -1:
            section_end = len(md_text)  # Se non trova il prossimo titolo, prendi la fine del testo
    else:
        section_end = len(md_text)  # Se non c'è next_h_title, prendi la lunghezza fino alla fine

    # Estrai il testo della sezione
    section_text = md_text[section_start:section_end].strip()

    # Ripulisci e conta i caratteri
    cleaned_text = clean_text(section_text)
    return len(cleaned_text)


class TestCalculateSectionLength(unittest.TestCase):

    def setUp(self):
        # Testo di esempio per i test
        self.md_text = """
# Introduction
        abc
# Installation
        Follow the steps below to install the software:
        - Step 1: Download the installer
        - Step 2: Run the installer

# Conclusion
        abcd
        """

    def test_section_length(self):
        # Verifica che la funzione calcoli correttamente la lunghezza della sezione tra 'Introduction' e 'Installation'
        result = calculate_section_length(self.md_text, "Introduction", "Installation")
        self.assertEqual(result, len("abc"))

    def test_next_title_not_found(self):
        """Se `next_h_title` non viene trovato, deve calcolare fino alla fine del testo"""
        result = calculate_section_length(self.md_text, "Conclusion", "NonExistentTitle")
        expected_length = len("abcd")
        self.assertEqual(result, expected_length)

    def test_section_length_last_section(self):
        # Verifica che la funzione calcoli correttamente la lunghezza dell'ultima sezione quando non c'è un titolo successivo
        result = calculate_section_length(self.md_text, "Conclusion", None)
        self.assertEqual(result, len("abcd"))

    def test_empty_section(self):
        # Verifica il caso di una sezione vuota
        md_text = """
        # Empty Section
        """
        result = calculate_section_length(md_text, "Empty Section", None)
        self.assertEqual(result, 0)  # La sezione è vuota, quindi la lunghezza deve essere 0





    def test_section_with_markdown(self):
        # Verifica che la funzione pulisca correttamente il testo con formattazione Markdown (ad esempio, **bold**)
        md_text = """
        # Installation
        Follow the **steps** below to *install* the software.
        """
        result = calculate_section_length(md_text, "Installation", None)
        self.assertEqual(result, len("Follow the steps below to install the software"))  # La lunghezza senza formattazione Markdown

if __name__ == '__main__':
    unittest.main()
