import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import config

# ========== Utility Functions ==========

def carica_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def salva_fig(percorso):
    if percorso:
        plt.savefig(percorso)
    plt.show()
    plt.close()


def carica_dataframe(csv_path):
    df = pd.read_csv(csv_path)
    return df


def normalizza_colonna(df, colonna, riempimento=''):
    df[colonna] = df[colonna].fillna(riempimento)
    return df


# ========== Analisi Categorie ==========

def conta_categorie(df, categorie):
    return df['Category'].value_counts().reindex(categorie.keys(), fill_value=0).to_dict()


def grafico_occorrenze_categorie(conteggio, save_path=None):
    dati_ordinati = dict(sorted(conteggio.items(), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(dati_ordinati.keys()), y=list(dati_ordinati.values()), palette='coolwarm')
    plt.xticks(rotation=45)
    plt.xlabel('Categorie')
    plt.ylabel('Numero di Occorrenze')
    plt.title('Occorrenze delle Categorie Riconosciute')
    plt.tight_layout()
    salva_fig(save_path)


def grafico_categorie_per_readme(df, save_path=None):
    df = normalizza_colonna(df, 'Category')
    matrice = pd.DataFrame(0, index=df['File_name'].unique(), columns=[])

    for _, row in df.iterrows():
        for cat in map(str.strip, row['Category'].split(',')):
            if cat:
                if cat not in matrice.columns:
                    matrice[cat] = 0
                matrice.at[row['File_name'], cat] = 1

    conteggi = matrice.sum(axis=1)
    distribuzione = conteggi.value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=distribuzione.index, y=distribuzione.values, palette='crest')
    plt.xlabel('Numero di Categorie nel README')
    plt.ylabel('Numero di README')
    plt.title('Distribuzione delle Categorie nei README')
    plt.tight_layout()
    salva_fig(save_path)


# ========== Analisi Lunghezza README ==========

def grafico_lunghezza_readme(percorso_csv, save_path=None):
    df = carica_dataframe(percorso_csv)
    df['Char_counts'] = pd.to_numeric(df['Char_counts'], errors='coerce').dropna()

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Char_counts', bins=20, kde=True, color='skyblue')
    plt.xscale('log')
    plt.xlabel('Numero di Caratteri nel README')
    plt.ylabel('Numero di File')
    plt.title('Distribuzione della Lunghezza dei README')
    plt.tight_layout()
    salva_fig(save_path)


def grafico_lunghezza_readme_fasce(percorso_csv, save_path=None):
    df = carica_dataframe(percorso_csv)
    df['Char_counts'] = pd.to_numeric(df['Char_counts'], errors='coerce').dropna()

    bins = [0, 1000, 5000, 10000, 20000, float('inf')]
    labels = ['Molto Corto (0-1k)', 'Corto (1k-5k)', 'Medio (5k-10k)', 'Lungo (10k-20k)', 'Molto Lungo (>20k)']
    df['Fascia Lunghezza'] = pd.cut(df['Char_counts'], bins=bins, labels=labels)

    distribuzione = df['Fascia Lunghezza'].value_counts().reindex(labels, fill_value=0)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=distribuzione.index, y=distribuzione.values, palette='crest')
    plt.xlabel('Fascia di Lunghezza dei README')
    plt.ylabel('Numero di README')
    plt.title('Distribuzione della Lunghezza dei README per Fasce')
    plt.tight_layout()
    salva_fig(save_path)


# ========== Analisi Rilevanza ==========

def aggiungi_rilevanza(percorso_csv, percorso_output=None):
    df = carica_dataframe(percorso_csv)

    pesi = {
        'Alta': {'description': 1.0, 'install': 1.0, 'prerequisites': 1.0, 'documentation': 1.0},
        'Media': {'configuration': 0.3, 'features': 0.3, 'testing': 0.3, 'performance': 0.3, 'title': 0.3},
        'Bassa': {'credits': 0.1, 'license': 0.1, 'contacts': 0.1, 'help': 0.1, 'feedback': 0.1, 'todo': 0.1}
    }

    df['Relevance_score'] = 0.0
    for categoria in pesi.values():
        for col, peso in categoria.items():
            if col in df.columns:
                df['Relevance_score'] += df[col] * peso
            else:
                print(f"Attenzione: Campo mancante nel CSV: '{col}'")

    output_path = percorso_output if percorso_output else percorso_csv
    df.to_csv(output_path, index=False)
    print(f"✅ File salvato con rilevanza: {output_path}")


# ========== Main Execution ==========

def main():
    df = carica_dataframe(config.NAME_FILE_CSV_OUT)
    df.fillna("Unknown", inplace=True)

    categorie = carica_json(os.path.join('in', 'tipologia.json'))
    conteggi = conta_categorie(df, categorie)

    grafico_occorrenze_categorie(conteggi, config.GRAPH_OUT_DIR + 'grafico1_occorrenze_categorie.pdf')
    grafico_categorie_per_readme(df, config.GRAPH_OUT_DIR + 'grafico2_distribuzione_categorie_readme.pdf')

    grafico_lunghezza_readme(
        config.TABLES_FILE_SUMMARY,
        config.GRAPH_OUT_DIR + 'grafico3_lunghezza_readme.pdf'
    )
    grafico_lunghezza_readme_fasce(
        config.TABLES_FILE_SUMMARY,
        config.GRAPH_OUT_DIR + 'grafico4_distribuzione_lunghezza_readme_per_fasce.pdf'
    )

    aggiungi_rilevanza(
        config.TABLES_FILE_SUMMARY,
        config.TABLES_OUT_DIR + 'readme_summary_relevance_score.csv'
    )


if __name__ == "__main__":
    main()
