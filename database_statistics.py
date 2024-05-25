import mysql.connector
import time

# Dictionary with city prefixes
prefixe_orase = {
    'B': 'București', 'AB': 'Alba', 'AR': 'Arad', 'AG': 'Argeș', 'BC': 'Bacău', 'BH': 'Bihor', 'BN': 'Bistrița-Năsăud', 'BR': 'Brăila',
    'BT': 'Botoșani', 'BV': 'Brașov', 'BZ': 'Buzău', 'CS': 'Caraș-Severin', 'CL': 'Călărași', 'CJ': 'Cluj', 'CT': 'Constanța', 'CV': 'Covasna',
    'DB': 'Dâmbovița', 'DJ': 'Dolj', 'GL': 'Galați', 'GR': 'Giurgiu', 'GJ': 'Gorj', 'HR': 'Harghita', 'HD': 'Hunedoara', 'IL': 'Ialomița',
    'IS': 'Iași', 'IF': 'Ilfov', 'MM': 'Maramureș', 'MH': 'Mehedinți', 'MS': 'Mureș', 'NT': 'Neamț', 'OT': 'Olt', 'PH': 'Prahova',
    'SM': 'Satu Mare', 'SJ': 'Sălaj', 'SB': 'Sibiu', 'SV': 'Suceava', 'TR': 'Teleorman', 'TM': 'Timiș', 'TL': 'Tulcea', 'VS': 'Vaslui',
    'VL': 'Vâlcea', 'VN': 'Vrancea'
}

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Welcome@MGA123',
    'database': 'parcare'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Dictionary to store entry times for vehicles
timp_intrare_dict = {}

# Function to identify the city
def identifica_oras(nr_inmatriculare):
    prefix = nr_inmatriculare[:2]
    return prefixe_orase.get(prefix, 'Necunoscut')

# Function to record entry in the database
def inregistrare_intrare(nr_inmatriculare, timp_intrare):
    ora_intrare = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timp_intrare))
    oras = identifica_oras(nr_inmatriculare)
    try:
        cursor.execute("""
            INSERT INTO intrari_parcare (numar_inmatriculare, ora_intrare, oras) 
            VALUES (%s, %s, %s)
        """, (nr_inmatriculare, ora_intrare, oras))
        conn.commit()
        print("Intrare înregistrată cu succes!")
    except mysql.connector.Error as err:
        print(f"Eroare la înregistrarea intrării în bază de date: {err}")

# Function to record exit
def inregistrare_iesire(nr_inmatriculare, timp_intrare, timp_iesire):
    ora_iesire = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timp_iesire))
    timp_total = (timp_iesire - timp_intrare) / 60
    suma_plata = timp_total * 0.1  # 0.1 lei per minut
    try:
        cursor.execute("""
            UPDATE intrari_parcare
            SET ora_iesire = %s, timp_total = %s, suma_plata = %s
            WHERE numar_inmatriculare = %s AND ora_iesire IS NULL
        """, (ora_iesire, timp_total, suma_plata, nr_inmatriculare))
        conn.commit()
        print("Ieșire înregistrată cu succes!")
    except mysql.connector.Error as err:
        print(f"Eroare la înregistrarea ieșirii în bază de date: {err}")

# Function to process a license plate number
def proceseaza_numar(nr_inmatriculare):
    timp_actual = time.time()
    if nr_inmatriculare in timp_intrare_dict:
        print(f"Mașina cu numărul {nr_inmatriculare} a ieșit din parcare.")
        timp_intrare = timp_intrare_dict.pop(nr_inmatriculare)
        inregistrare_iesire(nr_inmatriculare, timp_intrare, timp_actual)
        timp_total = (timp_actual - timp_intrare) / 60
        suma_plata = timp_total * 0.1  # 0.1 lei per minut
        print(f"A petrecut {timp_total:.1f} minute în parcare.")
        print(f"Suma de plată este {suma_plata:.2f} lei.")
    else:
        print(f"Mașina cu numărul {nr_inmatriculare} a intrat în parcare.")
        inregistrare_intrare(nr_inmatriculare, timp_actual)
        timp_intrare_dict[nr_inmatriculare] = timp_actual

# Function to read license plate numbers in an infinite loop
def citeste_numere():
    try:
        while True:
            nr_inmatriculare = input("Introduceți numărul de înmatriculare sau 'exit' pentru a ieși: ")
            if nr_inmatriculare.lower() == 'exit':
                break
            proceseaza_numar(nr_inmatriculare)
    except KeyboardInterrupt:
        print("\nAplicația a fost întreruptă manual.")

# # Close the database connection
# cursor.close()
# conn.close()

# # Call the function to read license plate numbers
# citeste_numere()
