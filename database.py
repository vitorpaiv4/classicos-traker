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

if __name__ == "__main__":
    criar_tabela()