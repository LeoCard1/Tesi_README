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
    - data_table (list): Una lista di dizionari contenenti informazioni sulle sezioni Markdown.
    - name_file_csv_out (str): Nome del file CSV in cui salvare i dati.

    Ritorna:
    - Nessun valore di ritorno. Scrive i dati direttamente nel file CSV.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione delle colonne nel file CSV
        writer.writerow([
            "File_name",     # Nome del file Markdown
            "H1_titles",     # Titoli H1 trovati nel file
            "Category",      # Categoria assegnata al titolo H1
            "Char_counts",   # Numero di caratteri del titolo H1

            "Num_images",    # Numero di immagini nella sezione
            "Num_videos",    # Numero di video nella sezione
            "Num_code_blocks", # Numero di blocchi di codice nella sezione
            "Num_links",  # Numero totale di link nella sezione
            "Current_links",  # Lista dei link nella sezione
            "Repository_link" # URL del repository
        ])

        # Scrive i dati riga per riga nel file CSV
        for file_data in data_table:
            for i, title in enumerate(file_data["h1_titles"]):  # Itera sui titoli H1
                writer.writerow([
                    file_data["file_name"],     # Nome del file
                    title,                      # Titolo H1
                    file_data["category"][i],   # Categoria corrispondente
                    file_data["char_counts"][i], # Conteggio caratteri

                    file_data["num_images"][i],  # Numero di immagini
                    file_data["num_videos"][i],  # Numero di video
                    file_data["num_code_blocks"][i],  # Numero di blocchi di codice
                    file_data["num_links"][i],  # Numero di link
                    file_data["current_links"][i],  # Lista di link
                    file_data["link"]           # URL del repository
                ])

def get_csv_tab2(data_table, name_file_csv_out):
    """
    Variante di get_csv_tab che omette il Repository_link.

    Parametri:
    - data_table (list): Lista di dizionari con informazioni sulle sezioni Markdown.
    - name_file_csv_out (str): Nome del file CSV in cui salvare i dati.

    Ritorna:
    - Nessun valore di ritorno. Scrive i dati nel file CSV.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione delle colonne nel file CSV
        writer.writerow([
            "File_name",
            "H1_titles",
            "Category",
            "Char_counts",

            "Num_images",
            "Num_videos",
            "Num_code_blocks",
            "Num_links",
            "Current_links"
        ])

        # Scrive i dati riga per riga nel file CSV
        for file_data in data_table:
            for i, title in enumerate(file_data["h1_titles"]):
                writer.writerow([
                    file_data["file_name"],
                    title,
                    file_data["category"][i],
                    file_data["char_counts"][i],

                    file_data["num_images"][i],
                    file_data["num_videos"][i],
                    file_data["num_code_blocks"][i],
                    file_data["num_links"][i],
                    file_data["current_links"][i]
                ])
