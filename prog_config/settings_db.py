#white list de tabelas e colunas permitidas 
TABELAS_PERMITIDAS ={
    "produtos", "preco", "departamentos", "log_precos"  
    }

COLUNAS_PERMITIDAS_DB = {
    "produtos": ["id", "produto_id" , "marca_id", "classificacao_mercadologica_id",
                "descricao", "imagem", "disponivel", "preco", "priorizado",
                "quantidade_minima", "quantidade_maxima", "bebida_alcoolica", "link",
                "codigo_barras", "sku", "codigo_erp", "quantidade_vendida",
                "em_oferta", "quantidade_unidade_diferente", "exibe_preco_original",
                "preco_original", "unidade_sigla", "possui_unidade_diferente",
                "permitir_observacao_na_compra", "habilitar_seletor_unidade_peso",
                "observacao", "unidade_fracao", "marca", "secao_id",
                "busca_item", "volume_principal", "anunciado", "posicao",
                "urls_eventos_ads", "id_2", "data_coleta", "mercado"],
    "preco": ["id", "produto_id" ,  "preco_max" ,
                "preco_min" , "preco_atual_low" , "preco_atual_high" ,
                "qnt_min_low" , "qnt_min_high" , "dias_sem_atualizar" ,
                "data_ultima_coleta"],
    "departamentos": ["id", "classificacao_mercadologica_id", "nivel",
                    "parent_id", "descricao", "imagem", "link",
                    "total_ofertas","data_coleta","mercado"],
    "log_precos": ["id", "produto_id", "preco_low","preco_high",
                  "quantidade_maxima_low", "quantidade_maxima_high","data_coleta"]
}