from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from scraper import extrair_dados_olx # Importar o scraper
from database import salvar_no_banco, criar_tabela # Importar salvar_no_banco e criar_tabela

app = Flask(__name__)

def get_car_data(search_term=None):
    # Garante que a tabela exista antes de qualquer operação
    criar_tabela() 

    conn = sqlite3.connect('carros.db')
    query = "SELECT * FROM anuncios"
    
    # Se houver um termo de busca, tentamos filtrar primeiro
    if search_term:
        # Busca no banco de dados por termo (case-insensitive para modelo)
        # O COLLATE NOCASE funciona para SQLite, outros bancos podem usar LOWER()
        filtered_query = f"SELECT * FROM anuncios WHERE modelo LIKE '%{search_term}%' COLLATE NOCASE OR url LIKE '%{search_term}%'"
        df = pd.read_sql_query(filtered_query, conn)
        
        if df.empty:
            # Se não encontrou resultados, tentamos buscar na OLX
            print(f"Nenhum resultado encontrado para '{search_term}' no banco de dados. Buscando na OLX...")
            new_data = extrair_dados_olx(search_term)
            if new_data:
                salvar_no_banco(new_data)
                print(f"Novos dados para '{search_term}' salvos no banco de dados.")
                # Após salvar, reconsultamos o banco de dados para incluir os novos dados
                df = pd.read_sql_query(filtered_query, conn)
            else:
                print(f"Nenhum dado encontrado para '{search_term}' na OLX.")
    else:
        # Se não há termo de busca, retorna todos os anúncios
        df = pd.read_sql_query(query, conn)
        
    conn.close()
    return df.to_dict(orient='records')

@app.route('/')
def index():
    search_term = request.args.get('search')
    car_data = get_car_data(search_term)
    return render_template('index.html', cars=car_data, search_term=search_term)

if __name__ == '__main__':
    # Antes de iniciar o app, crie a tabela para garantir que exista
    criar_tabela()
    app.run(debug=True, host='0.0.0.0') # Alterado para 0.0.0.0 para ser acessível externamente se necessário
