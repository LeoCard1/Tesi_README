#!/usr/bin/env python3
import subprocess

'''
1. controlla che i link siano in apps.csv presente nella cartella ../in
2. controlla che i file markdown in locale siano nella cartella ../mdfile

- rimuovi il contenuto di una cartella -> rm -rf /percorso/della/cartella/md_file/*
- rinomina i file nella cartella per ottenere il formato numerico nn.md 
- vai sulla cartella ->  rename 's/_readme//' (esempio: rimuove _readme dal nome del file cifra_readme.md ) 

- copia tutti i file in un altra cartella-> cp -r ~/percorso/origine/readmes/* ~/percorso/destinazione/md_file
'''

def main():
    while True:  # Loop per tornare al menu se l'utente sceglie "m1"
        print("\nScegli un'opzione:")
        print("1 - Carica i link da in/*.csv e analizza i READMEs (download.py)")
        print("2 - Carica READMEs da /md_files/*.md e analizza (process.py)")
        print("3 - Stampa grafici nella cartella /graphs (data_analysis_graph.py)")
        print("4 - Stampa sommario su CSV nella cartella /tables (generate_summary_csv.py)")
        print("5 - Esci")

        scelta = input("Scegli: ").strip().lower()

        if scelta == "1":
            subprocess.run([".venv\\Scripts\\python.exe", "download.py"])
            input("\nPremi 'invio' per tornare al menu principale: ")
        elif scelta == "2":
            subprocess.run([".venv\\Scripts\\python.exe", "process.py"])
            input("\nPremi 'invio' per tornare al menu principale: ")
        elif scelta == "3":
            subprocess.run([".venv\\Scripts\\python.exe", "data_analysis_graph.py"])
            input("\nPremi 'invio' per tornare al menu principale: ")
        elif scelta == "4":
            subprocess.run([".venv\\Scripts\\python.exe", "generate_summary_csv.py"])
            input("\nPremi 'invio' per tornare al menu principale: ")
        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()