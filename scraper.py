import requests
from bs4 import BeautifulSoup
import re

def extrair_dados_olx(termo_busca):
    # Cabeçalho para o site não bloquear o acesso
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # URL de busca (Exemplo simplificado)
    url = f"https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?q={termo_busca}"
    
    resultados = [] # Inicializa resultados antes do try
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all individual ad containers
        anuncios = soup.find_all('div', class_='olx-adcard__content') 

        for anuncio_div in anuncios: 
            # Extrair URL
            url_tag = anuncio_div.find('a', class_='olx-adcard__link')
            url = url_tag.get('href') if url_tag else 'N/A'

            # Extrair modelo (title)
            modelo_tag = anuncio_div.find('h2', class_='olx-adcard__title')
            modelo_full_text = modelo_tag.text.strip() if modelo_tag else 'N/A'

            # Extrair ano do texto completo do modelo usando regex
            ano = 'N/A'
            ano_match = re.search(r'\b(19|20)\d{2}\b', modelo_full_text) 
            if ano_match:
                try:
                    ano = int(ano_match.group(0))
                except ValueError:
                    pass
            
            # Extrair preço
            preco_tag = anuncio_div.find('h3', class_='olx-adcard__price')
            preco_text = preco_tag.text.strip() if preco_tag else 'R$ 0'
            try:
                preco = float(preco_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
            except ValueError:
                preco = 0.0 # Default value if conversion fails


            # Extrair km
            km_tag = anuncio_div.find('div', class_='olx-adcard__detail', attrs={'aria-label': lambda x: x and 'quilômetros rodados' in x})
            km = 'N/A'
            if km_tag:
                km_text = km_tag.text.strip().lower().replace('km', '').replace('.', '') # Remove 'km' and '.'
                try:
                    km = int("".join(filter(str.isdigit, km_text))) # Extract only digits
                except ValueError:
                    km = 'N/A'

            resultados.append({
                'modelo': modelo_full_text, 
                'preco': preco,
                'ano': ano,
                'km': km,
                'url': url
            })
        
        return resultados
        
    except Exception as e:
        print(f"E2rro ao acessar o site: {e}")
        return resultados22