import re
import json
from markdown_it import MarkdownIt

from utils.download_from_url import download_md_text


# Funzione per caricare il file JSON contenente le categorie e le parole chiave associate
def load_categories_from_json(json_file):
    """
    Carica un file JSON contenente le categorie e le parole chiave associate.

    Parametri:
    - json_file (str): Percorso del file JSON contenente le categorie.

    Ritorna:
    - dict: Dizionario con le categorie e le parole chiave corrispondenti.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


# Funzione per inizializzare una tabella dati per ogni file Markdown scaricato
def initialize_data_table(num_file_md, link_list):
    """
    Inizializza una lista di dizionari per memorizzare i dati estratti dai file Markdown.

    Parametri:
    - num_file_md (int): Numero di file Markdown da analizzare.
    - link_list (list): Lista di URL corrispondenti ai file Markdown.

    Ritorna:
    - list: Una lista di dizionari, ognuno contenente informazioni di base sul file.
    """
    data_table = []
    for i in range(num_file_md):
        file_data = {
            "file_name": f"{i}.md",  # Nome del file
            "h1_titles": [],  # Lista dei titoli H1
            "category": [],  # Categoria di ogni titolo H1
            "char_counts": [],  # Numero di caratteri della sezione sotto il titolo H1
            "link": link_list[i]  # URL del repository
        }
        data_table.append(file_data)
    return data_table


# Funzione per pulire il testo Markdown rimuovendo link, tag HTML e caratteri speciali
def clean_text(md_text):
    """
    Pulisce il testo Markdown rimuovendo link, tag HTML, emoji e caratteri non alfanumerici.

    Parametri:
    - md_text (str): Testo Markdown da ripulire.

    Ritorna:
    - str: Testo pulito.
    """
    md_text = re.sub(r'\[.*?\]\(.*?\)', '', md_text)  # Rimuove i link in formato Markdown
    md_text = re.sub(r'<.*?>', '', md_text)  # Rimuove i tag HTML
    md_text = re.sub(r'http[s]?://\S+', '', md_text)  # Rimuove gli URL
    md_text = re.sub(r'[^\x00-\x7F]+', '', md_text)  # Rimuove emoji e caratteri speciali
    md_text = re.sub(r'[^a-zA-Z\s]', '', md_text)  # Mantiene solo lettere e spazi
    return md_text.strip()  # Rimuove gli spazi iniziali e finali


# Funzione per categorizzare un titolo in base alle parole chiave del file JSON
def categorize_title(cleaned_title, categories):
    """
    Determina la categoria di un titolo H1 in base alle parole chiave fornite.

    Parametri:
    - cleaned_title (str): Titolo ripulito da analizzare.
    - categories (dict): Dizionario contenente le categorie e le relative parole chiave.

    Ritorna:
    - str: Nome della categoria corrispondente, oppure None se non corrisponde a nessuna.
    """
    for category_name, category_data in categories.items():
        keywords = category_data["keywords"]
        for keyword in keywords:
            if keyword.lower() in cleaned_title.lower():
                return category_name
    return None


# Funzione per calcolare la lunghezza in caratteri di una sezione di testo
def calculate_section_length(md_text, h_title, next_h_title):
    """
    Calcola la lunghezza di una sezione di testo compresa tra due titoli H1.

    Parametri:
    - md_text (str): Contenuto completo del file Markdown.
    - h_title (str): Titolo H1 della sezione attuale.
    - next_h_title (str or None): Titolo H1 della prossima sezione (None se ultimo titolo).

    Ritorna:
    - int: Numero di caratteri nella sezione di testo tra i due titoli.
    """
    section_start = md_text.find(h_title) + len(h_title)  # Inizio della sezione
    if section_start == -1:
        raise ValueError(f"Titolo '{h_title}' non trovato nel testo.")

    if next_h_title and next_h_title != h_title:
        section_end = md_text.find("# " + next_h_title)  # Trova il prossimo titolo H1
        if section_end == -1:
            section_end = len(md_text)  # Se non trovato, prendi la fine del testo
    else:
        section_end = len(md_text)

    section_text = md_text[section_start:section_end].strip()
    cleaned_text = clean_text(section_text)
    return len(cleaned_text)


# Funzione principale per estrarre informazioni dalle sezioni dei file Markdown
def extract_sections(data_table, path_md_file, categories):
    """
    Estrae i titoli H1, la categoria e la lunghezza delle sezioni per ogni file Markdown.

    Parametri:
    - data_table (list): Lista di dizionari contenente i dati dei file Markdown.
    - path_md_file (str): Percorso della cartella contenente i file Markdown.
    - categories (dict): Dizionario con le categorie e parole chiave per la classificazione.

    Ritorna:
    - list: La data_table aggiornata con i titoli H1, categorie e conteggi caratteri.
    """
    for file_data in data_table:
        md_text = download_md_text(path_md_file + file_data["file_name"])
        h1_titles = find_titles_md(md_text, categories)

        for i, (title, _, _) in enumerate(h1_titles):
            file_data["h1_titles"].append(title)

            next_h1_title = h1_titles[i + 1][0] if i + 1 < len(h1_titles) else None
            char_count = calculate_section_length(md_text, title, next_h1_title)

            file_data["char_counts"].append(char_count)
            file_data["category"].append(h1_titles[i][2])

    return data_table


# Funzione per estrarre i token Markdown usando markdown-it
def extract_md_tokens(md_text):
    """
    Estrae i token dal testo Markdown utilizzando la libreria markdown-it.

    Parametri:
    - md_text (str): Contenuto Markdown da analizzare.

    Ritorna:
    - list: Lista di token estratti.
    """
    md = MarkdownIt()
    tokens = md.parse(md_text)
    return tokens


# Funzione per trovare i titoli H1 nel testo Markdown e associarli a una categoria
def find_titles_md(md_text, categories):
    """
    Estrae tutti i titoli H1 da un testo Markdown e li classifica in base alle categorie.

    Parametri:
    - md_text (str): Testo Markdown da analizzare.
    - categories (dict): Dizionario delle categorie con parole chiave.

    Ritorna:
    - list: Lista di tuple (titolo, livello, categoria).
    """
    tokens = extract_md_tokens(md_text)
    h1_titles = []

    for i, token in enumerate(tokens):
        if token.type == 'heading_open':  # Verifica se il token è un titolo
            level = int(token.tag[1:])  # Determina il livello del titolo (H1, H2, etc.)
            title_content = tokens[i + 1].content  # Contenuto del titolo

            cleaned_title = clean_text(title_content)  # Ripulisce il titolo
            category = categorize_title(cleaned_title, categories)  # Determina la categoria

            if level == 1:  # Considera solo i titoli H1
                h1_titles.append((cleaned_title, level, category))

    return h1_titles


# Funzione principale per ottenere la tabella dati completa
def get_data_table(num_file_md, link_list, path_md_file, categories_json):
    """
    Genera la tabella dei dati estraendo informazioni dai file Markdown.

    Parametri:
    - num_file_md (int): Numero totale di file Markdown.
    - link_list (list): Lista di URL dei repository.
    - path_md_file (str): Percorso dei file Markdown.
    - categories_json (dict): Dizionario contenente le categorie.

    Ritorna:
    - list: Tabella dati con titoli, categorie e lunghezza delle sezioni.
    """
    data_table = initialize_data_table(num_file_md, link_list)
    return extract_sections(data_table, path_md_file, categories_json)
