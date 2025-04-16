import csv  # Per leggere e scrivere file CSV
from collections import defaultdict  # Per creare dizionari con valori predefiniti
import config  # File di configurazione con i percorsi (es. input/output CSV)

# Lista delle categorie riconosciute nei README
category_list = [
    "prerequisites", "title", "description", "install", "configuration", "documentation",
    "features", "license", "testing", "credits", "feedback", "help", "todo",
    "contacts", "performance"
]

def generate_summary(input_csv_path, output_csv_path):
    """
    Funzione che legge un CSV contenente i dati analizzati dei README
    e genera un riepilogo per ciascun file, esportando il tutto in un nuovo CSV.

    Parametri:
    - input_csv_path (str): Percorso del file CSV di input.
    - output_csv_path (str): Percorso del file CSV di output con il riassunto.
    """

    # Dizionario che contiene dati aggregati per ciascun file
    summary_data = defaultdict(lambda: {
        "char_counts": 0,              # Numero totale di caratteri
        "num_images": 0,               # Numero di immagini
        "num_videos": 0,               # Numero di video
        "num_code_blocks": 0,          # Numero di blocchi di codice
        "num_links": 0,                # Numero di link
        "categories": defaultdict(int),# Conteggio per ciascuna categoria
        "total_titles_recognized": 0   # Totale titoli/categorie riconosciute
    })

    # Dati aggregati totali per tutti i file
    total_summary = {
        "char_counts": 0,
        "num_images": 0,
        "num_videos": 0,
        "num_code_blocks": 0,
        "num_links": 0,
        "categories": defaultdict(int),
        "total_titles_recognized": 0,
    }

    # Legge il file CSV riga per riga
    with open(input_csv_path, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            filename = row["File_name"]
            category = row["Category"].strip().lower()  # Elimina spazi e converte in minuscolo

            # Se c'è una categoria valida, aggiorna i conteggi
            if category:
                if category in category_list:
                    summary_data[filename]["categories"][category] += 1
                    summary_data[filename]["total_titles_recognized"] += 1
                    total_summary["categories"][category] += 1
                    total_summary["total_titles_recognized"] += 1

            # Somma dei valori numerici (es. immagini, link, ecc.)
            for field in ["Char_counts", "Num_images", "Num_videos", "Num_code_blocks", "Num_links"]:
                value = int(row[field])  # Converte da stringa a intero
                key = field.lower()  # Uniforma le chiavi in minuscolo
                summary_data[filename][key] += value
                total_summary[key] += value

    # Scrive il file CSV di output con il riepilogo
    with open(output_csv_path, "w", newline='', encoding='utf-8') as outfile:
        # Definisce le intestazioni del file CSV finale
        fieldnames = [
            "File_name", "Total_titles_recognized", "Char_counts",
            "Num_images", "Num_videos", "Num_code_blocks", "Num_links"
        ] + category_list  # Aggiunge le categorie come colonne

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # Scrive l’intestazione nel file

        for file_name, data in summary_data.items():
            # Riepilogo per ogni file
            row = {
                "File_name": file_name,
                "Total_titles_recognized": data["total_titles_recognized"],
                "Char_counts": data["char_counts"],
                "Num_images": data["num_images"],
                "Num_videos": data["num_videos"],
                "Num_code_blocks": data["num_code_blocks"],
                "Num_links": data["num_links"]
            }

            # Inserisce '1' ripetuto per quante volte è presente una categoria (es. '1', '11', '111', ecc.)
            for cat in category_list:
                row[cat] = data["categories"].get(cat, 0)

            writer.writerow(row)  # Scrive la riga nel CSV

    # --- BLOCCO FACOLTATIVO PER SCRIVERE ANCHE IL RIEPILOGO TOTALE ---
    '''
    with open(totals_csv_path, "w", newline='', encoding='utf-8') as total_file:
        total_writer = csv.DictWriter(total_file, fieldnames=fieldnames)
        total_writer.writeheader()

        total_row = {
            "File_name": "TOTAL",
            "Total_titles_recognized": total_summary["total_titles_recognized"],
            "Char_counts": total_summary["char_counts"],
            "Num_images": total_summary["num_images"],
            "Num_videos": total_summary["num_videos"],
            "Num_code_blocks": total_summary["num_code_blocks"],
            "Num_links": total_summary["num_links"]
        }

        for cat in category_list:
            count = total_summary["categories"].get(cat, 0)
            total_row[cat] = '1' * count if count > 0 else ""

        total_writer.writerow(total_row)
    '''
    # Questo blocco commentato serve per scrivere un riepilogo globale
    # Può essere attivato se vuoi una riga "TOTAL" con i dati complessivi


# Esempio di utilizzo della funzione principale
generate_summary(
    input_csv_path=config.NAME_FILE_CSV_OUT,  # Percorso CSV di input (analisi)
    output_csv_path=config.TABLES_OUT_DIR + "readme_summary.csv",  # CSV di output generato
    # totals_csv_path="readme_totals.csv"  # (Facoltativo) CSV con i totali globali
)
