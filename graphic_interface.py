import tkinter as tk
from collections import defaultdict
from datetime import datetime, timedelta
import mysql.connector
from tkinter import filedialog
import image_processing as ip
import database_statistics as ds

# Funcție pentru a verifica dacă a stat mai mult de 5 minute
def mai_mult_de_5_minute(durata):
    return durata.total_seconds() > 5 * 60

# Funcție pentru a actualiza tabelul cu statistica
def actualizare_statistica():
    # Șterge rândurile existente din tabel
    for widget in tabel_frame.winfo_children():
        widget.destroy()

    # Adaugă antetul tabelului
    tk.Label(tabel_frame, text="Număr", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
    tk.Label(tabel_frame, text="Timp", borderwidth=1, relief="solid").grid(row=0, column=1, sticky="nsew")
    tk.Label(tabel_frame, text="Reducere", borderwidth=1, relief="solid").grid(row=0, column=2, sticky="nsew")

    # Adaugă rândurile cu datele statistice
    row = 1
    for numar, timp in statistica.items():
        timp_delta = timedelta(seconds=timp)
        reducere = "Reducere disponibilă!" if mai_mult_de_5_minute(timp_delta) else "Fără reducere disponibilă"
        
        tk.Label(tabel_frame, text=str(numar), borderwidth=1, relief="solid").grid(row=row, column=0, sticky="nsew")
        tk.Label(tabel_frame, text=str(timp_delta), borderwidth=1, relief="solid").grid(row=row, column=1, sticky="nsew")
        tk.Label(tabel_frame, text=reducere, borderwidth=1, relief="solid").grid(row=row, column=2, sticky="nsew")
        
        row += 1

# Funcție pentru a încărca date din baza de date
def incarca_din_baza_de_date():
    try:
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Welcome@MGA123',
            'database': 'parcare'
        }
        conn = mysql.connector.connect(**db_config)  # Connect to the MySQL database
        cursor = conn.cursor()

        cursor.execute("SELECT numar_inmatriculare, ora_intrare, oras, ora_iesire, timp_total, suma_plata FROM intrari_parcare")
        
        # Clear existing data in the GUI table
        for widget in tabel_frame.winfo_children():
            widget.destroy()

        # Add table headers
        tk.Label(tabel_frame, text="Nr. Inmatriculare", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
        tk.Label(tabel_frame, text="Ora Intrare", borderwidth=1, relief="solid").grid(row=0, column=1, sticky="nsew")
        tk.Label(tabel_frame, text="Oras", borderwidth=1, relief="solid").grid(row=0, column=2, sticky="nsew")
        tk.Label(tabel_frame, text="Ora Iesire", borderwidth=1, relief="solid").grid(row=0, column=3, sticky="nsew")
        tk.Label(tabel_frame, text="Timp Total", borderwidth=1, relief="solid").grid(row=0, column=4, sticky="nsew")
        tk.Label(tabel_frame, text="Suma Plata", borderwidth=1, relief="solid").grid(row=0, column=5, sticky="nsew")

        row = 1
        for row_data in cursor.fetchall():
            for col, value in enumerate(row_data):
                tk.Label(tabel_frame, text=str(value), borderwidth=1, relief="solid").grid(row=row, column=col, sticky="nsew")
            row += 1

        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
# Funcție pentru a încărca calea unei fotografii
def incarca_cale_fotografie():
    fisier = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    photo_path_var.set(fisier)

# Funcție pentru a trimite calea fotografiei și a goli zona de text
def trimite_cale_fotografie():
    cale_fotografie = photo_path_var.get()
    if cale_fotografie:
        licence_number = ip.get_licence_number(cale_fotografie)
        ds.proceseaza_numar(licence_number)
        photo_path_var.set("")  # Golește zona de text

# Creare interfață grafică
root = tk.Tk()
root.title("Statistica numere")

# Buton pentru încărcarea numerelor din baza de date
incarca_button = tk.Button(root, text="Încarcă numere din baza de date", command=incarca_din_baza_de_date)
incarca_button.pack()

# Frame pentru tabel
tabel_frame = tk.Frame(root)
tabel_frame.pack()

# Dicționar pentru a ține evidența timpului de intrare pentru fiecare număr
last_timestamp = {}

# Dicționar pentru a stoca cât timp a stat fiecare număr
statistica = defaultdict(int)

# Text area pentru afișarea căii fotografiei
photo_path_var = tk.StringVar()
photo_path_entry = tk.Entry(root, textvariable=photo_path_var, width=50)
photo_path_entry.pack()

# Buton pentru încărcarea căii unei fotografii
incarca_fotografie_button = tk.Button(root, text="Încarcă fotografie", command=incarca_cale_fotografie)
incarca_fotografie_button.pack()

# Buton pentru trimiterea căii fotografiei și golirea zonei de text
trimite_fotografie_button = tk.Button(root, text="Trimite cale fotografie", command=trimite_cale_fotografie)
trimite_fotografie_button.pack()

# Actualizarea statisticilor la început
actualizare_statistica()

# Rularea buclei principale a interfeței grafice
root.mainloop()

# Configurația bazei de date

