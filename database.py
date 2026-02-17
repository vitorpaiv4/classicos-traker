import sqlite3

def criar_tabela():
    conn = sqlite3.connect('carros.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anuncios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            preco REAL,
            ano INTEGER,
            km INTEGER,
            url TEXT UNIQUE,
            data_coleta DATE DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    conn.close()

def salvar_no_banco(dados):
    conn = sqlite3.connect('carros.db')
    cursor = conn.cursor()
    for item in dados:
        try:
            cursor.execute('''
                INSERT INTO anuncios (modelo, preco, ano, km, url) 
                VALUES (?, ?, ?, ?, ?)
            ''', (item['modelo'], item['preco'], item['ano'], item['km'], item['url']))
        except sqlite3.IntegrityError:
            pass # Ignora se a URL já existir (anúncio duplicado)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela()
    # If this module is run directly, it will only create the table.
    # The scraping and saving logic is now orchestrated by main.py or app.py
