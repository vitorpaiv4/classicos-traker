from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from scraper import extrair_dados_olx
from database import salvar_no_banco, criar_tabela

app = Flask(__name__)

def get_car_data(search_term=None, min_price=None, max_price=None, min_year=None, max_year=None, min_km=None, max_km=None):
    criar_tabela() 

    conn = sqlite3.connect('carros.db')
    where_clauses = []
    params = []

    if search_term:
        where_clauses.append("(modelo LIKE ? COLLATE NOCASE OR url LIKE ?)")
        params.extend([f"%{search_term}%", f"%{search_term}%"])

    if min_price is not None:
        where_clauses.append("preco >= ?")
        params.append(min_price)
    if max_price is not None:
        where_clauses.append("preco <= ?")
        params.append(max_price)
    if min_year is not None:
        where_clauses.append("ano >= ?")
        params.append(min_year)
    if max_year is not None:
        where_clauses.append("ano <= ?")
        params.append(max_year)
    if min_km is not None:
        where_clauses.append("km >= ?")
        params.append(min_km)
    if max_km is not None:
        where_clauses.append("km <= ?")
        params.append(max_km)

    query = "SELECT * FROM anuncios"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    df = pd.read_sql_query(query, conn, params=params)

    # --- Lógica de scraping on-demand ---
    # Se a busca principal (com search_term) não retornar resultados e houver um search_term
    # E não houver outros filtros que possam restringir demais a busca para acionar o scrape indevidamente
    if search_term and df.empty and not any([min_price, max_price, min_year, max_year, min_km, max_km]):
        print(f"Nenhum resultado encontrado para '{search_term}' no banco de dados. Buscando na OLX...")
        new_data = extrair_dados_olx(search_term)
        if new_data:
            salvar_no_banco(new_data)
            print(f"Novos dados para '{search_term}' salvos no banco de dados.")
            # Após salvar, reconsultamos o banco de dados para incluir os novos dados
            df = pd.read_sql_query(query, conn, params=params) # Re-query with original filters
        else:
            print(f"Nenhum dado encontrado para '{search_term}' na OLX.")
    # --- Fim da lógica de scraping on-demand ---
            
    conn.close()
    return df.to_dict(orient='records')

@app.route('/')
def index():
    search_term = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_year = request.args.get('min_year', type=int)
    max_year = request.args.get('max_year', type=int)
    min_km = request.args.get('min_km', type=int)
    max_km = request.args.get('max_km', type=int)

    car_data = get_car_data(search_term, min_price, max_price, min_year, max_year, min_km, max_km)
    
    return render_template('index.html', 
                           cars=car_data, 
                           search_term=search_term,
                           min_price=min_price, max_price=max_price,
                           min_year=min_year, max_year=max_year,
                           min_km=min_km, max_km=max_km)

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True, host='0.0.0.0')