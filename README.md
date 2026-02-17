# Classicos Tracker

## Descrição do Projeto
Este projeto é um rastreador de carros clássicos que coleta dados de anúncios online (atualmente da OLX), armazena-os em um banco de dados SQLite, permite a análise desses dados usando Pandas e oferece uma interface web para visualização e busca dinâmica.

## Funcionalidades
*   **Web Scraping:** Extrai informações de anúncios de carros da OLX (modelo, preço, ano, KM, URL).
*   **Banco de Dados:** Armazena os dados coletados em um banco de dados SQLite (`carros.db`).
*   **Análise de Dados:** Permite a análise dos dados coletados usando a biblioteca Pandas.
*   **Visualização Web:** Uma aplicação Flask que exibe os dados em uma tabela HTML com funcionalidades de busca e filtragem.
*   **Busca Dinâmica com Scraping On-Demand:** Se um termo de busca não for encontrado no banco de dados, a aplicação web tentará raspar os dados da OLX em tempo real para o termo buscado.
*   **Filtros de Pesquisa:** Filtra os resultados da busca por preço (mín/máx), ano (mín/máx) e quilometragem (mín/máx).
*   **Indicador de Carregamento:** Exibe um indicador visual durante o processo de busca/raspagem na interface web.
*   **Automação:** Configuração de um Cron Job para execução periódica do scraper.

## Tecnologias Utilizadas
*   **Python 3**
*   **BeautifulSoup4:** Para parsing de HTML no scraping.
*   **Requests:** Para fazer requisições HTTP.
*   **SQLite3:** Banco de dados leve e embarcado.
*   **Pandas:** Para manipulação e análise de dados.
*   **Flask:** Microframework web para a interface de usuário.
*   **argparse:** Para tratamento de argumentos de linha de comando no script principal.

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:vitorpaiv4/classicos-traker.git
    cd classicos-traker
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt # Se existir um requirements.txt
    # Caso contrário, instale manualmente:
    pip install requests beautifulsoup4 pandas Flask
    ```
    *(Nota: Um `requirements.txt` pode ser gerado com `pip freeze > requirements.txt`)*

## Uso

### 1. Inicialização do Banco de Dados
A tabela `anuncios` será criada automaticamente quando você executar o `main.py` com a opção `--scrape` ou iniciar o `app.py`.

### 2. Coleta de Dados (Scraping)
Para coletar dados de carros (ex: Fiat 147, Chevrolet Kadett) e armazená-los no `carros.db`:
```bash
python3 main.py --scrape
```

### 3. Análise de Dados
Para realizar uma análise básica dos dados já coletados (cabeçalho, estatísticas descritivas, contagem de modelos):
```bash
python3 main.py --analyze
```

### 4. Aplicação Web
Para iniciar a aplicação web Flask e visualizar os dados:
```bash
python3 app.py
```
Acesse a aplicação em seu navegador: `http://127.0.0.1:5000/`

Na interface web, você poderá:
*   Digitar um termo na barra de pesquisa para filtrar por modelo ou URL.
*   Usar os campos de "Preço Mínimo/Máximo", "Ano Mínimo/Máximo" e "KM Mínimo/Máximo" para refinar sua busca.
*   Se uma pesquisa (sem filtros adicionais) não encontrar resultados no banco, o sistema tentará raspar novos dados da OLX e adicioná-los.

## Automação (Cron Job)
Para automatizar a coleta de dados diária (ex: todo dia às 03:00 AM), adicione a seguinte linha ao seu crontab:

1.  Abra o crontab para edição:
    ```bash
    crontab -e
    ```
2.  Adicione a linha no final do arquivo e salve-o:
    ```
    0 3 * * * /home/paiva/projects/portfólio/classicos-tracker/venv/bin/python3 /home/paiva/projects/portfólio/classicos-tracker/main.py --scrape >> /tmp/classicos_tracker_cron.log 2>&1
    ```
    *(Ajuste o caminho para o seu ambiente virtual e o diretório do projeto se necessário)*

## Estrutura do Projeto
```
.
├── app.py              # Aplicação web Flask para visualização e busca
├── carros.db           # Banco de dados SQLite para armazenar os anúncios
├── database.py         # Funções para interação com o banco de dados (criar tabela, salvar dados)
├── main.py             # Script principal para scraping e análise (linha de comando)
├── scraper.py          # Lógica de web scraping para a OLX
├── templates/
│   └── index.html      # Template HTML para a interface web
└── venv/               # Ambiente virtual Python
    └── ...             # Dependências instaladas
```

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes (se aplicável).
