import os
import sys

# Percorsi dei file di input e output
NAME_FILE_CSV_IN = "./in/mini_apps.csv"
NAME_FILE_CSV_OUT = "./out/output_section.csv"
PATH_MD_FILE = "./md_file/"
NAME_FILE_JSON_IN = "./in/tipologia.json"
OUT_DIR = "./out/"
IN_DIR= "./in/"
NAME_FILE_CSV_OUT_URL= "urls/output_urls.csv"

# Funzione per controllare se un file esiste e non è vuoto
def check_file(file_path, file_description):
    if not os.path.isfile(file_path):
        print(os.path.abspath("./out/output_sections.csv"))
        print(f"Errore: Il file {file_description} ({file_path}) non esiste.")
        sys.exit(1)
    if os.path.getsize(file_path) == 0:
        print(f"Errore: Il file {file_description} ({file_path}) è vuoto.")
        sys.exit(1)

# Funzione per controllare se una cartella esiste
def check_directory(dir_path, dir_description):
    if not os.path.isdir(dir_path):
        print(f"Errore: La cartella {dir_description} ({dir_path}) non esiste.")
        sys.exit(1)

# Controllo dei file e delle cartelle
check_file(NAME_FILE_CSV_IN, "CSV di input")
check_file(NAME_FILE_JSON_IN, "JSON di input")
check_directory(PATH_MD_FILE, "per i file Markdown")
check_directory(OUT_DIR, "di output")  # Controllo della cartella out
check_directory(IN_DIR, "di input")  # Controllo della cartella in
#check_directory(NAME_FILE_CSV_OUT_URL, "urls nelle sezioni del reame")  # Controllo della cartella degli urls nei READMEs

# Se tutto è OK, procedi con l'esecuzione del programma
print("Tutti i file e le cartelle necessari esistono e sono validi.")