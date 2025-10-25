from asyncio.windows_events import NULL
#from curses import raw
import json
from datetime import datetime, timedelta
from prog_config.settings import MERCADOS, DB_PATH
from src.database import manager
from src.database.manager import pesquisa_produto_db_por_id, update_db, pesquisa_todos_produto_db_por_id, salvar_produto, pesquisa_preco_produto, atualizar_preco_produto
from src.mercados.atacadao.utils import query_pesquisa
from src.mercados import atacadao
import time



class Departamento:

    def __init__(self, raw_data) -> None:
        """
        raw_data é o json de dados dos departamentos recebido pela API
        """

        #campos extraidos
        self.classificacao_mercadologica_id = raw_data.get("classificacao_mercadologica_id")
        self.nivel = raw_data.get("nivel")
        self.parent_id = raw_data.get("parent_id")
        self.descricao = raw_data.get("descricao")
        self.imagem = raw_data.get("imagem")
        self.link = raw_data.get("link")
        self.total_ofertas = raw_data.get("total_ofertas")
        self.children = raw_data.get("children")
        self.data_coleta = datetime.now().date() #Data da coleta
        self.mercado = raw_data.get("mercado")

    def to_dict(self):# -> dict[str, Any]:
        """ Retorna os dados como dicionário para uso em DataFrame ou JSON"""
        return {
            "classificacao_mercadologica_id": self.classificacao_mercadologica_id,
            "nivel": self.nivel,
            "parent_id": self.parent_id,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "link": self.link,
            "total_ofertas": self.total_ofertas,
            "data_coleta": self.data_coleta,
            "mercado": self.mercado
        }
    
    def salvar(self, database_manager) -> None:
        """Salva o departamento no banco via manager"""
        database_manager.salvar_departamento(self.to_dict())

    def parse_departamento(data, nivel = "departamento", parent_id = None , id_counter = None):
        """
        Extrai e retorna uma lista de objetos Departamentos
        """
        departamentos = []

        if id_counter is None:
            id_counter = {"id": 1}
        
        for dept in data:
            if dept:
                current_id = id_counter["id"]
                departamento = {
                    "classificacao_mercadologica_id": current_id,
                    "nivel": nivel,
                    "parent_id": parent_id,
                    "descricao": dept["name"],
                    "link": dept["href"],
                    "children": dept.get("subCategories") or [],
                    "mercado" : MERCADOS.get("atacadao")
                }

                departamentos.append(Departamento(raw_data=departamento))

                id_counter["id"] += 1

                # Recursão para subcategorias
                if "subCategories" in dept and dept["subCategories"]:
                    children = dept["subCategories"]
                    child_nivel = "seção" if nivel == "departamento" else "subseção"
                    departamentos.extend(
                        Departamento.parse_departamento(children, nivel=child_nivel, parent_id=current_id, id_counter=id_counter)
                    )
            else:
                print(f"O id: {current_id} não possui item, está vazio")
                continue

        return departamentos

    

class Produto:
    def __init__(self, raw_data) -> None:
        """
        raw_data é o json de dados dos produtos recebido pela API
        """

        #campos extraidos
        self.produto_id = raw_data.get("produto_id")
        self.marca_id = raw_data.get("marca_id")
        self.classificacao_mercadologica_id = raw_data.get("classificacao_mercadologica_id")
        self.descricao = raw_data.get("descricao")
        self.imagem = raw_data.get("imagem")
        self.disponivel = raw_data.get("disponivel")
        self.preco = raw_data.get("preco")
        self.priorizado = raw_data.get("priorizado")
        self.quantidade_minima = raw_data.get("quantidade_minima")
        self.quantidade_maxima = raw_data.get("quantidade_maxima")
        self.bebida_alcoolica = raw_data.get("bebida_alcoolica")
        self.link = raw_data.get("link")
        self.codigo_barras=raw_data.get("codigo_barras")
        self.sku = raw_data.get("sku")
        self.codigo_erp = raw_data.get("codigo_erp")
        self.quantidade_vendida = raw_data.get("quantidade_vendida")
        self.em_oferta = raw_data.get("em_oferta")
        self.quantidade_unidade_diferente = raw_data.get("quantidade_unidade_diferente")
        self.exibe_preco_original = raw_data.get("exibe_preco_original")
        self.preco_original = raw_data.get("preco_original")
        self.unidade_sigla = raw_data.get("unidade_sigla")
        self.possui_unidade_diferente = raw_data.get("possui_unidade_diferente")
        self.permitir_observacao_na_compra = raw_data.get("permitir_observacao_na_compra")
        self.habilitar_seletor_unidade_peso = raw_data.get("habilitar_seletor_unidade_peso")
        self.observacao = raw_data.get("observacao")
        self.unidade_fracao = raw_data.get("unidade_fracao")
        self.marca = raw_data.get("marca")
        self.secao_id = raw_data.get("secao_id")
        self.busca_item = raw_data.get("busca_item")
        self.volume_principal = raw_data.get("volume_principal")
        self.anunciado = raw_data.get("anunciado")
        self.posicao = raw_data.get("posicao")
        self.urls_eventos_ads = raw_data.get("urls_eventos_ads")
        self.id_2 = raw_data.get("id")
        self.data_coleta = raw_data.get("data_coleta")#Data da coleta
        self.mercado = raw_data.get("mercado")
        
    def to_dict(self):# -> dict[str, Any]:

        """ Retorna os dados como dicionário para uso em DataFrame ou JSON"""

        return {
            "produto_id" : self.produto_id,
            "marca_id":self.marca_id,
            "classificacao_mercadologica_id":self.classificacao_mercadologica_id,
            "descricao":self.descricao,
            "imagem":self.imagem,
            "disponivel":self.disponivel,
            "preco":self.preco,
            "priorizado":self.priorizado,
            "quantidade_minima":self.quantidade_minima,
            "quantidade_maxima":self.quantidade_maxima,
            "bebida_alcoolica":self.bebida_alcoolica,
            "link":self.link,
            "codigo_barras":self.codigo_barras,
            "sku":self.sku,
            "codigo_erp":self.codigo_erp,
            "quantidade_vendida":self.quantidade_vendida,
            "em_oferta":self.em_oferta,
            "quantidade_unidade_diferente":self.quantidade_unidade_diferente,
            "exibe_preco_original":self.exibe_preco_original,
            "preco_original":self.preco_original,
            "unidade_sigla":self.unidade_sigla,
            "possui_unidade_diferente":self.possui_unidade_diferente,
            "permitir_observacao_na_compra":self.permitir_observacao_na_compra,
            "habilitar_seletor_unidade_peso":self.habilitar_seletor_unidade_peso,
            "observacao":self.observacao,
            "unidade_fracao": json.dumps(self.unidade_fracao) if isinstance(self.unidade_fracao, dict) else self.unidade_fracao,
            "marca":self.marca,
            "secao_id":self.secao_id,
            "busca_item":self.busca_item,
            "volume_principal":self.volume_principal,
            "anunciado":self.anunciado,
            "posicao":self.posicao ,
            "urls_eventos_ads":self.urls_eventos_ads,
            "id_2":self.id_2,
            "data_coleta":self.data_coleta,
            "mercado":self.mercado,
        }
                    
    def parse_produto(data):
        """
        Extrai e retorna uma lista de objetos produtos
        """
        produtos=[]
        lista_bebida_al = ["Champanhes, espumantes e sidras", "Coquetéis", "Destilados", "Cervejas", "Vinhos", "Whiskies"]

        for produto_raw in data:
            alcoolica = False

            t_ini_2 = datetime.now()

            #verifica se existem preços no produto
            if isinstance(produto_raw.get("node",{}).get("offers"), dict) and "offers" in produto_raw["node"]["offers"]:
                offer = produto_raw["node"]["offers"]["offers"][0]
            else:
                offer = {}

            #verifica se existe image url e pega o link                
            if produto_raw.get("node", {}).get("image"):
                image_url = produto_raw["node"]["image"][0]["url"]

            #verifica se a variavel offer esta completa com as offerta de varejo e atacado
            try:
                if isinstance(produto_raw.get("node").get("offers").get("offers")[1], dict):
                    qnt_min = produto_raw.get("node").get("offers").get("offers")[1].get("minQuantity")
            except IndexError:
                qnt_min = None

            #Ajuste da variavel de bebida alcoolica que não existe no json
            bebida_al = produto_raw["node"]["breadcrumbList"]["itemListElement"][1]["name"]
            if bebida_al in lista_bebida_al:
                alcoolica = True        
            
            produto ={
                "produto_id": produto_raw.get("node",{}).get("id"),
                "descricao": produto_raw.get("node",{}).get("name"),
                "imagem": image_url,
                "disponivel": 1,
                "preco": offer.get("listPrice"),
                "quantidade_minima" : offer.get("minQuantity"),
                "quantidade_maxima": qnt_min,
                "bebida_alcoolica": alcoolica,
                "link" : produto_raw.get("node").get("breadcrumbList").get("itemListElement")[-1].get("item"),
                "sku": produto_raw.get("node",{}).get("sku",{}),
                "unidade_sigla": produto_raw.get("node",{}).get("measurementUnit"),
                "marca": produto_raw.get("node",{}).get("brand",{}).get("brandName",{}),
                "data_coleta": datetime.now().date(), 
                "mercado" : MERCADOS.get("atacadao")
            }
            
            produto = Produto(raw_data=produto)
            produtos.append(produto)
        return produtos                

    def cadastro_cod_barras() -> None:
        resultado_query_shibata =manager.carregar_db(db_path=DB_PATH["shibata"])
        contador = 0
        for produto in resultado_query_shibata:
            contador += 1
            print(contador)
            try:
                print(produto)

                #TODO - Melhorar a pesquisa, fazer cruzamneto de DF para ser mais rapido e não ficar atualizando produtos sem necessidade

                marca_id, codigo_barra = produto[1], produto[13]
                
                resultado_pesquisa_db_atacadao = manager.pesquisa_produto_db_por_multiplos_cod_barras(lista_de_cb=codigo_barra, mercado=MERCADOS["atacadao"])
                print(resultado_pesquisa_db_atacadao)
                if len(resultado_pesquisa_db_atacadao)<1:
                    resultado_pesquisa = query_pesquisa(cod_barra=codigo_barra)
                    time.sleep(0.3)
                    if resultado_pesquisa["data"]["search"]["products"]["pageInfo"]["totalCount"] == 0:
                        print("produto não encontrado")
                        continue
                    else:
                        produto_raw = resultado_pesquisa["data"]["search"]["suggestions"]["products"][0]
                        produto_id = int(produto_raw.get("id"))
                        pesquisa_db_atacadao = pesquisa_produto_db_por_id(produto_id=produto_id, mercado=MERCADOS["atacadao"])
                        print(pesquisa_db_atacadao)
                        if len(pesquisa_db_atacadao) != 0:
                            produto ={
                                "produto_id": produto_id,
                                "descricao": produto_raw.get("name"),
                                "codigo_barra": codigo_barra,
                                "marca_id":marca_id
                            }
                            update_db(db_path=DB_PATH["atacadao"],marca_id=produto["marca_id"],codigo_barras=produto["codigo_barra"], produto_id=produto["produto_id"])
                        else:
                            bebida_al = produto_raw["breadcrumbList"]["itemListElement"][1]["name"]
                            lista_bebida_al = ["Champanhes, espumantes e sidras", "Coquetéis", "Destilados", "Cervejas", "Vinhos", "Whiskies"]
                            alcoolica = False
                            if bebida_al in lista_bebida_al:
                                alcoolica = True
                            data_iso = datetime.today()
                            
                            if len(produto_raw.get("offers").get("offers")) == 2:
                                quantidade_max = str(produto_raw.get("offers").get("offers")[1].get("minQuantity"))
                            else: 
                                quantidade_max = None
                            print(f"Quantidade de links: {len(produto_raw.get("breadcrumbList").get("itemListElement"))}")
                            if len(produto_raw.get("breadcrumbList").get("itemListElement")) != 4:
                                link = produto_raw.get("breadcrumbList").get("itemListElement")[2].get("item")
                            else:
                                link = produto_raw.get("breadcrumbList").get("itemListElement")[3].get("item")
                            produto_raw = {
                                "produto_id": produto_id,
                                "descricao": produto_raw.get("name"),
                                "imagem": produto_raw.get("image")[0].get("url"),
                                "disponivel": 1,
                                "preco": produto_raw.get("highPrice"),
                                "quantidade_minima" : produto_raw.get("offers").get("offers")[0].get("minQuantity"),
                                "quantidade_maxima": quantidade_max,
                                "codigo_barra" : codigo_barra,
                                "bebida_alcoolica": alcoolica,
                                "link" : link,
                                "sku": produto_raw.get("sku",{}),
                                "unidade_sigla": produto_raw.get("measurementUnit"),
                                "marca": produto_raw.get("brand",{}).get("brandName",{}),
                                "data_coleta": datetime.now().date(), 
                                "mercado" : MERCADOS.get("atacadao")
                            }
                            print(produto_raw)
                            produto_raw = Produto(raw_data=produto_raw)
                            salvar_produto(db_path=DB_PATH["atacadao"], produto_data=produto_raw.to_dict())
                            print(f"Produto {produto_raw.descricao}, salvo com sucesso")

            except Exception as e:
                print(f'O erro foi de {type(e)}: e')
                continue

class Preco:
    def __init__(self, raw_data) -> None:
        """
        raw_data -> json de dados dos preços recebidos pelal API ou extraído do produto
        """
        #Campos extraidos
        self.produto_id = raw_data.get("produto_id")
        self.preco_max = None
        self.preco_min = None
        self.preco_atual_low = raw_data.get("preco_atual_low")
        self.preco_atual_high = raw_data.get("preco_atual_high")
        self.qnt_min_low = raw_data.get("qnt_min_low")
        self.qnt_min_high = raw_data.get("qnt_min_high")
        self.dias_sem_atualizar = None
        self.data_coleta = datetime.now().date()


    def to_dict(self)->dict:
       """Retorna os dados como dicionário para uso em DataFrame ou JSON"""
       return {
        "produto_id": self.produto_id,
        "preco_max": self.preco_max,
        "preco_min": self.preco_min,
        "preco_atual_low": self.preco_atual_low,
        "preco_atual_high": self.preco_atual_high,
        "qnt_min_low":self.qnt_min_low, 
        "qnt_min_high": self.qnt_min_high, 
        "dias_sem_atualizar": self.dias_sem_atualizar,
        "ultima_coleta": self.data_coleta,
        }
    

    def salvar_preco(self, database_manager)-> None:
        """Salva o preço no banco via manager"""
        database_manager.salvar_preco(self.to_dict())

 
    def parse_preco_from_produtos(produtos_data:list) -> list:

        """
        Extrai o preços da lista de produtos arrumadas no parse_pruduto() e vincula ao produto_id
        """
        precos =[]
        for produto_raw in produtos_data:
            try:
                #verificar se o produto tem os dados necessários:
                if isinstance(produto_raw.get("node",{}).get("offers"), dict) and "offers" in produto_raw["node"]["offers"]:
                    offer = produto_raw["node"]["offers"]["offers"]
                else:
                    offer = {}

                preco = {
                    "produto_id":produto_raw.get("node",{}).get("id"),
                    "preco_atual_low": offer[0].get("listPrice",{}),
                    "preco_atual_high": offer[1].get("listPrice",{}) if len(offer) == 2 else offer[0].get("listPrice",{}),
                    "qnt_min_low": offer[0].get("minQuantity",{}), 
                    "qnt_min_high": offer[1].get("minQuantity",{}) if len(offer) == 2 else offer[0].get("minQuantity",{}), 
                    }
      
                preco = Preco(raw_data=preco)
                precos.append(preco)
                
            
            except Exception as e:
                print(f'Erro ao processar preço do produto: {type(e)}: {e}')
                continue

        return precos
    

    def compara_mudanca_preco(preco:dict, ultimo_preco:list[tuple]) -> dict:
        """
        Compara o preço coleta com o preço no banco de dados.
        Se houver mudança ele retorna True se não retorna False
        Retorna: {'mudou': bool, 'diferenca': float, 'percentual': float}
        """
        try:
            product_id = preco.produto_id
            
            if len(ultimo_preco) == 0:
                print(f"primeiro registro de preço do produto: {product_id}")
                return {
                    'mudou': True, 
                    'diferenca': 0, 
                    'percentual': 0
                    }
            ultimo_preco = ultimo_preco[0]
            (
             db_id, 
             produto_id, 
             preco_max, 
             preco_min, 
             preco_atual_low, 
             preco_atual_high, 
             quantidade_minima_low, 
             quantidade_maxima_high, 
             data_ultima_coleta,  
             dias_sem_atualizar
             ) = ultimo_preco
                        
            
            if preco_atual_high != preco.preco_atual_high:
                diferenca =  preco.preco_atual_high - preco_atual_high 
                percentual = (diferenca/preco_atual_high) * 100 if preco_atual_high > 0 else 0 
                
                return {
                'mudou': True, 
                'diferenca': round(diferenca, 2), 
                'percentual': round(percentual, 2)
                }
            else:
                return {
                    'mudou': False, 
                    'diferenca': 0, 
                    'percentual': 0
                    }
        except Exception as e:
            print(f"Erro ao comparar preços: {e}")
            return {'mudou': False, 'diferenca': 0, 'percentual': 0}


    def atualizar_novo_preco(preco:dict, ultimo_preco:list) -> None:
        preco_max = None
        preco_min = None
        if len(ultimo_preco) != 0:
            (   db_id, 
                _produto_id, 
                _preco_max, 
                _preco_min, 
                _preco_atual_low, 
                _preco_atual_high, 
                _quantidade_minima_low, 
                _quantidade_maxima_high, 
                _data_ultima_coleta,  
                _dias_sem_atualizar
                ) = ultimo_preco[0]
            
        try: 
            
            product_id = preco.produto_id
            print("preço max: ", preco_max)
            if len(ultimo_preco) != 0:
                if _preco_max or preco_max is None:
                   preco_max =  _preco_atual_high  
                elif _preco_atual_high >= preco_max:  
                    preco_max =  _preco_atual_high 
                else:
                    preco_max = _preco_max
            if len(ultimo_preco) != 0:
                if _preco_min or preco_min is None:
                   preco_min =  _preco_atual_high
                elif _preco_atual_high <= preco_min:
                   preco_min = _preco_atual_high
                else:
                    preco_min = _preco_min

            preco_atual_low = preco.preco_atual_low
            preco_atual_high = preco.preco_atual_high
            quantidade_minima_low = preco.qnt_min_low
            quantidade_maxima_high = preco.qnt_min_high
            data_ultima_coleta = datetime.now().date()
            dias_sem_atualizar = 0

            preco_novo = (  product_id, 
                            preco_max, 
                            preco_min, 
                            preco_atual_low, 
                            preco_atual_high, 
                            quantidade_minima_low, 
                            quantidade_maxima_high, 
                            data_ultima_coleta,  
                            dias_sem_atualizar
                        )
            manager.atualizar_preco_produto(db_path=DB_PATH["atacadao"], preco_produto_data=preco_novo)

        except Exception as e:
            print(f"Erro ao salvar preços: {e}")


    def atualizar_preco_nao_atualizado(preco, ultimo_preco) -> None:

        #ultimo_preco = ultimo_preco[0]
        (
        _db_id, 
        _produto_id, 
        _preco_max, 
        _preco_min, 
        _preco_atual_low, 
        _preco_atual_high, 
        _quantidade_minima_low, 
        _quantidade_maxima_high, 
        _data_ultima_coleta,  
        _dias_sem_atualizar
        ) = ultimo_preco[0]

        data = datetime.strptime(_data_ultima_coleta, "%Y-%m-%d").date()
        data_com_dias_sem_atulizar = data+timedelta(days=_dias_sem_atualizar)
        dif_datas = (datetime.today().date() - data).days
        try: 
            if data == preco.data_coleta:
                print("coleta mesmo dia, sem alteração de preço")
                pass
            
            elif data_com_dias_sem_atulizar == datetime.today().date():
                print("coleta mesmo dia, sem alteração de preço")
                pass

            elif _dias_sem_atualizar > dif_datas:
                print(f"dias sem atualizar com data errada... corrigindo para {dif_datas} dia(s)")
                dias_sem_atualizar =  dif_datas  
                preco_data = (
                     _produto_id,
                     dias_sem_atualizar
                            )
                manager.atualizar_preco_nao_atualizado(db_path = DB_PATH["atacadao"], preco_produto_data=preco_data)
            else:

                dias_sem_atualizar = _dias_sem_atualizar + 1 

                preco_data = (
                     _produto_id,
                     dias_sem_atualizar
                            )
                manager.atualizar_preco_nao_atualizado(db_path = DB_PATH["atacadao"], preco_produto_data=preco_data)

        except Exception as e:
            print(f"Erro ao salvar preços: {e}")


    def inserir_log_precos(preco, db_path) -> None:
        _preco = (
        preco.produto_id,
        preco.preco_atual_low,
        preco.preco_atual_high,
        preco.qnt_min_low,
        preco.qnt_min_high,
        preco.data_coleta,
        )
        manager.log_preco(db_path=db_path, preco_produto_data=_preco)

        