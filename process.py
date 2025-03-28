'''

Esegui process da terminale:
python process.py python3 process.py --md_path "~/leonardo/Scr*/readmes/" --json "in/tipologia.json" --csv_out "out/output_sections.csv"

'''

import argparse
import os

import utils.in_out_csv as ioc
import utils.parse_markdown_column as pmc
import config

def main():
    parser = argparse.ArgumentParser(description="Elabora i file Markdown scaricati e genera un CSV con le informazioni.")
    parser.add_argument('--md_path', type=str, default=config.PATH_MD_FILE, help="Cartella contenente i file Markdown")
    parser.add_argument('--json', type=str, default=config.NAME_FILE_JSON_IN, help="File JSON con le categorie")
    parser.add_argument('--csv_out', type=str, default=config.NAME_FILE_CSV_OUT, help="Percorso per il file CSV di output")
    parser.add_argument('--csv_out_url', type=str, default=config.NAME_FILE_CSV_OUT_URL, help="Percorso per il file CSV url di output")

    args = parser.parse_args()


    # Carica il file JSON delle categorie
    categories = pmc.load_categories_from_json(args.json)
    print(".. Categorie caricate dal JSON ..")

    # Verifica se la cartella esiste
    num_file_md=0

    if os.path.isdir(args.md_path):
        # Recupera la lista di file nella cartella
        link_list = [file for file in os.listdir(args.md_path) if file.endswith('.md') ]
        num_file_md = len(link_list)
        print(f".. Presenti {num_file_md} README dalla cartella {args.md_path} ..")

    # Analizza i file Markdown e crea una tabella
    data_table = pmc.get_data_table2(num_file_md, config.PATH_MD_FILE, categories)
    print(".. Tabella dei dati creata ..")

    # Esporta la tabella in CSV
    ioc.get_csv_tab2(data_table, args.csv_out)
    print(f".. Tabella esportata in {args.csv_out} ..")

    # Analizza i file Markdown e crea una tabella
    data_table = pmc.get_data_table_url_2(num_file_md, args.md_path, categories)
    print(".. Tabella degli url creata ..")

    ioc.get_csv_tab_url_2(data_table, args.csv_out_url)
    print(f".. Tabella url esportata in {args.csv_out_url} ..")


if __name__ == "__main__":
    main()
