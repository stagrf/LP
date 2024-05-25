import mysql.connector
import time

# dictionar cu prefixele
prefixe_orase = {
    'B': 'București', 'AB': 'Alba', 'AR': 'Arad', 'AG': 'Argeș', 'BC': 'Bacău', 'BH': 'Bihor', 'BN': 'Bistrița-Năsăud', 'BR': 'Brăila',
    'BT': 'Botoșani', 'BV': 'Brașov', 'BZ': 'Buzău', 'CS': 'Caraș-Severin', 'CL': 'Călărași', 'CJ': 'Cluj', 'CT': 'Constanța', 'CV': 'Covasna',
    'DB': 'Dâmbovița', 'DJ': 'Dolj', 'GL': 'Galați', 'GR': 'Giurgiu', 'GJ': 'Gorj', 'HR': 'Harghita', 'HD': 'Hunedoara', 'IL': 'Ialomița',
    'IS': 'Iași', 'IF': 'Ilfov', 'MM': 'Maramureș', 'MH': 'Mehedinți', 'MS': 'Mureș', 'NT': 'Neamț', 'OT': 'Olt', 'PH': 'Prahova',
    'SM': 'Satu Mare', 'SJ': 'Sălaj', 'SB': 'Sibiu', 'SV': 'Suceava', 'TR': 'Teleorman', 'TM': 'Timiș', 'TL': 'Tulcea', 'VS': 'Vaslui',
    'VL': 'Vâlcea', 'VN': 'Vrancea'
}

# configurația bazei de date
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Samurai.ninja14',
    'database': 'parcare1'
}

# conectarea la baza de date
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


timp_intrare_dict = {}

#  identifica orașul
def identifica_oras(nr_inmatriculare):
    litere = []
    for char in nr_inmatriculare:
        #if char.isalpha():
            litere.append(char)
    prefix = ''.join(litere[:2])
    return prefixe_orase.get(prefix, 'Necunoscut')

#  inregistre intrarea în baza de date
def inregistrare_intrare(nr_inmatriculare, timp_intrare):
    ora_intrare = time.strftime('%H:%M:%S', time.localtime(timp_intrare))
    oras = identifica_oras(nr_inmatriculare)
    cursor.execute("""
        INSERT INTO intrari_parcare (numar_inmatriculare, ora_intrare, oras) 
        VALUES (%s, %s, %s)
    """, (nr_inmatriculare, ora_intrare, oras))
    conn.commit()

#  inregistrare iesire
def inregistrare_iesire(nr_inmatriculare, timp_intrare, timp_iesire):
    ora_iesire = time.strftime('%H:%M:%S', time.localtime(timp_iesire))
    timp_total = (timp_iesire - timp_intrare) / 60
    suma_plata = timp_total * 0.1  # 0.1 lei per minut
    cursor.execute("""
        UPDATE intrari_parcare
        SET ora_iesire = %s, timp_total = %s, suma_plata = %s
        WHERE numar_inmatriculare = %s AND ora_iesire IS NULL
    """, (ora_iesire, timp_total, suma_plata, nr_inmatriculare))
    conn.commit()

# pentru a procesa un numar de inmatriculare
def proceseaza_numar(nr_inmatriculare):
    timp_actual = time.time()
    if nr_inmatriculare in timp_intrare_dict:
        print(f"Masina cu numarul {nr_inmatriculare} a iesit din parcare.")
        timp_intrare = timp_intrare_dict.pop(nr_inmatriculare)
        inregistrare_iesire(nr_inmatriculare, timp_intrare, timp_actual)
        timp_total = (timp_actual - timp_intrare) / 60
        suma_plata = timp_total * 0.1  # 0.1 lei per minut
        print(f"A petrecut {timp_total:.1f} minute in parcare.")
        print(f"Suma de plata este {suma_plata:.2f} lei.")
    else:
        print(f"Masina cu numarul {nr_inmatriculare} a intrat in parcare.")
        inregistrare_intrare(nr_inmatriculare, timp_actual)
        timp_intrare_dict[nr_inmatriculare] = timp_actual

# pentru a citi numerele de inmatriculare intr-o bucla infinita
def citeste_numere():
    while True:
        nr_inmatriculare = input("Introduceti numarul de inmatriculare sau 'exit' pentru a iesi: ")
        if nr_inmatriculare.lower() == 'exit':
            break
        proceseaza_numar(nr_inmatriculare)

# apelam funcaia
citeste_numere()

# inchide conexiunea la baza de date
cursor.close()
conn.close()