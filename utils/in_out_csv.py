import csv

def read_urls(path):
    """
    Legge un file CSV e restituisce una lista di URL validi.

    Parametri:
    - path (str): Il percorso del file CSV da leggere.

    Ritorna:
    - list: Una lista contenente gli URL validi (cioè quelli che iniziano con 'http').
    """
    site_list = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for raw in csv_reader:
            # Verifica che la seconda colonna contenga un URL valido
            if raw[1].startswith('http'):
                site_list.append(raw[1])  # Aggiunge l'URL alla lista
    return site_list


def get_csv_tab(data_table, name_file_csv_out):
    """
    Scrive i dati estratti da file Markdown in un file CSV strutturato.

    Parametri:
    - data_table (list): Lista di dizionari contenenti le informazioni estratte.
    - name_file_csv_out (str): Nome del file CSV di output.

    Ritorna:
    - None: I dati vengono scritti direttamente nel file CSV.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione del CSV
        writer.writerow([
            "File_name",
            "H1_titles",
            "Level",
            "Category",
            "Char_counts",
            "Num_images",
            "Num_videos",
            "Num_code_blocks",
            "Num_links",
            "Current_links",
            "Repository_link"
        ])

        # Scrive ogni riga per ciascun H1 nel file
        for file_data in data_table:
            for i, title in enumerate(file_data["h1_titles"]):
                level = file_data["level"][i]
                writer.writerow([
                    file_data["file_name"],
                    title,
                    level,
                    file_data["category"][i],
                    file_data["char_counts"][i],
                    file_data["num_images"][i],
                    file_data["num_videos"][i],
                    file_data["num_code_blocks"][i],
                    file_data["num_links"][i],
                    file_data["current_links"][i],
                    file_data["link"]
                ])


def get_csv_tab2(data_table, name_file_csv_out):
    """
    Variante semplificata di get_csv_tab che esclude il link al repository.

    Parametri:
    - data_table (list): Lista di dizionari contenenti le informazioni estratte.
    - name_file_csv_out (str): Nome del file CSV di output.

    Ritorna:
    - None: I dati vengono scritti direttamente nel file CSV.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione del CSV semplificata
        writer.writerow([
            "File_name",
            "Titles",
            "Level",
            "Category",
            "Char_counts",
            "Num_images",
            "Num_videos",
            "Num_code_blocks",
            "Num_links",
            "Current_links"
        ])

        # Scrive ogni riga per ciascun H1 nel file
        for file_data in data_table:
            for i, title in enumerate(file_data["h1_titles"]):
                level = file_data["level"][i]
                writer.writerow([
                    file_data["file_name"],
                    title,
                    level,
                    file_data["category"][i],
                    file_data["char_counts"][i],
                    file_data["num_images"][i],
                    file_data["num_videos"][i],
                    file_data["num_code_blocks"][i],
                    file_data["num_links"][i],
                    file_data["current_links"][i]
                ])


def get_csv_tab_url(data_table, name_file_csv_out):
    """
    Scrive un file CSV contenente un elenco dettagliato dei link trovati in ciascun file Markdown.

    Ogni riga rappresenta un singolo link con:
    - Nome del file
    - Categoria assegnata al link
    - Numero progressivo del link
    - URL del link
    - Link del repository sorgente

    Parametri:
    - data_table (list): Lista di dizionari contenenti i dati estratti.
    - name_file_csv_out (str): Nome del file CSV di output.

    Ritorna:
    - None: I dati vengono scritti direttamente nel file.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione del CSV
        writer.writerow(["File_name", "Category", "Number", "Link", "Repository"])

        for file_data in data_table:
            file_name = file_data["file_name"]
            repository_link = file_data["link"]

            # Estrae tutti i link da tutte le sezioni (lista di tuple)
            all_links = [item for section_links in file_data["current_links"] for item in section_links]

            for category, number, link in all_links:
                writer.writerow([
                    file_name,
                    category if category else "None",  # Categoria 'None' se mancante
                    number,
                    link,
                    repository_link
                ])


def get_csv_tab_url_2(data_table, name_file_csv_out):
    """
    Variante semplificata di get_csv_tab_url che non include il link al repository.

    Ogni riga rappresenta un singolo link con:
    - Nome del file
    - Categoria assegnata al link
    - Numero progressivo del link
    - URL del link

    Parametri:
    - data_table (list): Lista di dizionari contenenti i dati estratti.
    - name_file_csv_out (str): Nome del file CSV di output.

    Ritorna:
    - None: I dati vengono scritti direttamente nel file.
    """
    with open(name_file_csv_out, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Intestazione del CSV
        writer.writerow(["File_name", "Category", "Number", "Link"])

        for file_data in data_table:
            file_name = file_data["file_name"]

            # Estrae tutti i link da tutte le sezioni (lista di tuple)
            all_links = [item for sublist in file_data["current_links"] for item in sublist]

            for category, number, link in all_links:
                writer.writerow([
                    file_name,
                    category if category else "None",
                    number,
                    link
                ])
