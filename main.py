import utils.in_out_csv as ioc  # Modulo per la gestione di file CSV
import utils.download_from_url as dfu  # Modulo per scaricare file da URL
import utils.parse_markdown_column as pmc  # Modulo per analizzare file Markdown

# Percorsi dei file di input e output
name_file_csv_in = "../analizza_readme/in/mini_apps.csv"  # Test:sostituisci con la prossima riga
# name_file_csv_in = "./in/apps.csv"  # File CSV da cui leggere gli URL
name_file_csv_out = "../analizza_readme/out/output_sections.csv"  # File CSV dove salvare l'output
path_md_file = "../analizza_readme/md_file/"  # Directory per salvare i file Markdown scaricati
name_file_json_in = "../analizza_readme/in/tipologia.json"  # File JSON per le categorie

# Legge gli URL dal file CSV di input
site_list = ioc.read_urls(name_file_csv_in)  # Funzione che legge gli URL dal CSV
print(".. imported URLs from CSV ..")
#print(site_list)

# Rinomina gli URL per il download
link_list = dfu.rename_urls(site_list)  # Funzione che rinomina gli URL per il download
print(".. renamed URLs ..")
#dprint(link_list)

# Scarica i file Markdown dagli URL rinominati
num_file_md = dfu.download_md_file(link_list, path_md_file)  # Funzione che scarica i file Markdown
print(f".. downloaded {num_file_md} markdown files in {path_md_file}..")

# Carica il file JSON delle categorie
categories = pmc.load_categories_from_json(name_file_json_in)  # Funzione per caricare le categorie dal JSON
print(".. loaded categories from JSON ..")

# Crea una tabella dei dati analizzando i file Markdown scaricati
data_table = pmc.get_data_table(num_file_md, link_list, path_md_file, categories)  # Funzione che analizza i file
print(".. created data table from markdown files ..")

# Esporta la tabella dei dati in un file CSV di output
ioc.get_csv_tab(data_table, name_file_csv_out)  # Funzione per esportare i dati in un CSV
print(f".. table exported to CSV at {name_file_csv_out} ..")

# Segnala la fine dell'esecuzione del programma
print("END")
