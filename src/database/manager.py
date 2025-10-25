import sqlite3
import os
from prog_config.settings import DB_PATH, MERCADOS
from prog_config.settings_db import TABELAS_PERMITIDAS, COLUNAS_PERMITIDAS_DB
from typing import List, Dict, Any, Tuple

def salvar_departamento(db_path, departamento_data) -> None:
    
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO departamentos (
        classificacao_mercadologica_id, 
        nivel, 
        parent_id, 
        descricao, 
        imagem, 
        link, 
        total_ofertas, 
        data_coleta,
        mercado
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (
        departamento_data["classificacao_mercadologica_id"],
        departamento_data["nivel"],
        departamento_data["parent_id"],
        departamento_data["descricao"],
        departamento_data["imagem"],
        departamento_data["link"],
        departamento_data["total_ofertas"],
        departamento_data["data_coleta"],
        departamento_data["mercado"]
    )
    )

    conn.commit()
    conn.close()

def pesquisa_departamento(db_path:str) -> list:
    
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT (DISTINCT classificacao_mercadologica_id)
        FROM departamentos
    '''
    )
    resultados = cursor.fetchall()

    print(resultados)

    conn.commit()
    conn.close()

    return resultados

def  salvar_produto(db_path:str, produto_data:dict) -> None:
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (
                produto_id, 
                marca_id, 
                classificacao_mercadologica_id, 
                descricao,
                imagem,
                disponivel,
                preco,
                priorizado,
                quantidade_minima,
                quantidade_maxima,
                bebida_alcoolica,
                link,
                codigo_barras,
                sku,
                codigo_erp,
                quantidade_vendida,
                em_oferta,
                quantidade_unidade_diferente,
                exibe_preco_original,
                preco_original,
                unidade_sigla,
                possui_unidade_diferente,
                permitir_observacao_na_compra,
                habilitar_seletor_unidade_peso,
                observacao,
                unidade_fracao,
                marca,
                secao_id,
                busca_item,
                volume_principal,
                anunciado,
                posicao,
                urls_eventos_ads,
                id_2,
                data_coleta,
                mercado
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
                produto_data["produto_id"], 
                produto_data["marca_id"], 
                produto_data["classificacao_mercadologica_id"], 
                produto_data["descricao"],
                produto_data["imagem"],
                produto_data["disponivel"],
                produto_data["preco"],
                produto_data["priorizado"],
                produto_data["quantidade_minima"],
                produto_data["quantidade_maxima"],
                produto_data["bebida_alcoolica"],
                produto_data["link"],
                produto_data["codigo_barras"],
                produto_data["sku"],
                produto_data["codigo_erp"],
                produto_data["quantidade_vendida"],
                produto_data["em_oferta"],
                produto_data["quantidade_unidade_diferente"],
                produto_data["exibe_preco_original"],
                produto_data["preco_original"],
                produto_data["unidade_sigla"],
                produto_data["possui_unidade_diferente"],
                produto_data["permitir_observacao_na_compra"],
                produto_data["habilitar_seletor_unidade_peso"],
                produto_data["observacao"],
                produto_data["unidade_fracao"],
                produto_data["marca"],
                produto_data["secao_id"],
                produto_data["busca_item"],
                produto_data["volume_principal"],
                produto_data["anunciado"],
                produto_data["posicao"],
                produto_data["urls_eventos_ads"],
                produto_data["id_2"],
                produto_data["data_coleta"],
                produto_data["mercado"]
                
                ))
    conn.commit()
    conn.close()

def  salvar_preco_produto(db_path, preco_produto_data:dict) -> None:
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO preco (
                    produto_id,
                    preco_max,
                    preco_min,
                    preco_atual_low,
                    preco_atual_high,
                    quantidade_minima_low,
                    quantidade_maxima_high,
                    data_ultima_coleta,
                    dias_sem_atualizar
                 ) VALUES (?,?,?,?,?,?,?,?,?)
                   ''',(
                    preco_produto_data["produto_id"],
                    preco_produto_data["preco_max"],
                    preco_produto_data["preco_min"],
                    preco_produto_data["preco_atual_low"],
                    preco_produto_data["preco_atual_high"],
                    preco_produto_data["qnt_min_low"],
                    preco_produto_data["qnt_min_high"],
                    preco_produto_data["ultima_coleta"],
                    preco_produto_data["dias_sem_atualizar"],
                   ))
    conn.commit()
    conn.close()

def  atualizar_preco_produto(db_path:str, preco_produto_data: tuple) -> None:
    """ 
    Atualiza o preço de um produto
    """
    (product_id, 
    preco_max, 
    preco_min, 
    preco_atual_low, 
    preco_atual_high, 
    quantidade_minima_low, 
    quantidade_maxima_high, 
    data_ultima_coleta,  
    dias_sem_atualizar) = preco_produto_data
    
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
                    UPDATE preco 
                    SET 
                        preco_max = ?,
                        preco_min = ?,
                        preco_atual_low = ?,
                        preco_atual_high = ?,
                        quantidade_minima_low = ?,
                        quantidade_maxima_high = ?,
                        data_ultima_coleta = ?,
                        dias_sem_atualizar =?
                    
                    WHERE produto_id = ?
                   ''',( preco_max,
                                    preco_min,
                                    preco_atual_low,
                                    preco_atual_high,
                                    quantidade_minima_low,
                                    quantidade_maxima_high,
                                    data_ultima_coleta,
                                    dias_sem_atualizar,
                                    int(product_id))
                    )
    conn.commit()
    conn.close()

def  atualizar_preco_nao_atualizado(db_path:str, preco_produto_data: tuple) -> None:
    """
    Atualiza os dias sem atualização de um produto cujo o preço nao mudou
    """
    (product_id,dias_sem_atualizar) = preco_produto_data
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
                    UPDATE preco 
                    SET 
                        dias_sem_atualizar =?
                     
                    WHERE  produto_id = ?
                   ''',(
                       dias_sem_atualizar,
                       int(product_id))
                )
    conn.commit()
    conn.close()

def log_preco(db_path:str, preco_produto_data:tuple) -> None:
    """
    Insere o registro novo no log de preços 
    """

    #(product_id,preco_low,preco_high,quantidade_maxima_low,quantidade_maxima_high,data_coleta) = preco_produto_data
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
                    INSERT INTO log_precos ( 
                        produto_id,
                        preco_low,
                        preco_high,
                        quantidade_maxima_low,
                        quantidade_maxima_high,
                        data_coleta
                     
                   ) VALUES (?,?,?,?,?,?)''' ,(
                    preco_produto_data)
                )
    conn.commit()
    conn.close()

def pesquisa_ultimo_log(db_path:str, preco_produto_data:tuple) -> None:
    """
    pesquisa o ultimo log de um produto
    """
    produto_id = preco_produto_data[0]
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
                    SELECT*
                   FROM log_precos
                   WHERE produto_id = ?
                   ORDER BY data_coleta ASC
                     
                   ''', (produto_id,) 
                )
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultados

def pesquisa_log_preco(produto_id:str, db_path) -> None:
    """
    Pesquisa na tabela log_precos a existencia do ID para saber 
    se o produto ja foi cadastrado 
    """
    
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
                    SELECT produto_id
                    FROM log_precos
                    WHERE produto_id = ?
                        
                ''', (produto_id,))
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultados

def pesquisa_preco_produto(produto_id:str, mercado:int) -> list[tuple]:

    match mercado:
        case 1:
            conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                    ORDER BY data_ultima_coleta 
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados

        case 2:
            conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados

        case 3:
            conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''SELECT *
                    FROM preco 
                    WHERE produto_id= ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            print('produto encontrado')
            return resultados
        case 4:
            conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados
        case 5:
            conn = sqlite3.connect(database=DB_PATH["pao_de_acucar"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados
        case 6:
            conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados
        case 7:
            conn = sqlite3.connect(database=DB_PATH["tauste"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados
        case 8:
            conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT *  
                    FROM preco 
                    WHERE produto_id = ?
                ''', (produto_id,))
            resultados = cursor.fetchall()
            return resultados
        case _:
            print("Mercado não disponível, verifique erro")

def pesquisa_de_departamentos(db_path, mercado) -> list[tuple]:
        match mercado:

            case 1:
                conn = sqlite3.connect(database=db_path, check_same_thread=False)
                cursor = conn.cursor()

                cursor.execute('''
                               SELECT classificacao_mercadologica_id, parent_id, descricao
                               FROM departamentos 
                               WHERE parent_id IS NOT NULL
                               ''')
                resultados = cursor.fetchall()
                return resultados
            

            case 2:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute('''select descricao, link from departamentos where parent_id is null''')
                resultados = cursor.fetchall()
                
                return resultados


            case 3:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute('''select descricao, link from departamentos where parent_id is null''')
                resultados = cursor.fetchall()
                
                return resultados
            
            case _:
                print("Mercado não disponível, verifique erro")

def pesquisa_produto_db_por_multiplos_ids(lista_de_ids: set, mercado=int) -> list[tuple]:
    db_file_path = DB_PATH["shibata"]
    # --- ADICIONE ESTAS DUAS LINHAS PARA DEBUGAR ---
    print(f"DEBUG: Tentando abrir o banco de dados em: {db_file_path}")
    print(f"DEBUG: O arquivo existe no caminho especificado? {os.path.exists(db_file_path)}")
    # ----------------------------------------------

    if not lista_de_ids:
        return [] # Retorna lista vazia se não houver IDs para buscar

    # Converte o set de IDs para uma tupla para usar no SQL IN clause
    # Isso garante que a ordem não importa e é um formato aceito
    ids_tuple = tuple(lista_de_ids)
    
    # Gera uma string de placeholders '?, ?, ?' com base no número de IDs
    placeholders = ','.join(['?' for _ in ids_tuple])

    match mercado:
        case 1:
            conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id IN ({placeholders})  
                           ''', ids_tuple
                           )
            resultados = cursor.fetchall()
            return resultados

        case 2:
            conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados

        case 3:
            conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''  
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )

            resultados = cursor.fetchall()
            #print(resultados)
            return resultados
            
        case 4:
            conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 5:
            conn = sqlite3.connect(database=DB_PATH["pao de acucar"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 6:
            conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 7:
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 8:
            conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case _:
            print("Mercado não disponível, verifique erro")
       
def pesquisa_produto_db_por_id(produto_id: int, mercado=int) -> List[Tuple]:
    match mercado:
        case 1:
            conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id in produto_id = ? 
                           ''', (produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados

        case 2:
            conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados

        case 3:
            conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''  
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, imagem 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )

            resultados = cursor.fetchall()
            #print(resultados)
            return resultados
            
        case 4:
            conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 5:
            conn = sqlite3.connect(database=DB_PATH["pao de acucar"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 6:
            conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 7:
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 8:
            conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case _:
            print("Mercado não disponível, verifique erro")

def pesquisa_todos_produto_db_por_id(mercado=int, limit=int,offset=0) -> List[Tuple]:
    match mercado:
        case 1:
            conn = sqlite3.connect(database=DB_PATH["shibata"])
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id
                            LIMIT {limit} OFFSET {offset}  
                           '''
                           )
            resultados = cursor.fetchall()
            return resultados

        case 2:
            conn = sqlite3.connect(database=DB_PATH["carrefour"])
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados

        case 3:
            conn = sqlite3.connect(database=DB_PATH["atacadao"])
            cursor = conn.cursor()
            cursor.execute('''  
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )

            resultados = cursor.fetchall()
            #print(resultados)
            return resultados
            
        case 4:
            conn = sqlite3.connect(database=DB_PATH["coop"])
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 5:
            conn = sqlite3.connect(database=DB_PATH["pao de acucar"])
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 6:
            conn = sqlite3.connect(database=DB_PATH["piratininga"])
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 7:
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case 8:
            conn = sqlite3.connect(database=DB_PATH["tenda"])
            cursor = conn.cursor()
            cursor.execute('''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras 
                            FROM produtos 
                            WHERE produto_id = ? 
                            GROUP BY produto_id = ?
                           ''', (produto_id,produto_id,)
                           )
            resultados = cursor.fetchall()
            return resultados
        case _:
            print("Mercado não disponível, verifique erro")

def pesquisa_todos_produto_db_secao(
    mercado:int,
    tabela: str,
    colunas: List[str] = None,  # None = todas as colunas
    filtros: Dict[str, Any] = None,  # Filtros seguros
    order_by: str = None,
    limit: int = None,
    offset: int = None,
) -> List[Tuple]:

    """
    Função genérica segura para pesquisas no banco de dados.
    
    Args:
        db_path: Caminho para o banco de dados
        tabela: Nome da tabela
        colunas: Lista de colunas a retornar (None = todas)
        filtros: Dicionário de filtros {coluna: valor}
        order_by: Coluna para ordenação
        limit: Limite de resultados
    """

    # Validações de segurança
    if tabela not in TABELAS_PERMITIDAS:
        raise ValueError(f"Tabela '{tabela}' não permitida")
    
    # Valida colunas solicitadas
    if colunas is None:
        colunas_str = '*'
    else:
        COLUNAS_PERMITIDAS = [col for col in colunas if col in COLUNAS_PERMITIDAS_DB.get(tabela, set())]
        if not COLUNAS_PERMITIDAS:
            colunas_str = '*'
        else:
            colunas_str = ', '.join(COLUNAS_PERMITIDAS)
    
    # Constrói query segura com parâmetros
    query = f"SELECT {colunas_str} FROM {tabela}"
    params = []
    
    # Adiciona WHERE clause segura
    if filtros:
        where_conditions = []
        for coluna, valor in filtros.items():
            if coluna in COLUNAS_PERMITIDAS_DB.get(tabela, set()):
                where_conditions.append(f"{coluna} = ?")
                params.append(valor)
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
    
    # Adiciona ORDER BY e LIMIT
    if order_by and order_by in COLUNAS_PERMITIDAS_DB.get(tabela, set()):
        query += f" ORDER BY {order_by}"
    
    if limit and isinstance(limit, int) and limit > 0:
        query += f" LIMIT {limit}"

    try:
        match mercado:
            case 1:
                conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados

            case 2:
                conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados

            case 3:
                conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)

                resultados = cursor.fetchall()
                #print(resultados)
                return resultados
                
            case 4:
                conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            case 5:
                conn = sqlite3.connect(database=DB_PATH["pao de acucar"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            case 6:
                conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            case 7:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            case 8:
                conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            case _:
                print("Mercado não disponível, verifique erro")

    except Exception as e:
        print(f"Erro ao pesquisar dados: {e}")

def encontrar_produtos_indisponiveis(
    db_path: str,
    classificacao_mercadologica_id: int
) -> List[int]:
    """
    Encontra produtos de uma classificação específica que não tiveram 
    preço coletado hoje.

    Args:
        db_path: Caminho para o banco de dados
        classificacao_mercadologica_id: ID da classificação mercadológica

    Returns:
        Lista de produto_ids que precisam de coleta
    """

    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    try:
        
        query = """
            SELECT produtos.produto_id 
            FROM produtos
            WHERE produtos.classificacao_mercadologica_id = ?
              AND produtos.disponivel = 1  -- Apenas produtos disponíveis
              AND produtos.produto_id NOT IN (
                SELECT DISTINCT preco.produto_id 
                FROM preco
                WHERE DATE(preco.data_ultima_coleta) = DATE('now')
              )
        """
        
        cursor.execute(query, (classificacao_mercadologica_id,))
        resultados = cursor.fetchall()
        
        # Extrai apenas os IDs
        produto_ids = [row[0] for row in resultados]
        
        return produto_ids
        
    finally:
        conn.close()

def  atualizar_produtos_indisponiveis(db_path: str, lista_ids: List[int], novo_valor: int) -> None:
    """
    Atualiza a coluna 'disponivel' para múltiplos produtos por ID.
    
    Args:
        db_path: Caminho para o banco de dados
        lista_ids: Lista de IDs dos produtos a atualizar
        novo_valor: Novo valor para a coluna 'disponivel' (0 ou 1)
    """

    if not lista_ids:
        print("Lista de IDs vazia")
        return

    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()

    try:
        # Cria placeholders para os IDs (?)
        placeholders = ','.join('?' * len(lista_ids))
        
        query = f"""
            UPDATE produtos 
            SET disponivel = ?
            WHERE produto_id IN ({placeholders})
        """
        
        # Parâmetros: novo_valor + lista de IDs
        parametros = [novo_valor] + lista_ids
        
        cursor.execute(query, parametros)
        conn.commit()
        
        print(f"Atualizados {cursor.rowcount} produtos")
        
    except Exception as e:
        print(f"Erro na atualização: {e}")
        conn.rollback()
    finally:
        conn.close()

def pesquisa_total_dados_bd(mercado:int, coluna:str) -> list[tuple]:
    match mercado:
            case 1:
                conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados

            case 2:
                conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados

            case 3:
                conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )

                resultados = cursor.fetchall()
                #print(resultados)
                return resultados
                
            case 4:
                conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados
            case 5:
                conn = sqlite3.connect(database=DB_PATH["pao de acucar"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados
            case 6:
                conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados
            case 7:
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados
            case 8:
                conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f'''
                                SELECT COUNT({coluna})
                                FROM produtos 
                            '''
                            )
                resultados = cursor.fetchall()
                return resultados
            case _:
                print("Mercado não disponível, verifique erro")

def pesquisa_produto_db_por_multiplos_cod_barras(lista_de_cb=set, mercado=int) -> list[tuple]:
    # ----------------------------------------------

    if not lista_de_cb:
        return [] # Retorna lista vazia se não houver IDs para buscar

    # Converte o set de IDs para uma tupla para usar no SQL IN clause
    # Isso garante que a ordem não importa e é um formato aceito
    if isinstance(lista_de_cb, (set, list)):
        cb_tuple = tuple(lista_de_cb)
    elif isinstance(lista_de_cb, (int, str)):
        cb_tuple = (lista_de_cb,) # Garante que é uma tupla de um elemento
    else:
        # Se o tipo não for esperado, você pode levantar um erro ou lidar de outra forma
        raise TypeError("lista_de_cb deve ser uma lista, set, int ou str de códigos de barras.")
    #print(f" A tupla fornecida para pesquisa foi : {cb_tuple}")
    # Gera uma string de placeholders '?, ?, ?' com base no número de IDs
    placeholders = ','.join(['?' for _ in cb_tuple])
    
    match mercado:
        case 1:
            conn = sqlite3.connect(database=DB_PATH["shibata"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT id, produto_id, descricao, marca_id, codigo_barras, preco 
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados

        case 2:
            conn = sqlite3.connect(database=DB_PATH["carrefour"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados

        case 3:
            conn = sqlite3.connect(database=DB_PATH["atacadao"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''  
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )

            resultados = cursor.fetchall()
            print(resultados)
            return resultados
            
        case 4:
            conn = sqlite3.connect(database=DB_PATH["coop"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados
        case 5:
            conn = sqlite3.connect(database=DB_PATH["pao de acucar"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados
        case 6:
            conn = sqlite3.connect(database=DB_PATH["piratininga"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados
        case 7:
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados
        case 8:
            conn = sqlite3.connect(database=DB_PATH["tenda"], check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(f'''
                            SELECT 
                                id, produto_id, descricao, marca_id, codigo_barras, preco  
                            FROM produtos 
                            WHERE codigo_barras IN ({placeholders})  
                           ''', cb_tuple
                           )
            resultados = cursor.fetchall()
            return resultados
        case _:
            print("Mercado não disponível, verifique erro")
       
def  atualizar_link_imagem(db_path:str, preco_produto_data: tuple) -> None:
    """
    Atualiza o link da imagem de um produto
    """
    (product_id, imagem) = preco_produto_data
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
                    UPDATE produtos 
                    SET 
                        imagem =?
                     
                    WHERE  produto_id = ?
                   ''',(
                       imagem,
                       int(product_id))
                )
    conn.commit()
    conn.close()

def update_db(db_path, marca_id, codigo_barras, produto_id) -> None:
    conn = sqlite3.connect(database=db_path)
    cursor = conn.cursor()

    cursor.execute(f'''update produtos
                   set marca_id = {marca_id}, codigo_barras = {codigo_barras}
                   where produto_id = {produto_id} ''')
    conn.commit()
    conn.close()
    print("produto atualizado")

def carregar_db(db_path) -> list[tuple]:

    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''select* 
                   from produtos
                   ''')
    resultados = cursor.fetchall()
    return resultados

