# ── LIBRERIE ──────────────────────────────────────────────────────
import re
import json
import os
import urllib.request
from markdown_it import MarkdownIt  # Parser Markdown


# ── FUNZIONI DI SUPPORTO FILE ─────────────────────────────────────

def download_md_text(md_file):
    """
    Legge e restituisce il contenuto di un file Markdown locale.

    Parametri:
    - md_file (str): Percorso del file Markdown.

    Ritorna:
    - str: Contenuto testuale del file, oppure stringa vuota in caso di errore.
    """
    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def download_markdown_file(url, destination_path):
    """
    Scarica un file Markdown da un URL remoto e lo salva localmente.

    Parametri:
    - url (str): Indirizzo del file Markdown.
    - destination_path (str): Percorso locale in cui salvare il file.

    Ritorna:
    - bool: True se il download è riuscito, False altrimenti.
    """
    try:
        urllib.request.urlretrieve(url, destination_path)
        return True
    except Exception as e:
        print(f"Errore durante il download di {url}: {e}")
        return False


# ── PULIZIA E CATEGORIZZAZIONE ─────────────────────────────────────

def load_categories_from_json(json_file):
    """
    Carica da file JSON le categorie e le parole chiave per la classificazione dei titoli.

    Parametri:
    - json_file (str): Percorso del file JSON.

    Ritorna:
    - dict: Dizionario contenente categorie e parole chiave associate.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def clean_text(md_text):
    """
    Pulisce il testo Markdown rimuovendo link, HTML, emoji e simboli non alfabetici.

    Parametri:
    - md_text (str): Testo Markdown da pulire.

    Ritorna:
    - str: Testo ripulito, pronto per l’analisi.
    """
    md_text = re.sub(r'\[.*?\]\(.*?\)', '', md_text)     # Link in formato Markdown
    md_text = re.sub(r'<.*?>', '', md_text)              # Tag HTML
    md_text = re.sub(r'http[s]?://\S+', '', md_text)     # URL
    md_text = re.sub(r'[^\x00-\x7F]+', '', md_text)      # Emoji / caratteri non ASCII
    md_text = re.sub(r'[^a-zA-Z\s]', '', md_text)        # Simboli non alfabetici
    return md_text.strip()


def categorize_title(cleaned_title, categories):
    """
    Assegna una categoria a un titolo sulla base delle parole chiave.

    Parametri:
    - cleaned_title (str): Titolo già pulito.
    - categories (dict): Categorie e relative parole chiave.

    Ritorna:
    - str | None: Categoria assegnata oppure None se nessuna corrispondenza.
    """
    for category_name, category_data in categories.items():
        keywords = category_data["keywords"]
        keywords.append(category_name)  # Include anche il nome della categoria come keyword
        for keyword in keywords:
            if re.search(re.escape(keyword.lower()), cleaned_title.lower()):
                return category_name
    return None


# ── PARSING MARKDOWN ──────────────────────────────────────────────

def extract_md_tokens(md_text):
    """
    Esegue il parsing del testo Markdown e restituisce i token.

    Parametri:
    - md_text (str): Contenuto di un file Markdown.

    Ritorna:
    - list: Lista di token Markdown (oggetti markdown-it).
    """
    md = MarkdownIt()
    return md.parse(md_text)


def find_titles_md(md_text, categories):
    """
    Analizza il Markdown per trovare titoli, contare immagini, link, video e codice.

    Parametri:
    - md_text (str): Contenuto Markdown da analizzare.
    - categories (dict): Categorie per classificare i titoli.

    Ritorna:
    - tuple: (titoli, immagini, num_link, link_attivi, video, codice)
    """
    tokens = extract_md_tokens(md_text)

    # Inizializzazione delle variabili di output
    titles, images, links_count, links_list, videos, code_blocks = [], [], [], [], [], []
    countim = countlink = countvideo = countcode = 0
    current_links, link_text, link_url = [], "", ""
    link_active = False
    cat = ""

    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag in ['h1', 'h2', 'h3', 'h4']:
            # Salva i dati della sezione precedente
            if titles:
                images.append(countim)
                links_count.append(countlink)
                links_list.append(current_links)
                videos.append(countvideo)
                code_blocks.append(countcode)

            # Inizio nuova sezione
            title_content = tokens[i + 1].content
            cleaned_title = clean_text(title_content)
            category = categorize_title(cleaned_title, categories)
            level = int(token.tag[1])
            titles.append((title_content, level, category))

            # Reset contatori
            cat = category
            countim = countlink = countvideo = countcode = 0
            current_links, link_text, link_url = [], "", ""
            link_active = False

        elif token.type == 'inline':
            for child in token.children:
                if child.type == 'image':
                    countim += 1
                elif child.type == 'link_open':
                    link_active = True
                    link_text, link_url = "", ""
                    link_url = child.attrs.get('href', "")
                elif child.type == 'text' and link_active:
                    link_text += child.content.strip()
                elif child.type == 'link_close' and link_active and link_text.strip():
                    countlink += 1
                    current_links.append((cat, countlink, link_url))
                    link_active = False
                elif child.type in ['code_block', 'inline_code']:
                    countcode += 1

    # Salva l’ultima sezione
    if titles:
        images.append(countim)
        links_count.append(countlink)
        links_list.append(current_links)
        videos.append(countvideo)
        code_blocks.append(countcode)

    return titles, images, links_count, links_list, videos, code_blocks


# ── CALCOLO STATISTICHE ────────────────────────────────────────────

def calculate_section_length(md_text, h_title, next_h_title):
    """
    Calcola la lunghezza (in caratteri) della sezione compresa tra due titoli.

    Parametri:
    - md_text (str): Contenuto completo del file Markdown.
    - h_title (str): Titolo iniziale della sezione.
    - next_h_title (str | None): Titolo successivo (o None se ultimo).

    Ritorna:
    - int: Numero di caratteri della sezione.
    """
    section_start = md_text.find(h_title)
    if section_start == -1:
        raise ValueError(f"Titolo '{h_title}' non trovato nel testo.")
    section_start += len(h_title)
    section_end = md_text.find(next_h_title, section_start) if next_h_title else len(md_text)
    section_text = md_text[section_start:section_end].strip()
    return len(clean_text(section_text))


# ── FUNZIONI DI INIZIALIZZAZIONE DATI ──────────────────────────────

def initialize_data_table(num_file_md, link_list):
    """
    Inizializza una struttura dati completa per ciascun file Markdown remoto.

    Parametri:
    - num_file_md (int): Numero di file.
    - link_list (list): Lista dei link corrispondenti.

    Ritorna:
    - list[dict]: Lista di dizionari inizializzati per ogni file.
    """
    return [{
        "file_name": f"{i}.md",
        "level": [],
        "h1_titles": [],
        "category": [],
        "char_counts": [],
        "num_links": [],
        "current_links": [],
        "num_images": [],
        "num_videos": [],
        "num_code_blocks": [],
        "link": link_list[i]
    } for i in range(num_file_md)]


def initialize_data_table2(num_file_md):
    """
    Variante per file locali senza link remoti.

    Parametri:
    - num_file_md (int): Numero di file.

    Ritorna:
    - list[dict]: Lista di strutture dati iniziali.
    """
    return [{
        "file_name": f"{i}.md",
        "level": [],
        "h1_titles": [],
        "category": [],
        "char_counts": [],
        "num_links": [],
        "current_links": [],
        "num_images": [],
        "num_videos": [],
        "num_code_blocks": []
    } for i in range(num_file_md)]


def initialize_data_table_url(num_file_md, link_list):
    """
    Inizializza struttura minimale per analisi URL (con link remoti).

    Parametri:
    - num_file_md (int): Numero file.
    - link_list (list): Lista dei link remoti.

    Ritorna:
    - list[dict]: Strutture dati base per estrazione URL.
    """
    return [{
        "file_name": f"{i}.md",
        "current_links": [],
        "link": link_list[i]
    } for i in range(num_file_md)]


def initialize_data_table_url_2(num_file_md):
    """
    Variante URL-only per file locali (senza repository).

    Parametri:
    - num_file_md (int): Numero file.

    Ritorna:
    - list[dict]: Strutture dati minimali.
    """
    return [{
        "file_name": f"{i}.md",
        "current_links": []
    } for i in range(num_file_md)]


# ── FUNZIONE PRINCIPALE (RICORSIVA) ───────────────────────────────

def extract_sections_recursive(data_table, path_md_file, categories, processed_files=None, download_dir=None):
    """
    Estrae sezioni e statistiche da Markdown, anche ricorsivamente da link a file remoti.

    Parametri:
    - data_table (list): Lista strutture dati iniziali.
    - path_md_file (str): Directory dei file Markdown.
    - categories (dict): Mappa delle categorie.
    - processed_files (set): Set dei file già processati.
    - download_dir (str): Directory di salvataggio file remoti.

    Ritorna:
    - list: Tabella finale con tutte le analisi (inclusi file figli).
    """
    if processed_files is None:
        processed_files = set()
    if download_dir is None:
        download_dir = path_md_file

    os.makedirs(download_dir, exist_ok=True)
    result_data_table = []

    for file_data in data_table:
        file_path = os.path.join(path_md_file, file_data["file_name"])
        if file_path in processed_files:
            continue
        processed_files.add(file_path)

        md_text = download_md_text(file_path)
        h1_titles, images, nlinks, cur_links, videos, code_blocks = find_titles_md(md_text, categories)

        for i, (title, level, category) in enumerate(h1_titles):
            next_h1_title = h1_titles[i + 1][0] if i + 1 < len(h1_titles) else None
            char_count = calculate_section_length(md_text, title, next_h1_title)

            file_data["h1_titles"].append(clean_text(title))
            file_data["char_counts"].append(char_count)
            file_data["category"].append(category)
            file_data["num_links"].append(nlinks[i])
            file_data["current_links"].append(cur_links[i])
            file_data["num_images"].append(images[i])
            file_data["num_videos"].append(videos[i])
            file_data["num_code_blocks"].append(code_blocks[i])
            file_data["level"].append(level)

        result_data_table.append(file_data)

        # Parsing ricorsivo per file .md remoti linkati
        for section_links in file_data["current_links"]:
            for _, _, link_url in section_links:
                if link_url.lower().endswith(".md") and link_url.startswith("http://"):
                    original_child_file = os.path.basename(link_url)
                    parent_file_name = os.path.splitext(os.path.basename(file_data["file_name"]))[0]
                    child_base_name = os.path.splitext(original_child_file)[0]
                    combined_file_name = f"{parent_file_name}_{child_base_name}.md"
                    new_file_path = os.path.join(download_dir, combined_file_name)

                    if new_file_path in processed_files or os.path.exists(new_file_path):
                        continue
                    if not download_markdown_file(link_url, new_file_path):
                        continue

                    # Inizializzazione ricorsiva
                    child_entry = {
                        "file_name": combined_file_name,
                        "h1_titles": [],
                        "category": [],
                        "char_counts": [],
                        "num_links": [],
                        "current_links": [],
                        "num_images": [],
                        "num_videos": [],
                        "num_code_blocks": [],
                        "level": []
                    }

                    child_data = extract_sections_recursive(
                        [child_entry],
                        path_md_file=download_dir,
                        categories=categories,
                        processed_files=processed_files,
                        download_dir=download_dir
                    )
                    result_data_table.extend(child_data)

    return result_data_table


# ── INTERFACCE PRINCIPALI ─────────────────────────────────────────

def get_data_table(num_file_md, link_list, path_md_file, categories_json):
    """
    Wrapper per elaborazione remota con categorie.

    Ritorna:
    - list: Struttura dati analizzata.
    """
    data_table = initialize_data_table(num_file_md, link_list)
    return extract_sections_recursive(data_table, path_md_file, categories_json)


def get_data_table2(num_file_md, path_md_file, categories_json):
    """
    Wrapper per elaborazione di file locali.

    Ritorna:
    - list: Tabella dati estratti.
    """
    data_table = initialize_data_table2(num_file_md)
    return extract_sections_recursive(data_table, path_md_file, categories_json)


def extract_sections_url(data_table, path_md_file, categories):
    """
    Estrae solo i link dalle sezioni di ciascun file Markdown.

    Ritorna:
    - list: Tabella aggiornata con link trovati.
    """
    for file_data in data_table:
        md_text = download_md_text(os.path.join(path_md_file, file_data["file_name"]))
        _, _, _, cur_links, _, _ = find_titles_md(md_text, categories)
        file_data["current_links"] = cur_links
    return data_table


def get_data_table_url(num_file_md, link_list, path_md_file, categories_json):
    """
    Wrapper per estrazione URL remoti con metadati.

    Ritorna:
    - list: Tabella con link Markdown estratti.
    """
    data_table = initialize_data_table_url(num_file_md, link_list)
    return extract_sections_url(data_table, path_md_file, categories_json)


def get_data_table_url_2(num_file_md, path_md_file, categories_json):
    """
    Wrapper per estrazione URL da file locali.

    Ritorna:
    - list: Tabella con link estratti.
    """
    data_table = initialize_data_table_url_2(num_file_md)
    return extract_sections_url(data_table, path_md_file, categories_json)
