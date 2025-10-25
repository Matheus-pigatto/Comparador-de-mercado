import os
import json
import random
import time
from prog_config.settings import DEFAULT_HEADERS
from src.mercados import shibata

def salvar_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def carregar_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def salvar_token(caminho, token, sessao):
    """Salva o token em arquivo"""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w') as f:
        json.dump(obj={"token": token, 
                       "sessao-id": sessao}, fp=f, indent=4)

def carregar_token(caminho):
    """Carrega o token salvo, se existir"""
    dict_header = {}
    if not os.path.exists(caminho):
        return None
    
    with open(caminho, "r") as f:
        data = json.load(f)

    # Remove as aspas extras e escapes
    token_limpo = data.get("token", "").strip('"').replace('\\"', '"')
    session_limpo = data.get("sessao-id", "").strip('"').replace('\\"', '"')
    return token_limpo, session_limpo

def obter_headers(market, token=None):
    headers = DEFAULT_HEADERS[market].copy()
    if token:
        headers["Authorization"] = f"Bearer {token[0]}"
        headers["sessao-id"] = token[1]
    return headers 

def delay_inteligente():
    """Delay que simula comportamento humano"""
    # Maioria das pessoas faz pausas de 2-10 segundos entre ações
    delay = random.uniform(2, 6)
    
    # Ocasionalmente, pausas maiores (como um humano pensando)
    if random.random() < 0.1:  # 10% das vezes
        delay += random.uniform(10, 30)  # Pausa maior
    
    time.sleep(delay)

