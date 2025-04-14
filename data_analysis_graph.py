import os  # Modulo per operazioni su file e percorsi
import pandas as pd  # Libreria per la manipolazione dei dati (DataFrame)
import matplotlib.pyplot as plt  # Libreria per la generazione di grafici
import seaborn as sns  # Libreria di visualizzazione dati, integrata con matplotlib
import json  # Per leggere/scrivere file JSON
import config  # Modulo di configurazione con percorsi e costanti


def load_categories_from_json(json_file):
    """
    Carica un dizionario di categorie da un file JSON.

    Parametri:
    - json_file (str): Percorso del file JSON.

    Ritorna:
    - dict: Dizionario delle categorie.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def count_categories(df, categories):
    """
    Conta quante volte ciascuna categoria compare nel DataFrame.

    Parametri:
    - df (DataFrame): Il DataFrame che contiene la colonna 'Category'.
    - categories (dict): Dizionario di categorie da considerare.

    Ritorna:
    - dict: Conteggio delle categorie presenti nel DataFrame.
    """
    category_count = {category: 0 for category in categories.keys()}
    for category in df['Category']:
        if category in category_count:
            category_count[category] += 1
    return category_count


def plot_category_counts(data, save_path=None):
    """
    Crea un grafico a barre per visualizzare la quantità di occorrenze per ciascuna categoria.

    Parametri:
    - data (dict): Dizionario con categorie e relativo conteggio.
    - save_path (str, opzionale): Percorso dove salvare il grafico. Se None, non lo salva.

    Ritorna:
    - None
    """
    categories = list(data.keys())
    counts = list(data.values())

    plt.figure(figsize=(12, 6))
    sns.barplot(x=categories, y=counts, palette='coolwarm')  # Crea grafico a barre
    plt.xticks(rotation=45)
    plt.xlabel('Categorie')
    plt.ylabel('Numero di Occorrenze')
    plt.title('Occorrenze delle Categorie Riconosciute')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)  # Salva il grafico se specificato

    plt.show()  # Mostra il grafico
    plt.close()  # Chiude per evitare problemi con grafici successivi


def plot_readme_by_category_count(df, save_path=None):
    """
    Crea un grafico che mostra quanti README hanno 0, 1, 2, ... categorie assegnate.

    Parametri:
    - df (DataFrame): Il DataFrame con le informazioni dei README.
    - save_path (str, opzionale): Percorso dove salvare il grafico.

    Ritorna:
    - None
    """
    df['Category'] = df['Category'].fillna('')  # Rimpiazza NaN con stringa vuota

    # Ottiene tutte le categorie uniche (escludendo vuote)
    category_columns = list(df['Category'].unique())
    category_columns = [cat for cat in category_columns if cat.strip() != '']

    # Crea una matrice che associa ogni file alle categorie (1 se presente)
    category_matrix = pd.DataFrame(0, index=df['File_name'].unique(), columns=category_columns)

    for _, row in df.iterrows():
        categories = row['Category'].split(',')  # Alcuni README possono avere più categorie separate da virgole
        for cat in categories:
            if cat.strip():
                category_matrix.loc[row['File_name'], cat.strip()] = 1

    # Somma quante categorie ha ciascun file
    category_counts = category_matrix.sum(axis=1)

    # Range completo da 0 al massimo di categorie riconosciute in un file
    max_categories = category_counts.max()
    full_range = range(0, max_categories + 1)

    # Calcola la distribuzione (quanti README hanno 0, 1, 2, ecc. categorie)
    distribution = category_counts.value_counts().reindex(full_range, fill_value=0).sort_index()

    # Plot del grafico
    plt.figure(figsize=(10, 6))
    sns.barplot(x=distribution.index, y=distribution.values, palette='crest')
    plt.xlabel('Numero di Categorie Riconosciute nel README')
    plt.ylabel('Numero di README')
    plt.title('Distribuzione delle Categorie Riconosciute nei README')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)  # Salva se specificato

    plt.show()
    plt.close()


def main():
    """
    Funzione principale: carica i dati, conta le categorie e genera i grafici.
    """
    # Carica il DataFrame principale dal CSV
    df_main = pd.read_csv(config.NAME_FILE_CSV_OUT)

    # Carica il file JSON con le definizioni delle categorie
    json_file_path = os.path.join('in', 'tipologia.json')
    categories = load_categories_from_json(json_file_path)

    # Rimpiazza eventuali valori mancanti nella colonna Category con "Unknown"
    df_main.fillna("Unknown", inplace=True)

    # Conta le occorrenze delle categorie
    category_counts = count_categories(df_main, categories)

    # Crea e salva il primo grafico: quante volte appare ogni categoria
    plot_category_counts(
        category_counts,
        save_path=config.GRAPH_OUT_DIR + 'grafico1_occorrenze_categorie.pdf'
    )

    # Crea e salva il secondo grafico: distribuzione dei README per numero di categorie
    plot_readme_by_category_count(
        df_main,
        save_path=config.GRAPH_OUT_DIR + 'grafico2_distribuzione_categorie_readme.pdf'
    )


# Esegue lo script solo se lanciato direttamente (non se importato)
if __name__ == "__main__":
    main()
