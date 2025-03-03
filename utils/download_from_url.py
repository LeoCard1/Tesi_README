import urllib.request


# Funzione per convertire gli URL originali nei corrispondenti URL raw di GitHubusercontent
def rename_urls(site_list):
    """
    Questa funzione prende una lista di URL e li trasforma in URL di GitHub raw content.

    Parametri:
    - site_list (list): Lista di URL originali di repository GitHub.

    Ritorna:
    - s_raw (list): Lista di URL modificati che puntano al file README.md in formato raw.
    """
    s_raw = []
    for id, s in enumerate(site_list):
        # Sostituisce '.com' con 'usercontent.com' per ottenere l'URL raw
        a = s.split('.com')[0] + 'usercontent.com'
        b = s.split('.com')[1]
        # Costruisce l'URL che punta al file README.md nella directory principale del repo
        c = 'http://raw.' + a.split('//')[1] + b + '/master/README.md'
        s_raw.append(c)
    return s_raw


# Funzione per scaricare i file Markdown da una lista di link e salvarli localmente
def download_md_file(link_list, path_md_file):
    """
    Questa funzione scarica i file README.md dai link forniti e li salva localmente.

    Parametri:
    - link_list (list): Lista di URL dei file Markdown da scaricare.
    - path_md_file (str): Percorso della cartella in cui salvare i file Markdown.

    Ritorna:
    - i (int): Numero di file scaricati con successo.
    """
    i = 0  # Contatore per i file scaricati
    for link in link_list:
        try:
            # Scarica il file e lo salva con un indice numerico
            urllib.request.urlretrieve(link, path_md_file + str(i) + ".md")
            i += 1
        except:
            pass  # Ignora eventuali errori durante il download e continua con il prossimo link
    return i


# Funzione per leggere il contenuto di un file Markdown
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
