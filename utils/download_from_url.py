import os  # Per operazioni sul filesystem (cartelle, file)
import re  # Per espressioni regolari (non usato in questo snippet ma incluso)
import urllib.request  # Per scaricare contenuti via HTTP
from urllib.parse import urlparse  # Per analizzare URL (non usato direttamente qui)

import \
    requests  # Per effettuare richieste HTTP (non usato in queste funzioni ma probabilmente utile in altre parti del progetto)


# Funzione per convertire gli URL originali nei corrispondenti URL raw di GitHubusercontent
def rename_urls(site_list):
    """
    Questa funzione prende una lista di URL e li trasforma in URL di GitHub raw content.

    Parametri:
    - site_list (list): Lista di URL originali di repository GitHub.

    Ritorna:
    - s_raw (list): Lista di URL modificati che puntano al file README.md in formato raw.
    """
    s_raw = []  # Lista degli URL raw da restituire
    for id, s in enumerate(site_list):
        # Divide l'URL al punto '.com' per ricostruire l'indirizzo raw
        a = s.split('.com')[0] + 'usercontent.com'  # Parte base dell'URL raw
        b = s.split('.com')[1]  # Resto dell'URL dopo '.com'

        # Costruisce l'URL raw che punta al file README.md sul branch master (o main)
        c = 'http://raw.' + a.split('//')[1] + b + '/master/README.md'

        # Aggiunge l'URL finale alla lista
        s_raw.append(c)
    return s_raw


def pulisci_cartella(cartella):
    """
    Elimina solo i file con estensione .md presenti nella cartella,
    senza rimuovere la cartella stessa.

    Parametri:
    - cartella (str): Il percorso della cartella da "ripulire".

    Ritorna:
    - None
    """
    if os.path.exists(cartella):
        for file in os.listdir(cartella):
            file_path = os.path.join(cartella, file)
            try:
                # Se è un file Markdown (.md), lo elimina
                if os.path.isfile(file_path) and file.endswith(".md"):
                    os.remove(file_path)
            except Exception as e:
                print(f"Errore nell'eliminazione di {file}: {e}")
    else:
        # Se la cartella non esiste, la crea
        os.makedirs(cartella)


# Funzione per scaricare i file Markdown da una lista di URL
def download_md_file(link_list, path_md_file):
    """
    Scarica i file README.md dai link forniti e li salva localmente con nomi numerici.

    Parametri:
    - link_list (list): Lista di URL dei file Markdown da scaricare.
    - path_md_file (str): Percorso della cartella in cui salvare i file Markdown.

    Ritorna:
    - i (int): Numero di file scaricati con successo.
    """
    pulisci_cartella(path_md_file)  # Pulisce la cartella prima di iniziare

    i = 0  # Contatore per i file scaricati

    for link in link_list:
        try:
            # Scarica il file e lo salva come 0.md, 1.md, 2.md, ecc.
            urllib.request.urlretrieve(link, path_md_file + str(i) + ".md")
            i += 1  # Incrementa il contatore se il download va a buon fine
        except:
            # Ignora errori (ad esempio se un URL è non valido o non raggiungibile)
            pass
    return i
