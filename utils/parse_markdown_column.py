import re
import json
import urllib


from markdown_it import MarkdownIt

import config


# Funzione per scaricare i file Markdown da una lista di link e salvarli localmente
def download_md_text(md_file):
    """
    Questa funzione legge il contenuto di un file Markdown e lo restituisce come stringa.

    Parametri:
    - md_file (str): Percorso del file Markdown da leggere.

    Ritorna:
    - md_text (str): Contenuto del file Markdown, oppure stringa vuota se il file non esiste
                     o se si verifica un errore di decodifica.
    """
    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            md_text = file.read()
    except FileNotFoundError:
        md_text = ""  # Se il file non esiste, restituisce una stringa vuota
    except UnicodeDecodeError:
        md_text = ""  # Se c'è un errore di decodifica, restituisce una stringa vuota
    return md_text


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
            # Cerca la parola chiave come una corrispondenza parziale, ignorando maiuscole/minuscole
            if re.search(re.escape(keyword.lower()), cleaned_title.lower()):
                return category_name
    return None




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
        h1_titles, images, nlinks , cur_links = find_titles_md(md_text, categories)


        for i, (title, _, _) in enumerate(h1_titles):


            next_h1_title = h1_titles[i + 1][0] if i + 1 < len(h1_titles) else None
            char_count = calculate_section_length(md_text, title, next_h1_title)

            file_data["h1_titles"].append(clean_text(title))    #prima elabora poi ripuliscimi testo
            file_data["char_counts"].append(char_count)
            file_data["category"].append(h1_titles[i][2])
            file_data["num_links"].append(nlinks[i])
            file_data["current_links"].append(cur_links[i])
            file_data["num_images"].append(images[i])

    return data_table







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
            "num_links": [],  # Nuova colonna per il numero di link
            "current_links":[],
            "num_images":[],
            "link": link_list[i]  # URL del repository
        }
        data_table.append(file_data)
    return data_table

def initialize_data_table2(num_file_md):
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
           # "link": link_list[i]  # URL del repository
            "num_links": [],  # Nuova colonna per il numero di link
            "current_links": [],
            "num_images":[]

        }
        data_table.append(file_data)
    return data_table


def get_data_table2(num_file_md, path_md_file, categories_json):
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
    data_table = initialize_data_table2(num_file_md)
    return extract_sections(data_table, path_md_file, categories_json)


def calculate_section_length(md_text, h_title, next_h_title):
    """
    Calcola la lunghezza di una sezione di testo compresa tra due titoli H1 escludendo i titoli stessi.
    Parametri:
    - md_text (str): Contenuto completo del file Markdown.
    - h_title (str): Titolo H1 della sezione attuale.
    - next_h_title (str or None): Titolo H1 della prossima sezione (None se ultimo titolo).

    Ritorna:
    - int: Numero di caratteri nella sezione di testo tra i due titoli.
    """

    section_start = md_text.find(h_title)
    if section_start == -1:
        raise ValueError(f"Titolo '{h_title}' non trovato nel testo.")

    section_start += len(h_title)  # Sposta l'indice dopo il titolo

    # Trova l'indice di fine della sezione (prima del prossimo titolo)
    if next_h_title and next_h_title != h_title:
        section_end = md_text.find(next_h_title, section_start)  # Cerca il prossimo titolo H1
        if section_end == -1:
            section_end = len(md_text)  # Se non trovato, prendi la fine del testo
    else:
        section_end = len(md_text)

    # Estrae il testo della sezione e lo ripulisce
    section_text = md_text[section_start:section_end].strip()

    cleaned_text = clean_text(section_text)
    return len(cleaned_text)






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



def find_titles_md(md_text, categories):
    """
    Estrae tutti i titoli H1 da un testo Markdown e conta le immagini e i link tra i titoli.

    Ritorna:
    - h1_titles (list): Lista di tuple (titolo, livello, categoria).
    - images (list): Lista con il numero di immagini tra ogni titolo.
    - links_count (list): Lista con il numero di link tra ogni titolo.
    - links_list (list): Lista di liste contenenti tuple (testo, url) per ogni link tra i titoli.
    """
    tokens = extract_md_tokens(md_text)
    h1_titles = []
    images = []
    links_count = []
    links_list = []

    countim = 0  # Conta le immagini nella sezione corrente
    countlink = 0  # Conta i link nella sezione corrente
    current_links = []  # Memorizza gli URL e i testi dei link nella sezione corrente
    link_active = False  # Flag per sapere se siamo dentro un link
    link_text = ""  # Testo del link attuale
    link_url = ""  # URL del link attuale

    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag == 'h1':
            if h1_titles:
                images.append(countim)  # Salva il conteggio delle immagini per la sezione precedente
                links_count.append(countlink)  # Salva il conteggio dei link per la sezione precedente
                links_list.append(current_links)  # Salva la lista di link per la sezione precedente

            title_content = tokens[i + 1].content
            cleaned_title = clean_text(title_content)
            category = categorize_title(cleaned_title, categories)

            h1_titles.append((title_content, 1, category))

            # Resetta i contatori per la nuova sezione
            countim = 0
            countlink = 0
            current_links = []
            link_active = False  # Resetta flag del link mi dice se sono in un token 'link_open'
            link_text = ""
            link_url = ""
            filename_curr_url = ""

        elif token.type == 'inline':
            for child in token.children:
                if child.type == 'image':
                    countim += 1

                elif child.type == 'link_open':
                    link_active = True  # Inizia un nuovo link
                    link_text = ""  # Reset testo del link
                    link_url = ""
                    #filename_curr_url = "../current_urls/"+str(i)+".md"
                    if child.attrs['href']:
                        link_url = child.attrs['href']

                elif child.type == 'text':
                    if link_active:
                        link_text += child.content.strip()  # Accumula testo del link

                elif child.type == 'link_close':
                    if link_active and link_text.strip():
                        countlink += 1
                        current_links.append((countlink, link_url))  # Salva la coppia (num_url, url)
                        #get_text_from_url(link_url, filename_curr_url)

    # Aggiungi il conteggio e la lista di link per l'ultima sezione
    if h1_titles:
        images.append(countim)
        links_count.append(countlink)
        links_list.append(current_links)####

    return h1_titles, images, links_count, links_list

