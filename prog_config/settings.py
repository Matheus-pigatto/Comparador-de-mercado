# config/settings.py
import os
# -----------------------------
# URLs Gerais dos mercados
SITES = {
    "shibata" : "https://www.loja.shibata.com.br/",
    "atacadao" : "https://www.atacadao.com.br/",
    "carrefour" : "https://www.loja.shibata.com.br/",
    "pao_de_acucar" : "https://www.loja.shibata.com.br/",
    "piratininga" : "https://www.loja.shibata.com.br/",
    "tauste" : "https://www.loja.shibata.com.br/",
    "tenda" : "https://www.loja.shibata.com.br/"
}


#========================================================================================================
#                               CONFIGURAÇÕES GERAIS DO SHIBATA
#========================================================================================================


# -----------------------------
# URLs Gerais do Shibata
# -----------------------------
SHIBATA_HOME = SITES["shibata"]
SHIBATA_LOGIN_URL = f"{SHIBATA_HOME}/login"
SHIBATA_LOGOUT_URL = f"{SHIBATA_HOME}/logout"

# URL da API que retorna a árvore de departamentos
SHIBATA_API_DEPARTAMENTOS = (
    "https://services.se1.vipcommerce.com.br/api-admin/v1/org/{organizacao_id}/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/loja/classificacoes_mercadologicas/departamentos/arvore"
    
)


# URL base para produtos por departamento
SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO = (
    "https://services.se1.vipcommerce.com.br/api-admin/v1/org/{organizacao_id}/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/loja/classificacoes_mercadologicas/departamentos/{departamento}/produtos?page={pages}&secao={secao}"  
    
)


#URL base para detalhe dos produtos
SHIBATA_API_PRODUTOS = (
    "https://services.se1.vipcommerce.com.br/api-admin/v1/loja/produtos/{codigo_produto}/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/detalhes"
)

#URL base para carrinho
SHIBATA_API_CARRINHO =(
    "https://services.se1.vipcommerce.com.br/api-admin/v1/org/{organizacao_id}/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/loja/carrinhos"
)


# -----------------------------
# IDs Fixos (vindos da análise da API)
# -----------------------------
ORGANIZACAO_ID = 161
FILIAL_ID = 1
CENTRO_DISTRIBUICAO_ID = 13


# -----------------------------
# Caminhos do Projeto
# -----------------------------
# Caminho absoluto para o diretório atual (src/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para chegar na raiz do projeto (Comparador_de_mercados/)
project_root = os.path.dirname(current_dir)
# Caminho absoluto para a pasta 'db'
DB_FOLDER_PATH = os.path.join(project_root, "db")
# Dicionário com os caminhos absolutos para cada banco de dados
DB_PATH = {
    "shibata": os.path.join(DB_FOLDER_PATH, "shibata.db"),
    "carrefour": os.path.join(DB_FOLDER_PATH, "carrefour.db"),
    "atacadao": os.path.join(DB_FOLDER_PATH, "atacadao.db"),
    "coop": os.path.join(DB_FOLDER_PATH, "coop.db"),
    "pao de acucar": os.path.join(DB_FOLDER_PATH, "pao_de_acucar.db"),
    "piratininga" : os.path.join(DB_FOLDER_PATH, "piratininga.db"),
    "tauste": os.path.join(DB_FOLDER_PATH, "tauste.db"),
    "tenda": os.path.join(DB_FOLDER_PATH, "tenda.db")
}

IMAGE_BASE ={
    "shibata" : "https://produtos.vipcommerce.com.br/500x500/"
    #"atacadao":
}

DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
DATA_LISTS_DIR = "data/lists"
TOKEN_PATH = r"tokens/shibata_auth.jwt"
DOMAIN_KEY = "loja.shibata.com.br"


# -----------------------------
# Headers Padrão para Requests
# -----------------------------
DEFAULT_HEADERS = {
    "shibata" : {
    "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://www.loja.shibata.com.br/ ",
    "Origin": "https://www.loja.shibata.com.br ",
    "domainKey": "loja.shibata.com.br",
    "OrganizationID": "161"
    },
    "atacadao" :{
    "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://www.atacadao.com.br/",
    "Origin": "https://www.atacadao.com.br/ ",
    }
}

# -----------------------------
# ID dos Mercados
# -----------------------------
MERCADOS = {
    "shibata": 1,
    "carrefour": 2,
    "atacadao": 3,
    "coop": 4,
    "pao de acucar": 5,
    "piratininga" : 6,
    "tauste": 7,
    "tenda": 8
    }


# -----------------------------
# Outras Configurações
# -----------------------------
DELAY_ENTRE_REQUISICOES = 2  # segundos
MAX_TENTATIVAS = 3
TIMEOUT_PADRAO = 10  # segundos

#========================================================================================================
#                               CONFIGURAÇÕES GERAIS DO ATACADÃO
#========================================================================================================

# -----------------------------
# URLs Gerais do Atacadao
# -----------------------------
ATACADAO_HOME = SITES["shibata"]
ATACADAO_LOGIN_URL = f"https://secure.atacadao.com.br/api/io/login"
ATACADAO_LOGOUT_URL = f"{SHIBATA_HOME}/logout"

# URL da API que retorna a árvore de departamentos
ATACADAO_API_DEPARTAMENTOS = (
    "https://www.atacadao.com.br/_next/data/b7bf1OS-TDgHJQR5zpuxB/pt-BR.json"
)

# URL base para produtos por departamento
SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA1 = (
    "https://services.vipcommerce.com.br/api-admin/v1/loja/classificacoes_mercadologicas/secoes/{classificacao_mercadologica_id}/produtos/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/ativos"
    
)

# URL base para produtos por departamento
SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA_X = (
    "https://services.vipcommerce.com.br/api-admin/v1/loja/classificacoes_mercadologicas/secoes/{classificacao_mercadologica_id}/produtos/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/ativos?page={pages}"
    
)

#URL base para detalhe dos produtos
SHIBATA_API_PRODUTOS = (
    "https://services.vipcommerce.com.br/api-admin/v1/loja/produtos/{codigo_produto}/filial/{filial_id}/centro_distribuicao/{centro_distribuicao_id}/detalhes"
)