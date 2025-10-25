from turtle import width
from typing import Any
from unittest import result
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from src.mercados.shibata.api_client import coleta_carrinho
from src.core.utils import obter_headers, carregar_token
from src.mercados.shibata.parser import Carrinho, Preco
from src.database.manager import carregar_db, pesquisa_produto_db_por_multiplos_cod_barras, pesquisa_produto_db_por_multiplos_ids, pesquisa_preco_produto
from prog_config.settings import DB_PATH, MERCADOS,SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA1,                               SHIBATA_API_PRODUTOS_POR_DEPARTAMENTO_PAGINA_X, SHIBATA_API_CARRINHO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def limpeza_texto(texto:str) -> str:
    return texto.lower().replace("-", " ").strip()

def organizacao_pesquisa(mercado:int) -> list[tuple[Any, str]]:
    match mercado:
        case 1:
            db_atacadao = carregar_db(DB_PATH["atacadao"])
            
            db_atacadao_limpos = [(p[1],limpeza_texto(p[4]),p[37]) for p in db_atacadao]
            result = db_atacadao_limpos
        case 3:
            db_shibata = carregar_db(DB_PATH["shibata"])
            db_shibata_limpos = [(p[1],limpeza_texto(p[4]),p[37]) for p in db_shibata] 
            result = db_shibata_limpos
    
    return result

def comparar_carrinho(carrinho, mercado=None):
    assert mercado != None, 'Faltou inserir mercado'

    todos_produtos_limpos = organizacao_pesquisa(mercado)
    lista_matrix = [ produto[1] for produto in todos_produtos_limpos]
    
    resultados_provavel = []
    resultados_similares = []
    # Vetorização com TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lista_matrix)
    
    for produto in carrinho:
        tfidf_item = vectorizer.transform([produto])
        # Comparação do primeiro produto (banco1) com todos os outros
        similaridades = cosine_similarity(tfidf_item, tfidf_matrix)

        indices_top_provavel = similaridades.argsort()[0][-1:][::-1]  # ordem decrescente
        indices_top_similares = similaridades.argsort()[0][-5:][::-1]  # ordem decrescente
        # Adicionar ao resultado final
        for idx in indices_top_provavel:
            produto_id, nome_produto, mercado = todos_produtos_limpos[idx]
            resultados_provavel.append({
                'item_lista': produto,
                'id_produto_bd': produto_id,
                'produto_similar': nome_produto,
                'mercado': mercado,
                'score': round(similaridades[0][idx], 4)
            })
        for idx in indices_top_similares:
            produto_id, nome_produto, mercado = todos_produtos_limpos[idx]
            resultados_similares.append({
                'item_lista': produto,
                'id_produto_bd': produto_id,
                'produto_similar': nome_produto,
                'mercado': mercado,
                'score': round(similaridades[0][idx], 4)
            })
         
    # Converter pra DataFrame para visualização ou exportação
   

    return resultados_provavel, resultados_similares

def exibir_comparacao_com_imagens(carrinho_df, resultados_similares, path_load) -> None:

    
    """
    Versão com imagens reais dos produtos
    """
    
    # CSS aprimorado
    st.markdown("""
        <style>
        .produto-container {
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        
        .produto-original {
            width: 200px;
            text-align: center;
            margin-right: 30px;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .carrossel-container {
            flex: 1;
        }
        
        .carrossel-header {
            margin-bottom: 15px;
        }
        
        .carrossel {
            display: flex;
            overflow-x: auto;
            gap: 15px;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 8px;
            background-color: white;
        }
        
        .produto-similar {
            min-width: 160px;
            text-align: center;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .produto-imagem {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .produto-nome {
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 5px;
            height: 40px;
            overflow: hidden;
        }
        
        .produto-preco {
            font-size: 14px;
            color: #e74c3c;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .produto-score {
            font-size: 11px;
            color: #7f8c8d;
            background-color: #ecf0f1;
            padding: 3px 8px;
            border-radius: 12px;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Agrupar resultados
    from collections import defaultdict
    resultados_agrupados = defaultdict(list)
    
    for resultado in resultados_similares:
        resultados_agrupados[resultado['item_lista']].append(resultado)
    
    # Criar um dicionário para mapear descrições para dados do carrinho
    carrinho_dict = {}
    for _, row in carrinho_df.iterrows():
        key = row['descricao'].lower().replace('-', " ").strip()
        carrinho_dict[key] = row
    
    # Exibir cada item
    for item_key, similares in resultados_agrupados.items():
        if item_key in carrinho_dict:
            print("for item data")
            item_data = carrinho_dict[item_key]
            print(item_data["imagem"])
            st.markdown(f"""
                <div class="produto-container">
                    <div class="produto-original">
                        <h4>Produto Original</h4>
                        <img src="{item_data['imagem']}" class="produto-imagem" alt="{item_data['descricao']}">
                        <div class="produto-nome">{item_data['descricao']}</div>
                        <div class="produto-preco">R$ {item_data['preco']}</div>
                    </div>
                    
                    <div class="carrossel-container">
                        <div class="carrossel-header">
                            <h4>5 Opções Mais Similares</h4>
                        </div>
                        <div class="carrossel">
            """, unsafe_allow_html=True)
            
            # Exibir os 5 produtos similares
            for similar in similares[:5]:
                print(similar)
                st.markdown(f"""
                    <div class="produto-similar">
                        <div style="width: 120px; height: 120px; background-color: #f8f9fa; 
                                    border-radius: 8px; margin: 0 auto; display: flex; 
                                    align-items: center; justify-content: center; margin-bottom: 10px;">
                            <img src="{similar['imagem']}" class="produto-imagem" alt="{similar['descricao']}">
                        </div>
                        <div class="produto-nome">{similar['produto_similar']}</div>
                        <div class="produto-preco">{similar['preco']}</div>
                        <div class="produto-score">Score: {similar['score']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# No final do seu código, substitua por:
# exibir_comparacao_com_imagens(carrinho_de_compras, pesquisa_bd[1], path_load)