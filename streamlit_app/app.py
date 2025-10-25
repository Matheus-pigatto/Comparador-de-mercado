import streamlit as st
import pandas as pd
import sqlite3
from doctest import debug
import sys
import os



# Obtém o diretório do script atual (app.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para chegar ao diretório 'comparador_de_mercado'
project_root = os.path.dirname(current_dir)
#print(project_root)
# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(project_root)
# o caminho relativo correto é '../tokens/shibata_auth.jwt'
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "..", "tokens", "shibata_auth.jwt")
# ---------------------------------------------------------

st.set_page_config(
   page_title="Comparador",
   page_icon="🛒",
   layout="wide",
   initial_sidebar_state="expanded",
   
)


pg = st.navigation([
   
    st.Page("pages/01_home.py", title="Home", icon="🏠"),
    st.Page("pages/sobre_nos.py", title="Sobre", icon="ℹ️"),
    st.Page("pages/como_funciona.py", title="Como Funciona", icon="💡"),
    st.Page("pages/comparar_listas.py", title="Comparador", icon="📊"),
    st.Page("pages/historico_precos.py", title="Histórico de Preços", icon="📈"),
    st.Page("pages/contato.py", title="Contato", icon="✉️"),
])

pg.run()