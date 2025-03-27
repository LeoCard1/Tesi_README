'''Esegui il download da console:
python3 download.py --csv "in/mini_apps.csv" --output "../Tesi_readme_modulare/md_file/"
"
'''
import argparse
import os
import utils.in_out_csv as ioc
import utils.download_from_url as dfu
import utils.parse_markdown_column as pmc
import config

def main():
    parser = argparse.ArgumentParser(description="Scarica file README.md da una lista di repository GitHub.")
    parser.add_argument('--md_path', type=str, default=config.PATH_MD_FILE, help="Cartella contenente i file Markdown")
    parser.add_argument('--csv_in', type=str, default=config.NAME_FILE_CSV_IN, help="Percorso del file CSV con gli URL")

    parser.add_argument('--json', type=str, default=config.NAME_FILE_JSON_IN, help="File JSON con le categorie")
    parser.add_argument('--csv_out', type=str, default=config.NAME_FILE_CSV_OUT, help="Percorso per il file CSV di output")
    parser.add_argument('--csv_out_url', type=str, default=config.NAME_FILE_CSV_OUT_URL, help="Percorso per il file CSV url di output")

    args = parser.parse_args()

    # Crea la cartella di destinazione se non esiste
    os.makedirs(args.md_path, exist_ok=True)


    # Carica il file JSON delle categorie
    categories = pmc.load_categories_from_json(args.json)
    print(".. Categorie caricate dal JSON ..")

    # Legge gli URL dal file CSV
    site_list = ioc.read_urls(args.csv_in)
    print(f".. URL importati dal CSV: {args.csv_in} ..")
    #print (site_list)


    # Converte gli URL in formato raw per il download
    link_list = dfu.rename_urls(site_list)
    print(".. URL convertiti ..")
    #print(link_list)

    # Scarica i file Markdown
    num_file_md = dfu.download_md_file(link_list, args.md_path)
    print(f".. {num_file_md} file Markdown sono stati scaricati in {args.md_path} ..")

    # Analizza i file Markdown e crea una tabella
    data_table = pmc.get_data_table(num_file_md, link_list, args.md_path, categories)
    print(".. Tabella dei dati creata ..")

    # Esporta la tabella in CSV
    ioc.get_csv_tab(data_table, args.csv_out)
    print(f".. Tabella esportata in {args.csv_out} ..")

    # Analizza i file Markdown e crea una tabella
    data_table = pmc.get_data_table_url(num_file_md, link_list, args.md_path, categories)
    print(".. Tabella degli url creata ..")

    # Esporta la tabella in CSV degli url
    ioc.get_csv_tab_url(data_table, args.csv_out_url)
    print(f".. Tabella url esportata in {args.csv_out_url} ..")

if __name__ == "__main__":
    main()
