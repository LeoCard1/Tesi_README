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
    while True:  # Loop per tornare al menu se l'utente sceglie "m1
        print("\nScegli un'opzione:")
        print("1 - Carica README da elenco CSV e processa (download.py)")
        print("2 - Carica README da locale e processa (process.py)")
        print("3 - Analizza (statistics.py)")
        print("4 - Esci")

        scelta = input("Scegli: ").strip().lower()

        if scelta == "1":

            subprocess.run([".venv\\Scripts\\python.exe", "download.py"])
            azione = input(
                "\nPremi 'invio' per tornare al menu principale: ").strip().lower()
            if azione == "":
                continue  # Torna al menu

        elif scelta == "2":
            subprocess.run([".venv\\Scripts\\python.exe", "process.py"])
            azione = input(
                "\nPremi 'invio' per tornare al menu principale: ").strip().lower()
            if azione == "":
                continue  # Torna al menu

        elif scelta == "3":
            subprocess.run([".venv\\Scripts\\python.exe", "statistics.py"])
            azione = input(
                "\nPremi 'invio' per tornare al menu principale: ").strip().lower()
            if azione == "":
                continue  # Torna al menu

        elif scelta == "4":
            print("Uscita dal programma...")
            break  # Esce dal loop e termina il programma

        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()