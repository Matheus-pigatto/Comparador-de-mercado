import json
from datetime import datetime, timedelta
from prog_config.settings import MERCADOS, DB_PATH
from src.database.manager import atualizar_preco_produto, atualizar_preco_nao_atualizado, atualizar_preco_nao_atualizado, log_preco
from src.database import manager

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
        self.mercado = None

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

    def parse_departamento(data:list[dict]) -> list[tuple]:
        """
        Extrai e retorna uma lista de objetos Departamentos
        """
        departamentos=[]
        
        for dept in data:
            departamento = Departamento(raw_data=dept)
            departamento.mercado = MERCADOS["shibata"]
            departamentos.append(departamento)
            

            # Se tiver filhos, processamos também
            for child in dept.get("children", []):
                child_dept = Departamento(raw_data=child)
                child_dept.mercado = MERCADOS["shibata"]
                departamentos.append(child_dept)
                
        
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
        self.data_coleta = datetime.now().date() #Data da coleta
        self.mercado = None
        
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
        
        for dept in data:
            produto = Produto(raw_data=dept)
            produto.mercado = MERCADOS["shibata"]
            produtos.append(produto)
            
        
        return produtos 
    
    def atualizar_disponibilidade_produto(db_path: str, classificacao_mercadologica_id: int, disponivel: int,id_produto = None) -> None:
        # Uso:
        try:
            if id_produto is None: 
                produtos_indisponiveis = manager.encontrar_produtos_indisponiveis(
                    db_path=db_path,
                    classificacao_mercadologica_id=classificacao_mercadologica_id
                )

                if len(produtos_indisponiveis) > 0:
                    #se len for maior que 0 existe produtos indisponiveis entao ele atualiza a lista
                    manager.atualizar_produtos_indisponiveis(db_path=db_path, lista_ids=produtos_indisponiveis, novo_valor=0)
            else:
                manager.atualizar_produtos_indisponiveis(db_path=db_path, lista_ids=[id_produto], novo_valor=disponivel)
                    
            
        except Exception as e:
            print(f"Erro ao atualizar produtos indisponíveis: {e}")

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
    
    def parse_preco_from_produtos(produtos_data:list) -> list:

        """
        Extrai o preços da lista de produtos arrumadas no parse_pruduto() e vincula ao produto_id
        """
       
        produto = produtos_data
        try:
            preco = {
                "produto_id":produto.produto_id,
                "preco_atual_low": produto.preco,
                "preco_atual_high": produto.preco,
                "qnt_min_low": produto.quantidade_minima, 
                "qnt_min_high": None, 
                }
    
            preco = Preco(raw_data=preco)
            
            
        
        except Exception as e:
            print(f'Erro ao processar preço do produto: {type(e)}: {e}')
            

        return preco
    
    def compara_mudanca_preco(preco:dict, ultimo_preco:list[tuple]) -> dict:
        """
        Compara o preço coleta com o preço no banco de dados.
        Se houver mudança ele retorna True se não retorna False
        Retorna: {'mudou': bool, 'diferenca': float, 'percentual': float}
        """
        try:
            product_id = preco.produto_id
            
            ultimo_preco = ultimo_preco[0]
            (db_id, 
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
            if len(ultimo_preco)>0:           
                _preco_atua_low = float(preco.preco_atual_low)
                if preco_atual_low != _preco_atua_low:
                    diferenca =  float(preco.preco_atual_low) - preco_atual_low 
                    percentual = (diferenca/float(preco_atual_low)) * 100 if preco_atual_low > 0 else 0 
                    
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
            print(f"Não há registro de ultimo preço: {len(ultimo_preco)}")
            print(f"Erro ao comparar preços: {e}")
            return {'mudou': False, 'diferenca': 0, 'percentual': 0}

    def atualizar_novo_preco(preco:dict, ultimo_preco:list) -> None:
        
        if len(ultimo_preco) != 0:
                (db_id, 
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
            if len(ultimo_preco) != 0:
                if _preco_max == None: preco_max =  float(preco.preco_atual_low)
                else: preco_max = float(preco.preco_atual_low) if float(preco.preco_atual_low) >= _preco_max else _preco_max
            else:
                preco_max = float(preco.preco_max)
            if len(ultimo_preco) != 0:
                if _preco_min == None: preco_min = float(preco.preco_atual_low)
                else: preco_min = float(preco.preco_atual_low) if float(preco.preco_atual_low) <= _preco_min or _preco_min == None else _preco_min
            else:
                preco_min = float(preco.preco_min)
            
            preco_atual_low = float(preco.preco_atual_low)
            preco_atual_high = preco.preco_atual_high
            quantidade_minima_low = float(preco.qnt_min_low)
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
            atualizar_preco_produto(db_path=DB_PATH["shibata"], preco_produto_data=preco_novo)

        except Exception as e:
            print(f"Erro em atualizar_preço_novo")
            print(f"Erro ao salvar preços: {e}")

    def atualizar_preco_nao_atualizado(preco, ultimo_preco) -> None:
        if len(ultimo_preco)>0:
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

        else:
            _data_ultima_coleta= None  
            _dias_sem_atualizar= 0
            data = None
            data_com_dias_sem_atulizar = None
            dif_datas = 0
        
        
        try: 
            if data == preco.data_coleta:
                #print("coleta mesmo dia, sem alteração de preço")
                pass
            
            elif data_com_dias_sem_atulizar == datetime.today().date():
                #print("coleta mesmo dia, sem alteração de preço")
                pass

            elif _dias_sem_atualizar > dif_datas:
                print(f"dias sem atualizar com data errada... corrigindo para {dif_datas} dia(s)")
                dias_sem_atualizar =  dif_datas  
                preco_data = (
                     _produto_id,
                     dias_sem_atualizar
                            )
                atualizar_preco_nao_atualizado(db_path = DB_PATH["shibata"], preco_produto_data=preco_data)
            else:

                dias_sem_atualizar = _dias_sem_atualizar + 1 

                preco_data = (
                     preco.produto_id,
                     dias_sem_atualizar
                            )
                atualizar_preco_nao_atualizado(db_path = DB_PATH["shibata"], preco_produto_data=preco_data)

        except Exception as e:
            print(f"Erro em atualizar_preço_nao_atualizado")
            print(f"Erro ao salvar preços: {e}")

    def inserir_log_precos(preco, db_path) -> None:
        _preco = (
        int(preco.produto_id),
        float(preco.preco_atual_low),
        preco.preco_atual_high,
        int(preco.qnt_min_low),
        preco.qnt_min_high,
        preco.data_coleta,
        )
        resultado_ult_registro = manager.pesquisa_ultimo_log(db_path=db_path, preco_produto_data=_preco)
        if len(resultado_ult_registro) != 0:
            
            data = datetime.strptime(resultado_ult_registro[-1][-1], "%Y-%m-%d").date()
            if data == _preco[-1]: 
                #print("produto ja cadastrado no log hoje")
                pass

        log_preco(db_path=db_path, preco_produto_data=_preco)
    
    def inserir_preco_produto(preco, db_path) -> None:
        preco_produto_data={}
        preco_produto_data["produto_id"]=int(preco.produto_id)
        preco_produto_data["preco_max"]=None
        preco_produto_data["preco_min"]=None
        preco_produto_data["preco_atual_low"]=float(preco.preco_atual_low)
        preco_produto_data["preco_atual_high"]=preco.preco_atual_high
        preco_produto_data["qnt_min_low"]=int(preco.qnt_min_low)
        preco_produto_data["qnt_min_high"]=preco.qnt_min_high
        preco_produto_data["ultima_coleta"]=preco.data_coleta
        preco_produto_data["dias_sem_atualizar"]= 0
        _preco =(preco_produto_data)
        manager.salvar_preco_produto(db_path=db_path,preco_produto_data=_preco)
                              
class Carrinho():
    def __init__(self, raw_data) -> None:
        """
        raw_data é o json de dados dos itens no carrinho recebido pela API
        """

        #campos extraidos
        self.produto_id = raw_data.get("produto_id")
        self.descricao = raw_data.get("descricao")
        self.preco = raw_data.get("preco")
        self.quantidade_minima = raw_data.get("quantidade_minima")
        self.quantidade_maxima = raw_data.get("quantidade_maxima")
        self.em_oferta = raw_data.get("em_oferta")
        self.imagem = raw_data.get("imagem")
        self.quantidade_unidade_diferente = raw_data.get("quantidade_unidade_diferente")
        self.preco_original = raw_data.get("preco_original")
        self.unidade_sigla = raw_data.get("unidade_sigla")
        self.possui_unidade_diferente = raw_data.get("possui_unidade_diferente")
        self.permitir_observacao_na_compra = raw_data.get("permitir_observacao_na_compra")
        self.habilitar_seletor_unidade_peso = raw_data.get("habilitar_seletor_unidade_peso")
        self.observacao = raw_data.get("observacao")
        self.secao_id = raw_data.get("departamento").get("id")
        self.departamento = raw_data.get("departamento").get("descricao")
        self.data_coleta = datetime.now().date() #Data da coleta
        self.mercado = None
        
    def to_dict(self):# -> dict[str, Any]:

        """ Retorna os dados como dicionário para uso em DataFrame ou JSON"""

        return {
            "produto_id" : self.produto_id,
            "descricao":self.descricao,
            "preco":self.preco,
            "quantidade_minima":self.quantidade_minima,
            "quantidade_maxima":self.quantidade_maxima,
            "em_oferta":self.em_oferta,
            "imagem":self.imagem,
            "quantidade_unidade_diferente":self.quantidade_unidade_diferente,
            "preco_original":self.preco_original,
            "unidade_sigla":self.unidade_sigla,
            "possui_unidade_diferente":self.possui_unidade_diferente,
            "permitir_observacao_na_compra":self.permitir_observacao_na_compra,
            "habilitar_seletor_unidade_peso":self.habilitar_seletor_unidade_peso,
            "observacao":self.observacao,
            "secao_id":self.secao_id,
            "departamento": self.departamento,
            "data_coleta":self.data_coleta,
            "mercado":self.mercado,
        }
    
    @staticmethod # Adicione este decorador se for um método estático que não usa 'self' ou 'cls
    def parse_carrinho(data:list[dict]) -> list:
        """
        Extrai e retorna uma lista de objetos produtos
        """
        carrinhos = [] # Inicialize a lista de retorno
        if not data: # Se os dados de entrada estiverem vazios, retorne uma lista vazia
            return carrinhos

        produtos=[]
        dados_carrinho = {
        "carrinho_id": data.get("carrinho_id"),
        "centro_distribuicao_id": data.get("centro_distribuicao_id"),
        "quantidade_carrinho": data.get("quantidade"),
        "sub_total": data.get("preco"),
        "valor_minimo": data.get("valor_minimo"),
        "quantidade_limite":data.get("quantidade_limite")
        }
        produtos.append(dados_carrinho)
        try:
            for dept in data.get("itens"):
                produto = Carrinho(raw_data=dept)
                produtos.append(produto)
        except Exception as e:
            print(f"[ERRO em parse_carrinho] Falha ao parsear item: {e}")
            # Você pode querer logar o erro ou retornar uma lista vazia em caso de falha
            return [] # Retorna lista vazia em caso de erro no parsing    
        
        return produtos 
    