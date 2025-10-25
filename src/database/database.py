import sqlite3
import os

def init_db(db_path) -> None:
    #estrutura do banco de dados
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS departamentos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classificacao_mercadologica_id TEXT,
                    nivel TEXT,
                    parent_id TEXT,
                    descricao TEXT,
                    imagem TEXT,
                    link TEXT,
                    total_ofertas INTEGER,
                    data_coleta DATETIME,
                    mercado INTEGER
                   )
                   
    ''')
    conn.commit()
    conn.close()
    
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS produtos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTERGER,
                    marca_id TEXT,
                    classificacao_mercadologica_id TEXT,
                    descricao TEXT,
                    imagem TEXT,
                    disponivel BOOLEAN,
                    preco FLOAT,
                    priorizado BOOLEAN,
                    quantidade_minima INTEGER,
                    quantidade_maxima INTEGER,
                    bebida_alcoolica BOOLEAN,
                    link TEXT,
                    codigo_barras INTEGER,
                    sku TEXT,
                    codigo_erp INTEGER,
                    quantidade_vendida INTEGER,
                    em_oferta BOOLEAN,
                    oferta TEXT,
                    quantidade_unidade_diferente FLOAT,
                    exibe_preco_original BOOLEAN,
                    preco_original FLOAT,
                    unidade_sigla TEXT,
                    possui_unidade_diferente BOOLEAN,
                    permitir_observacao_na_compra BOOLEAN,
                    habilitar_seletor_unidade_peso BOOLEAN,
                    observacao TEXT,           
                    unidade_fracao TEXT,
                    marca TEXT,   
                    secao_id INTEGER,
                    busca_item TEXT,         
                    volume_principal TEXT, 
                    anunciado BOOLEAN,          
                    posicao TEXT,
                    urls_eventos_ads TEXT,           
                    id_2 INTEGER,
                    data_coleta DATE DEFAULT CURRENT_DATE,
                    mercado INTEGER
                    )
            ''')
    conn.commit()
    conn.close()

    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS preco(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    preco_max FLOAT,
                    preco_min FLOAT,
                    preco_atual_low FLOAT,
                    preco_atual_high FLOAT,
                    quantidade_minima_low INTEGER,
                    quantidade_maxima_high INTEGER,
                    data_ultima_coleta DATE DEFAULT CURRENT_DATE,
                    dias_sem_atualizar INTEGER,
                   
                    FOREIGN KEY (produto_id) REFERENCES produto(produto_id)
                    )
            ''')
    conn.commit()
    conn.close()
    
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS log_precos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    preco_low FLOAT,
                    preco_high FLOAT,
                    quantidade_maxima_low INTEGER,
                    quantidade_maxima_high INTEGER,
                    data_coleta DATE DEFAULT CURRENT_DATE,
                   
                    FOREIGN KEY (produto_id) REFERENCES produto(produto_id)
                    )
            ''')
    conn.commit()
    conn.close()