"""Arquivo contendo as funções para rodar os scripts na pagina do Shibata

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import json
import time
import requests

from core.utils import salvar_token, carregar_token
from prog_config.settings import ATACADAO_HOME, SHIBATA_HOME
from prog_config.settings import TOKEN_PATH, DOMAIN_KEY

def login_atacadao() -> None:
    """
    Tenta fazer login na conta Atacadao Supermercados.
    Se já tiver token válido, reutiliza.
    Se não, abre navegador pra login manual e captura token.
    """
    print("Iniciando processo de login...")

        # Tentar carregar token existente
    token = carregar_token(caminho=TOKEN_PATH)
    
    if token:
        print("Token encontrado. Usando modo autenticado...")
        return token

    # Se não tem token, abre navegador pra login
    print("Nenhum token válido encontrado. Abrindo navegador para login...")

    #config para navegador brave
    chrome_options = Options()
    chrome_options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # Conecta ao navegador Brave já em execução
    driver_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\chromedriver-win64\\chromedriver.exe'
    service = Service(executable_path=driver_path)

    # Carregando webdriver para acessar a pagina
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(30)

    # Abre uma nova aba usando JavaScript
    driver.execute_script("window.open('');")

    # Muda para a nova aba
    driver.switch_to.window(driver.window_handles[-1])

    try:
        driver.get(ATACADAO_HOME)

        # Aguarda até estar logado (você pode ajustar isso conforme necessidade)
        input("Faça login no site. Após logar, pressione Enter...")

        # Capturar o token do localStorage após login
        #auth = driver.execute_script("return localStorage.getItem('vp.auth');")
        session_id = driver.execute_script("return localStorage.getItem('vp.sessao');")
        token = driver.execute_script("return localStorage.getItem('vp.token');")

        if session_id and token :
           #print("Auth JWT capturado: ", auth[:50] + "...")  # Mostra só parte do token
            print("Sessao: ", session_id)
            print("Auth JWT capturado: ", token[:50] + "...")  # Mostra só parte do token
            salvar_token(caminho=TOKEN_PATH, token=token, sessao=session_id)
            header = {"token" : token,
                      "sessao" : session_id

            }
            return header
        
        else:
            raise Exception("Não foi possível capturar o token após login.")

    finally:
        driver.quit()
               
def config_retirada(driver):
    def selecionar_loja(driver, termo_busca) -> None:
    # Procura de loja com no título informado

        for i, loja in enumerate(lojas_elements):
            try:
                title_element = loja.find_element(By.XPATH, ".//h6[contains(@class, 'alterar-loja--opcao-retirada__title')]")

                if title_element and termo_busca in title_element.text:
                    print(f"Loja {termo_busca} encontrada: {title_element.text}")

                    # Tenta encontrar o botão "Selecionar" ou "Selecionado" dentro dessa loja
                    select_button = loja.find_element(By.XPATH, ".//button[contains(., 'Selecionar') or contains(i/@class, 'fa-check')]")

                    # Se o botão estiver visível antes do clique
                    WebDriverWait(loja, 30).until(
                        EC.visibility_of(select_button)
                    )

                    # Rolar até o elemento (caso não esteja visível)
                    driver.execute_script("arguments[0].scrollIntoView(true);", select_button)

                    # Clica no botão
                    select_button.click()
                    print("Botão 'Selecionar' da loja SJC clicado com sucesso.")
                    return
                
            except Exception as e:
                print(f"Erro ao processar loja {i}: {e}")
                continue

    print("Configurando retirada...")

    # Clica no botão para abrir opções de local
    try:
        button_location = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-warning ng-star-inserted']"))
        )
        button_location.click()
    except Exception as e:
        print("Erro ao abrir localização:", e)
        return

    # Clica na aba de "Retirada"
    try:
        button_pickup = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(., 'Retirada')]]"))
        )
        button_pickup.click()
    except Exception as e:
        print("Erro ao selecionar aba 'Retirada':", e)
        return

    # Encontra todos os cards de lojas disponíveis
    try:
        lojas_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH,
                "//div[@class='card card-default alterar-loja--opcao-retirada ng-star-inserted']")
            )
        )
    except Exception as e:
        print("Não foi possível encontrar locais de retirada:", e)
        return
    
    selecionar_loja(driver, "SJC")
       

