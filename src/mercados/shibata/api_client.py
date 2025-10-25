#Imports gerais
from datetime import datetime
from collections import Counter
import math
import os
from unittest import result
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from functools import partial
import requests
import random
import time
from typing import List, Dict, Any

# Imports do selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Imports do shibata
from src.core.utils import obter_headers, carregar_token
from prog_config.settings import CENTRO_DISTRIBUICAO_ID, DB_PATH, FILIAL_ID, MERCADOS, ORGANIZACAO_ID, SHIBATA_HOME, SHIBATA_API_DEPARTAMENTOS
from prog_config.settings import TOKEN_PATH,SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO,                               SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA_X, SHIBATA_API_CARRINHO, IMAGE_BASE
from src.mercados.atacadao import api_client
from src.mercados.shibata.login import login_shibata, config_retirada
from src.mercados.shibata.parser import Departamento, Produto, Preco, Carrinho
from src.database.manager import pesquisa_de_departamentos, pesquisa_log_preco, pesquisa_preco_produto, pesquisa_produto_db_por_id, salvar_departamento, salvar_produto
from src.database.models import criar_tabela_departamentos, criar_tabela_log_preco, criar_tabela_preco, criar_tabela_produtos
from src.database import manager
from prog_config.proxy_manager import fazer_requisicao, PROXY_USERNAME, PROXY_PASSWORD
from src.core.utils import delay_inteligente

# Cria um lock global para operações críticas no SQLite
DB_LOCK = threading.Lock()

# Variável global para sinalizar a parada (se for a regra de negócio)
STOP_SCRAPING = False

def preparar_navegador_shibata() -> None:
    # Passo 1: config para navegador brave
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
    driver.get(url=SHIBATA_HOME)

    # ====================
    # Shibata
    # ====================
    
    # Fazer login e configurar o local de retirada da mercadoria
    login_shibata()
    #config_retirada(driver=driver)

    # Carregar token salvo
    header = carregar_token(caminho=TOKEN_PATH)

    #Carregar os headers com os tokens
    headers = obter_headers(market="shibata", token=header)


def coleta_departamento(db_path) -> None:
    # Carregar token salvo
    header = carregar_token(caminho=TOKEN_PATH)
    headers = obter_headers(market="shibata", token=header)

    url_departamentos = SHIBATA_API_DEPARTAMENTOS.format(
                        organizacao_id=ORGANIZACAO_ID,
                        filial_id=FILIAL_ID,
                        centro_distribuicao_id=CENTRO_DISTRIBUICAO_ID
                        )
    
    # Requisição para a API do Shibata
    response = fazer_requisicao(url=url_departamentos,username=PROXY_USERNAME,password=PROXY_PASSWORD,headers=headers)
    """
    ==============================================================
                        Iniciar o banco de dados
    ===============================================================
    """
    criar_tabela_departamentos(db_path=db_path)

    """
    ===============================================================
                        Inicio coleta no shibata
                                     &
                        Armazenamento de dados
    ===============================================================
    """
    # 1º: Verificando a resposta da API Shibata e coletar dados
    if response.status_code == 200:
        print("API retornou ok, Logado!")
        dados = response.json()["data"]
        
        # 2º: Parsear (tratar) os dados em objetos departamento
        departamentos = Departamento.parse_departamento(data=dados)
        
        #3º Pesquisar no banco de dados todos os departamentos cadastrados
        resultado_pesquisa_dep = pesquisa_de_departamentos(db_path=db_path, mercado=MERCADOS["shibata"])

        #4º Criar um set com os departamentos encontrados no site e um set com os departamentos do BD  
        lista_de_departamento_ids_api = set([departamento.classificacao_mercadologica_id for departamento in departamentos])
        lista_departamento_ids_bd  = set([int(t[0]) for t in resultado_pesquisa_dep])
        
        #5º Comparar os sets para verificar se há algum departamento a ser salvo
        ids_novos_para_salvar  = lista_de_departamento_ids_api.difference(lista_departamento_ids_bd)
        
        #6º Se tiver algum novo departamento o if ocorrerá
        if len(ids_novos_para_salvar) > 0:    
            # 7º: Salvar cada departamento no banco            
            for dept in departamentos:
                #8º corre toda a lista id mercadologicos para ver se é o item novo, se for ele será salvo
                if dept.classificacao_mercadologica_id in ids_novos_para_salvar:
                    salvar_departamento(db_path=db_path, departamento_data=dept.to_dict())
                    print(f"Departamento {dept.descricao}, salvo com sucesso")

        else: print(f"Todos os {len(departamentos)} departamentos estão cadastrados.")
    else:
        print("Erro ao acessar API:", response.status_code, response.text)


def coleta_produtos(db_path) -> None:
    mercado=MERCADOS["shibata"]

    # Carregar token salvo e header
    header = carregar_token(caminho=TOKEN_PATH)
    headers = obter_headers(market="shibata", token=header)

    #busca lista de departamento
    pesquisa_dept = manager.pesquisa_de_departamentos(db_path=db_path,mercado=mercado)

    if not pesquisa_dept:
        print("Nenhum departamento encontrado no banco.")
        return
    
    
    """
    ========================
    Iniciar o banco de dados
    ========================
    """
    criar_tabela_produtos(db_path=db_path)
    criar_tabela_preco(db_path=db_path)
    criar_tabela_log_preco(db_path=db_path)
    """
    ========================
    Inicio coleta no shibata
    &
    Armazenamento de dados
    ========================
    """


    for n in pesquisa_dept:
        departamento = n[1]
        class_mercadologica_id = int(n[0])
        print("departamento: ", n[2], ". Sua class_merc é:", n[0])
        delay_inteligente()
        page = 1
        total_pages = 1

        while page <= total_pages:
            url = SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO.format(
                                filial_id = FILIAL_ID,
                                centro_distribuicao_id = CENTRO_DISTRIBUICAO_ID,
                                organizacao_id = ORGANIZACAO_ID,
                                secao = class_mercadologica_id,
                                departamento = departamento,
                                pages = page
                                )
                        
            # Requisição para a API do Shibata

            response = fazer_requisicao(url=url,username=PROXY_USERNAME,password=PROXY_PASSWORD,headers=headers)

            # 1o: Verificando a resposta da API Shibata e coletar dados
            if response.status_code == 200:
                print("API acessada!")
                dados = response.json()["data"]
                paginator = response.json()["paginator"]


                # 2o: Parsear (tratar) os dados em objetos departamento
                produtos = Produto.parse_produto(data=dados)
                produtos_na_pagina_api = set([produto.produto_id for produto in produtos])
                
                #comentar mais tarde
                
                ids_novos_para_salvar=comparar_id_pag_com_bd(
                    produtos_na_pagina_api=produtos_na_pagina_api,
                    mercado=mercado
                )
                
                
                for produto in produtos:
                                                         
                    resultado_pesquisa_preco = pesquisa_preco_produto(produto_id=produto.produto_id, mercado=mercado)
                    resultado_pesquisa_log_preco = pesquisa_log_preco(produto_id=produto.produto_id, db_path=db_path)
                    preco = Preco.parse_preco_from_produtos(produtos_data=produto)                            
                    if produto.produto_id in ids_novos_para_salvar:
                            
                            
                            resultado_pesquisa_log_preco = pesquisa_log_preco(produto_id=produto.produto_id, db_path=db_path)

                            if len(resultado_pesquisa_log_preco) == 0:
                                print(f"Cadastrando: {produto.descricao} no sistema.")
                                Preco.inserir_log_precos(preco=preco,db_path=db_path)
                                Preco.inserir_preco_produto(preco=preco,db_path=db_path)
                                salvar_produto(db_path=db_path, produto_data=produto.to_dict())
                                print(f"Cadastro completo do novo produto: {produto.descricao}. Salvo com sucesso.")
                            
                            elif len(resultado_pesquisa_preco) == 0:
                                print(f"Log de preço do produto: {produto.descricao} cadastrado mas preço ainda não cadastrado no sistema")
                                try:
                                    Preco.inserir_preco_produto(preco=preco,db_path=db_path)
                                    salvar_produto(db_path=db_path, produto_data=produto.to_dict())
                                    print(f"Cadastro completo do novo produto: {produto.descricao}. Salvo com sucesso.")
                                except Exception as e:
                                    print(f"Erro ao cadastrar produto: {produto.descricao}. Erro: {e}")

                            else:
                                print("Erro identificado")
                            
                    else:
                        if produto.disponivel == 1:
                            if len(resultado_pesquisa_preco) == 0:
                                print(f"Log de preço do produto: {produto.descricao} cadastrado mas preço ainda não cadastrado no sistema")
                                try:
                                    Preco.inserir_preco_produto(preco=preco,db_path=db_path)
                                    salvar_produto(db_path=db_path, produto_data=produto.to_dict())
                                    print(f"Cadastro completo do novo produto: {produto.descricao}. Salvo com sucesso.")
                                except Exception as e:
                                    print(f"Erro ao cadastrar produto: {produto.descricao}. Erro: {e}")
                            pesquisa_produto = manager.pesquisa_todos_produto_db_secao(mercado=mercado, tabela="produtos",colunas=["id","produto_id", "disponivel"],filtros={"produto_id": produto.produto_id})
                            if pesquisa_produto[0][2] == 0:
                                Produto.atualizar_disponibilidade_produto(db_path=db_path, classificacao_mercadologica_id=produto.classificacao_mercadologica_id, id_produto=produto.produto_id, disponivel=1)
                            resultado_comparacao_de_preco = Preco.compara_mudanca_preco(preco=preco, ultimo_preco=resultado_pesquisa_preco )
                            if resultado_comparacao_de_preco["mudou"] == True:
                                Preco.atualizar_novo_preco(preco=preco, ultimo_preco=resultado_pesquisa_preco)
                                Preco.inserir_log_precos(preco=preco,db_path=db_path)
                                print(f"Preço do produto: {produto.descricao} mudou! percentual {resultado_comparacao_de_preco["percentual"]}% ")
                            else:
                                
                                Preco.atualizar_preco_nao_atualizado(preco=preco, ultimo_preco=resultado_pesquisa_preco)
                                Preco.inserir_log_precos(preco=preco,db_path=db_path)
                                #print(f"Preço do produto: {produto.descricao} não mudou")

                        else:
                            print(f"produto {produto.descricao} não disponível valor = {produto.disponivel}...")
                            print("encerrando a sessão")
                            page = total_pages
                            classificacao_mercadologica_id = produto.classificacao_mercadologica_id
                            Produto.atualizar_disponibilidade_produto(
                                db_path=db_path,
                                classificacao_mercadologica_id=classificacao_mercadologica_id,
                                disponivel=0
                            )
                            # Uso:
                            produtos_indisponiveis = manager.encontrar_produtos_indisponiveis(
                                db_path=db_path,
                                classificacao_mercadologica_id=produto.classificacao_mercadologica_id
                            )

                            print(f"Foram encontrados {len(produtos_indisponiveis)} produtos indisponiveis")
                            print(f"IDs: {produtos_indisponiveis}")
                            if len(produtos_indisponiveis) == 0:
                                break
                            manager.atualizar_produtos_indisponiveis(db_path=db_path, lista_ids=produtos_indisponiveis, novo_valor=0)

                            print("colocando os itens de data passada não atualizados para indisponíveis")

                            
                if page == paginator["total_pages"]:
                    break
                print(f'Pagina {page} terminou de um total de {paginator["total_pages"]} paginas')   

                page = paginator["page"] + 1
                total_pages = paginator["total_pages"]
                delay_inteligente()

            else:
                print("Erro ao acessar API:", response.status_code, response.text)
                break


def processar_departamento(departamento_info, db_path, headers, mercado):
        
    """
    Processa um departamento específico (todos os produtos dele) em uma thread.
    
    Args:
        departamento_info: Tupla com informações do departamento (id, nome, descrição)
        db_path: Caminho do banco de dados
        headers: Headers para requisições API
        mercado: Identificador do mercado
    """
    global STOP_SCRAPING # Acessa a flag global
    thread_name = threading.current_thread().name
    departamento_nome = departamento_info[1]
    class_mercadologica_id = int(departamento_info[0])
    
    print(f"[{thread_name}] Iniciando departamento: {departamento_nome} (ID: {class_mercadologica_id})")

    try:
        page = 1
        total_pages = 1
        departamento_concluido = False

        while page <= total_pages and not departamento_concluido and not STOP_SCRAPING:
            if STOP_SCRAPING:
                print(f"[{thread_name}] STOP_SCRAPING ativada. Parando depto {departamento_nome}.")
                break
            
            url = SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO.format(
                filial_id=FILIAL_ID,
                centro_distribuicao_id=CENTRO_DISTRIBUICAO_ID,
                organizacao_id=ORGANIZACAO_ID,
                secao=class_mercadologica_id,
                departamento=departamento_nome,
                pages=page
            )

            # Criar cópia dos headers para evitar problemas de thread safety
            request_headers = headers.copy()
            
            # Fazer requisição com proxy
            response = fazer_requisicao(
                url=url, 
                username=PROXY_USERNAME, 
                password=PROXY_PASSWORD, 
                headers=request_headers
            )
            
            if response.status_code == 200:
                dados = response.json()["data"]
                paginator = response.json()["paginator"]
                total_pages = paginator["total_pages"]

                produtos = Produto.parse_produto(data=dados)
                produtos_na_pagina_api = {produto.produto_id for produto in produtos}
                
                # Comparar com BD
                ids_novos_para_salvar = comparar_id_pag_com_bd(
                    produtos_na_pagina_api=produtos_na_pagina_api, 
                    mercado=mercado
                )

                departamento_concluido = processar_produtos_pagina(
                    produtos, 
                    ids_novos_para_salvar, 
                    db_path, 
                    mercado,
                    thread_name
                )

    except Exception as e:
        print(f"[{thread_name}] Erro ao processar departamento {departamento_nome}: {e}")

def comparar_id_pag_com_bd(produtos_na_pagina_api, mercado):
    """ 
    Otimização: busca todos os IDs de uma vez, não página por página
    """
    # Obter todos os IDs existentes no banco
    with DB_LOCK:
        todos_produtos = manager.pesquisa_todos_produto_db_por_id(
            mercado=mercado, 
            limit=None,  # Busca todos de uma vez
            offset=0
        )
    
    ids_produtos_existentes_no_bd = set([x[1] for x in todos_produtos])
    return produtos_na_pagina_api.difference(ids_produtos_existentes_no_bd)


def coleta_carrinho(token=None):
    print("")
    print("coleta_carrinho")
    mercado=MERCADOS["shibata"]
    carrinho = []
    #3print((TOKEN_PATH))
    if token == None:
        header = carregar_token(caminho=TOKEN_PATH)
        headers = obter_headers(market="shibata", token=header)
    else:
        headers = obter_headers(market="shibata", token=token)
    #print("header:")
    #print(headers)
    #print(f"[DEBUG] Carrinho inicializado como: {carrinho}")
    

    #Carregar os headers com os tokens
    

    url = SHIBATA_API_CARRINHO.format(
                        organizacao_id = ORGANIZACAO_ID,
                        filial_id=FILIAL_ID,
                        centro_distribuicao_id=CENTRO_DISTRIBUICAO_ID
                        )
    #print(f"[DEBUG] URL da requisição: {url}")
    # Requisição para a API do Shibata
    #response = requests.get(url = url, headers = headers)
    response = fazer_requisicao(url=url,username=PROXY_USERNAME,password=PROXY_PASSWORD,headers=headers)
    #print(f"[DEBUG] Status Code da requisição: {response.status_code}")

    if response.status_code == 200:
                print("API acessada!")
                dados = response.json()["data"]
                carrinho = Carrinho.parse_carrinho(data=dados)
                #print(f"[DEBUG] Carrinho após parse: {carrinho}")
                #for produto in carrinho[1]:
                #    print(produto.produto_id)

    else:
        print(f"[DEBUG] Requisição falhou com status code: {response.status_code}")
        print(f"[DEBUG] Conteúdo da resposta: {response.text}")

    #print(f"[DEBUG] Valor final de carrinho antes do return: {carrinho}")
    return carrinho


def download_img(db_path):
    # Carregar token salvo
    header = carregar_token(caminho=TOKEN_PATH)

    #Carregar os headers com os tokens
    headers = obter_headers(market="shibata", token=header)

    url_base = IMAGE_BASE["shibata"]
    resposta_db = manager.carregar_db(db_path=db_path)
    dir_file = os.path.dirname(os.path.abspath(__file__))
    dir_file_save = dir_file + r"\product_img"

    try:
        for link in resposta_db:
            imag_link = link[5]
            
            if link[5] is not None:
                url_complete = url_base + imag_link
                path_save = dir_file_save + rf"\{link[5]}"  
                # Requisição para a API do Shibata
                if os.path.exists(path_save):
                    print("imagem existente")
                    continue
                else:
                    #response = requests.get(url = url_complete, headers = headers)
                    response = fazer_requisicao(url=url_complete,username=PROXY_USERNAME,password=PROXY_PASSWORD,headers=headers)
                    status_code = response.status_code
                    if  status_code == 403:
                        print("status code 403: forbidem ")
                        continue
                    response.raise_for_status()  # Levanta uma exceção para erros HTTP
                    with open(os.path.abspath(path_save), 'wb') as arquivo:
                        for parte in response.iter_content(chunk_size=8192):
                            arquivo.write(parte)
                    print(f"Arquivo baixado com sucesso e salvo em: {path_save}")
                    continue
            print("Link None")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")


def routine_shibata():
    #preparar_navegador_shibata()
    #coleta_carrinho()
    coleta_departamento(db_path=DB_PATH["shibata"])
    #download_img(db_path=DB_PATH["shibata"])
    coleta_produtos(db_path=DB_PATH["shibata"])

