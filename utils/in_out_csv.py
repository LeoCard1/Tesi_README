import csv

def read_urls(path):
    """
    Legge un file CSV e restituisce una lista di URL validi.

    Parametri:
    - path (str): Il percorso del file CSV da leggere.

    Ritorna:
    - list: Una lista contenente gli URL validi (quelli che iniziano con 'http').
    """
    site_list = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for raw in csv_reader:
            if raw[1].startswith('http'):  # Controlla se la seconda colonna contiene un URL valido
                site_list.append(raw[1])  # Aggiunge l'URL alla lista
    return site_list


def get_csv_tab(data_table, name_file_csv_out):
    """
    Scrive i dati forniti in un file CSV con un formato specifico.

    Parametri:
    - data_table (list): Una lista di dizionari, ognuno contenente informazioni da scrivere nel CSV.
      Ogni dizionario deve avere le chiavi:
        - "file_name" (str): Nome del file Markdown analizzato.
        - "h1_titles" (list): Lista dei titoli H1 presenti nel file.
        - "category" (list): Lista delle categorie corrispondenti ai titoli H1.
        - "char_counts" (list): Numero di caratteri dei titoli H1.
        - "link" (str): URL del repository di origine.
    - name_file_csv_out (str): Nome del file CSV in cui salvare i dati.

    Ritorna:
    - Nessun valore di ritorno. Scrive i dati direttamente nel file CSV.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Scrive l'intestazione delle colonne nel file CSV
        writer.writerow([
            "File_name",     # Nome del file Markdown
            "H1_titles",     # Titoli H1 trovati nel file
            "Category",      # Categoria assegnata al titolo H1
            "Char_counts",   # Numero di caratteri del titolo H1
            "Repository_link" # URL del repository di origine
        ])

        # Scrive i dati riga per riga nel file CSV
        for file_data in data_table:
            for i, title in enumerate(file_data["h1_titles"]):  # Itera sui titoli H1
                writer.writerow([
                    file_data["file_name"],   # Nome del file
                    title,                    # Titolo H1
                    file_data["category"][i], # Categoria corrispondente
                    file_data["char_counts"][i], # Conteggio caratteri
                    file_data["link"]         # URL del repository
                ])
