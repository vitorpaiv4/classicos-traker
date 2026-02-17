import sqlite3
import pandas as pd
import argparse

from database import criar_tabela, salvar_no_banco # Importar salvar_no_banco
from scraper import extrair_dados_olx

def analisar_dados():
    conn = sqlite3.connect('carros.db')
    df = pd.read_sql_query("SELECT * FROM anuncios", conn)
    conn.close()

    print("\n--- Análise de Dados ---")
    print("Cabeçalho do DataFrame:")
    print(df.head())
    print("\nEstatísticas Descritivas:")
    print(df.describe())
    print("\nInformações sobre valores nulos:")
    print(df.isnull().sum())
    print("\nContagem de anúncios por modelo:")
    print(df['modelo'].value_counts().head(10)) # Top 10 models

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ferramenta para rastrear anúncios de carros clássicos.")
    parser.add_argument('--scrape', action='store_true', help="Executa o scraper para coletar novos dados.")
    parser.add_argument('--analyze', action='store_true', help="Executa a análise dos dados coletados.")

    args = parser.parse_args()

    criar_tabela() # Sempre garante que a tabela exista

    if args.scrape:
        for carro in ['Fiat 147', 'Chevrolet Kadett']:
            print(f"Buscando dados para: {carro}...")
            dados = extrair_dados_olx(carro)
            salvar_no_banco(dados)
        print("Scraping concluído!")
    
    if args.analyze:
        analisar_dados()

    if not args.scrape and not args.analyze:
        print("Nenhuma ação especificada. Use --scrape ou --analyze.")