from turtle import width
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from src.mercados.shibata.api_client import coleta_carrinho
from src.core.utils import obter_headers, carregar_token
from src.core.utils_streamlit import organizacao_pesquisa, comparar_carrinho, limpeza_texto, exibir_comparacao_com_imagens
from src.mercados.shibata.parser import Carrinho, Preco
from src.database.manager import pesquisa_produto_db_por_multiplos_cod_barras, pesquisa_produto_db_por_multiplos_ids, pesquisa_preco_produto
from prog_config.settings import MERCADOS,SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA1,                               SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA_X, SHIBATA_API_CARRINHO

st.title("Comparador")
st.divider()


st.sidebar.image(image=r"C:\Users\Matheus Pigatto\Pictures\carrinho_compra.JPG",width=100)
st.sidebar.markdown(body='# :memo: Menu')
st.sidebar.divider()
st.sidebar.page_link("pages/01_home.py", label="Home")
st.sidebar.page_link("pages/sobre_nos.py", label="Sobre")
st.sidebar.page_link("pages/como_funciona.py", label="Como Funciona")
st.sidebar.page_link("pages/comparar_listas.py", label= "Comparador")
st.sidebar.page_link("pages/contato.py", label= "Contato")

TOKEN_PATH = os.path.join("C:\\Users\\Matheus Pigatto\\Documents\\Projetos de programação\\Particular\\Comparador_de_mercados\\", "tokens", "shibata_auth.jwt")
path_load = "http://localhost:8000/src/mercados/shibata/product_img/" #verificar se o endereço esta correto na hora de carregar a imagem
path_load2 = "http://localhost:8000/src/mercados/shibata/product_img/"
col1, col2 = st.columns(2)


carrinho=[]
token = carregar_token(TOKEN_PATH)

carrinho_lista = coleta_carrinho(token)


for produto in carrinho_lista[1:]:
    #st.write(produto.descricao)
    carrinho.append(produto.to_dict())
carrinho_de_compras = pd.DataFrame(carrinho)
#print(pd.DataFrame(carrinho_de_compras["imagem"]))

carrinho_de_compras["imagem"] = path_load + carrinho_de_compras["imagem"]



# --- Configuração do AgGrid ---
gb = GridOptionsBuilder.from_dataframe(carrinho_de_compras)

# Habilita a seleção de linha única
gb.configure_selection('single', use_checkbox=False, groupSelectsChildren=True)

# Remove a checkbox do cabeçalho da coluna 'ID'
gb.configure_column("ID", headerCheckboxSelection=False)

# Adiciona um estilo para o cursor mudar ao passar o mouse sobre as linhas
# Isso dá um feedback visual de que a linha é clicável
gb.configure_grid_options(domLayout='normal', rowStyle={
    "cursor": "pointer"
})

gridOptions = gb.build()

lista_ids_produtos_carriho = carrinho_de_compras[["produto_id"]]
lista_ids_produtos_carriho = lista_ids_produtos_carriho["produto_id"]
lista_precos_prod_carrinho = [] 

for produto in lista_ids_produtos_carriho:
    lista_preco=pesquisa_preco_produto(produto, mercado=MERCADOS["shibata"])
    lista_precos_prod_carrinho.append(lista_preco)
#print(lista_precos_prod_carrinho)
col1.dataframe(carrinho_de_compras[["imagem","descricao","preco"]], 
             column_config={
                 "imagem": st.column_config.ImageColumn(width="small")
                 })
col1.write(f"Total gasto no carrinho: R${carrinho_lista[0]['sub_total']}")
lista_de_ids=[ x for x in carrinho_de_compras["produto_id"]]
result_pesquisa = pesquisa_produto_db_por_multiplos_ids(lista_de_ids=lista_de_ids, mercado=MERCADOS["shibata"])
lista_pesquisa_cod_barras = []
for produto in result_pesquisa:
    if len(str(produto[4])) != 0 and len(str(produto[4]))>5:
        lista_pesquisa_cod_barras.append(produto[4])
lista_pesquisa_cod_barras = set(lista_pesquisa_cod_barras)

result_pesquisa_cb = pesquisa_produto_db_por_multiplos_cod_barras(lista_de_cb=lista_pesquisa_cod_barras,mercado=MERCADOS["atacadao"])

carrinho_limpo = (carrinho_de_compras['descricao'].str.lower().str.replace('-', " ").str.strip()).tolist()

pesquisa_bd = comparar_carrinho(carrinho=carrinho_limpo, mercado=1)

#st.dataframe(pesquisa_bd[0])
#st.dataframe(pesquisa_bd[1])

exibir_comparacao_com_imagens(carrinho_de_compras, pesquisa_bd[1], path_load)
