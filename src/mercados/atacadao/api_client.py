#Imports gerais
from datetime import datetime
import json
import math
import os
import requests

# Imports do selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Imports do atacadao
from prog_config.settings import ATACADAO_API_DEPARTAMENTOS, ATACADAO_HOME, DB_PATH, DEFAULT_HEADERS, MERCADOS
#from mercados.atacadao import login
from src.mercados.atacadao.parser import Departamento, Produto, Preco
from src.database.manager import salvar_departamento, salvar_produto, pesquisa_preco_produto, pesquisa_log_preco, pesquisa_produto_db_por_id
from src.database.models import criar_tabela_departamentos, criar_tabela_log_preco, criar_tabela_preco, criar_tabela_produtos
from src.database import database, manager
from prog_config.proxy_manager import fazer_requisicao, PROXY_USERNAME, PROXY_PASSWORD
from src.core.utils import delay_inteligente

def preparar_navegador_atacadao():
    # Passo 1: config para navegador brave
    brave_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application'
    chrome_options = Options()
    chrome_options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # Passo 2: Conecta ao navegador Brave já em execução
    driver_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\chromedriver-win64\\chromedriver.exe'
    service = Service(executable_path=driver_path)

    # Passo 3: Carregando webdriver para acessar a pagina
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(30)

    # Passo 4: Abre uma nova aba usando JavaScript
    driver.execute_script("window.open('');")

    # Passo 5: Muda para a nova aba
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url=ATACADAO_HOME)


# =============================================================
#                         ATACADAO
# =============================================================
    
def coleta_departamento():

    # 1o: Verificando a resposta da API Shibata e coletar dados
    url_departamentos = ATACADAO_API_DEPARTAMENTOS

        # Requisição para a API do Atacadão
    #response = requests.get(url = url_departamentos, headers = DEFAULT_HEADERS["atacadao"])
    response = fazer_requisicao(
        url=url_departamentos,
        username=PROXY_USERNAME,
        password=PROXY_PASSWORD,
        headers=DEFAULT_HEADERS["atacadao"]
    )
    try:
        if response.status_code == 200:
            print(f"Acesso a API concedido")
            dados = response.json()["pageProps"]["cmsMenuCategory"]["menu"]["menuCategories"]["menuItems"]

            """
            ========================
            Iniciar o banco de dados
            ========================
            """
            criar_tabela_departamentos(db_path=DB_PATH["atacadao"])

            """
            ========================
            Inicio coleta no shibata
            &
            Armazenamento de dados
            ========================
            """

            # 2o: Parsear (tratar) os dados em objetos departamento
            departamentos = Departamento.parse_departamento(data=dados)
                    
            # 3o: Salvar cada departamento no banco
            for dept in departamentos:
                salvar_departamento(db_path=DB_PATH["atacadao"], departamento_data=dept.to_dict())
                delay_inteligente()
                print(f"Departamento {dept.descricao}, salvo com sucesso")
            

        else:
            print("Erro ao acessar API:", response.status_code, response.text)
    except Exception as e:
        print(f"Erro no departamento: {e}")


def coleta_produtos(db_path:str, mercado:int) -> None:
    pesquisa_dept = manager.pesquisa_de_departamentos(db_path=db_path,mercado=mercado)
       
    """
    =================================================
                Iniciar o banco de dados
    =================================================
    """
    criar_tabela_produtos(db_path=db_path)
    criar_tabela_preco(db_path=db_path)
    criar_tabela_log_preco(db_path=db_path)

    """
    =================================================
    Inicio coleta no de departamentos no atacadao
                        &
                Armazenamento de dados
    ================================================
    """

    for departamento in pesquisa_dept:
        scan_all_departments(departments=departamento)


def scan_all_departments(departments):
    #variaveis globais do funçao
    all_products = []
    items_per_page = 40
    contagem_prod = 0
    nome_dep = departments[0]
    link_dep = departments[1]
    page = 1
    temp_dep = datetime.now()

    #ajuste do link de departamento para alguns links    
    link_dep = link_dep.replace("/","")
    if "?" in link_dep:
        link_dep = link_dep.split('?')[0]

    
    print(f"\n[+] Buscando produtos no departamento: {nome_dep}")

    # 1o: buscar lista de produtos por pagina em um departamento especifico
    result = busca_products(department=link_dep, page=page,items_per_page=items_per_page, facetsValue=link_dep)

    # calculo da quantidade de paginas a ser pesquisada
    total_prod = result["data"]["search"]["products"]["pageInfo"]["totalCount"]
    total_pag = math.ceil(total_prod / items_per_page)

    while total_prod > contagem_prod:
        t_ini = datetime.now()
        print(f"[Página {page}] Coletando produtos de {nome_dep}...")
        page += 1

        #condição de fim do laço com base no nº de paginas
        contagem_prod += items_per_page
        if not result or "data" not in result:
            print("[-] Erro ou fim de página.")
            break
        
        if result is None:
            print("Erro: A variável 'result' está vazia (None).")
            return # Ou levantar uma exceção apropriada, ou tentar novamente

        if "data" not in result or result["data"] is None:
            print("Erro: 'data' não encontrado ou é None em 'result'.")
            return

        if "search" not in result["data"] or result["data"]["search"] is None:
            print("Erro: 'search' não encontrado ou é None em 'result['data']'.")
            return

        if "products" not in result["data"]["search"] or result["data"]["search"]["products"] is None:
            print("Erro: 'products' não encontrado ou é None em 'result['data']['search']'.")
            # Imprima 'result' completo para depurar a estrutura da resposta
            print(f"Estrutura de result['data']['search'] para depuração: {result['data']['search']}")
            return

        #TODO: Refatorar posteriormente o codigo para iterar sobre cada item da lista products_data e nao sobre as listas normalisadas 

        # Se todas as verificações passarem, então é seguro acessar 'edges'

        products_data = result["data"]["search"]["products"]["edges"]
        
        # 2º: Parsear (tratar) os dados em objetos departamento
        produtos = Produto.parse_produto(data=products_data)

        # 3º Verificar atualizações de preço
        precos = Preco.parse_preco_from_produtos(produtos_data=products_data)
        for preco in precos:
            #Busca de itens nos bancos de dados
            ultimo_log = pesquisa_log_preco(produto_id=preco.produto_id, db_path=DB_PATH["atacadao"])
            ultimo_preco = pesquisa_preco_produto(produto_id=preco.produto_id, mercado=MERCADOS["atacadao"])
            status_alt_preco = Preco.compara_mudanca_preco(preco=preco, ultimo_preco=ultimo_preco)

            #verificação se os preços existem no banco de dados ou se sao a primeira inserção
            if len(ultimo_preco) == 0:
                manager.salvar_preco_produto(db_path=DB_PATH["atacadao"], preco_produto_data=Preco.to_dict(preco))
            elif len(ultimo_log) == 0:
                Preco.inserir_log_precos(preco=preco, db_path=DB_PATH["atacadao"])

            # Verifica se o preço foi alterado ou não
            if status_alt_preco["mudou"]:
                Preco.atualizar_novo_preco(preco=preco, ultimo_preco=ultimo_preco)
                Preco.inserir_log_precos(preco=preco, db_path=DB_PATH["atacadao"])
                print(f"Preço do produto {preco.produto_id}, mudou!")
        
            else:
                Preco.atualizar_preco_nao_atualizado(preco=preco, ultimo_preco=ultimo_preco)
                print(f"Preço do produto {preco.produto_id}, não mudou!")

        # 4o: Verifica o link das imagens
        for item in produtos:
            print("pesquisando imagem")
            pesquisa_prod = pesquisa_produto_db_por_id(produto_id=item.produto_id, mercado=MERCADOS["atacadao"])
            produto_id = int(item.produto_id)
            pesquisa_prod_id = pesquisa_prod[0][1] if len(pesquisa_prod) != 0 else 0
            pesquisa_prod_imagem = pesquisa_prod[0][5] if len(pesquisa_prod) != 0 else 0
            if produto_id == pesquisa_prod_id:
                if item.imagem != pesquisa_prod_imagem:
                    manager.atualizar_link_imagem(db_path=DB_PATH["atacadao"], preco_produto_data=(item.produto_id, item.imagem))
                print("produto ja existe no banco de dados, somente a imagem foi atualizada")

                        
        # 5o: Salvar cada produto no banco se ele não existir
        for item in produtos:
            pesquisa_prod = pesquisa_produto_db_por_id(produto_id=item.produto_id, mercado=MERCADOS["atacadao"])
            produto_id = int(item.produto_id)
            pesquisa_prod = pesquisa_prod[0][1] if len(pesquisa_prod) != 0 else 0
            if produto_id == pesquisa_prod:
                print("produto ja existe no banco de dados, somente o preço foi atualizado")
            else:
                salvar_produto(db_path=DB_PATH["atacadao"], produto_data=item.to_dict())
                print(f"Produto {item.descricao}, salvo com sucesso")

            #t_final=datetime.now()
            
        print(f'Pagina {page} terminou de um total de {total_pag} paginas')  
        result = busca_products(department=nome_dep, page=page, facetsValue=link_dep)
        #tempo_total= t_final-t_ini
        #print(tempo_total)
        
    tempo_gasto = datetime.now() - temp_dep
    print(f"Tempo gasto para o departamemnto {nome_dep} foi: ", tempo_gasto)
    #return all_products  


def busca_products(department, page=1, items_per_page=40,
                    facetsValue=None):
    url = "https://www.atacadao.com.br/api/graphql? "

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    after = str(0)

    if page > 1:
        after = str((page - 1) * items_per_page)
        
    variables = {
        "first": items_per_page,
        "after": after,
        "sort": "score_desc",
        "term": "",
        "selectedFacets": [
            {"key": "category-1", "value": facetsValue},
            {"key": "channel", "value": "{\"salesChannel\":\"1\",\"seller\":\"atacadaobr744\",\"regionId\":\"U1cjYXRhY2FkYW9icjc0NA==\"}"},
            {"key": "locale", "value": "pt-BR"}
        ]
    }
    params = {
        "operationName": "ProductsQuery",
        "variables": json.dumps(variables)
    }
    
    try:
        #response = requests.get(url, headers=headers, params=params)
        response = fazer_requisicao(
            url=url,
            username=PROXY_USERNAME,
            password=PROXY_PASSWORD,
            headers=headers,
            params=params
        )
        if response.status_code == 429:
            print("Limite de requisições atingido. Esperando 10s...")
            delay_inteligente()
            return busca_products(department=department, page=page, items_per_page=items_per_page, facetsValue=facetsValue)
        elif response.status_code == 200:
                delay_inteligente()
                return response.json()
    
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None


def query_de_atualizacao(db_path):
    Produto.cadastro_cod_barras()

def download_img(db_path):
    #url_base = IMAGE_BASE["atacadao"]
    resposta_db = manager.carregar_db(db_path=db_path)
    dir_file = os.path.dirname(os.path.abspath(__file__))
    dir_file_save = os.path.join(dir_file, "product_img")

    # Cria diretório se não existir
    os.makedirs(dir_file_save, exist_ok=True)

    try:
        for link in resposta_db:
            imag_link = link[5]
            
            if imag_link is not None:
                filename = imag_link.split('/')[-1].split('?')[0] or f"image_{link[0]}.jpg"
                path_save = os.path.join(dir_file_save, filename)  
                # Requisição para a API do Shibata
                if os.path.exists(path_save):
                    print("imagem existente")
                    continue
                else:
                    response = fazer_requisicao(
                        url=imag_link, 
                        username=PROXY_USERNAME, 
                        password=PROXY_PASSWORD, 
                        headers=DEFAULT_HEADERS["atacadao"]
                        )
                    status_code = response.status_code
                    if  status_code == 403 or status_code == 404:
                        print("status code 403: forbidem ")
                        print("ou ")
                        print("status code 404: not found ")
                        continue

                    response.raise_for_status()  # Levanta uma exceção para erros HTTP

                    with open(path_save, 'wb') as arquivo:
                        for parte in response.iter_content(chunk_size=8192):
                            arquivo.write(parte)
                    print(f"Arquivo baixado com sucesso e salvo em: {path_save}")
                    continue
            print("Link None")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")


def routine_atacadao():
    #preparar_navegador_atacadao()
    #coleta_departamento()
    coleta_produtos(db_path=DB_PATH["atacadao"],mercado=MERCADOS["atacadao"])
    #query_de_atualizacao(db_path=DB_PATH["atacadao"])
    download_img(db_path=DB_PATH["atacadao"])



