import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Welcome@MGA123',
    'database': 'parcare'
}

# Funcție pentru a crea baza de date și tabelul necesar
def creaza_baza_de_date():
    try:
        # Conectare la baza de date MySQL
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS intrari_parcare (
                    numar_inmatriculare VARCHAR(20),
                    ora_intrare DATETIME,
                    oras VARCHAR(50),
                    ora_iesire DATETIME,
                    timp_total FLOAT,
                    suma_plata FLOAT,
                    nr_inmatriculare VARCHAR(20)
                )
            ''')
            conn.commit()
            print("Tabela a fost creată cu succes!")
    except Error as e:
        print(f"Eroare la conectarea la baza de date: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Apelarea funcției pentru a crea baza de date
creaza_baza_de_date()
