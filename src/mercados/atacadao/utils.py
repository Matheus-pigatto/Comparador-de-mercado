from typing import Any
import requests
import json



def query_pesquisa(cod_barra:int) -> Any:

    url = "https://www.atacadao.com.br/api/graphql?"

    cod_barra = str(cod_barra)

    headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }

    variables = {
            "term": cod_barra,
            "selectedFacets": [
                {"key": "channel", "value": "{\"salesChannel\":\"1\",\"regionId\":\"v2.2C77AEF626FE4CCFE9F2E84CB8792D37\",\"seller\":\"atacadaobr744\"}"},
                {"key": "locale", "value": "pt-BR"}
            ]
        }
    params = {
            "operationName": "SearchSuggestionsQuery",
            "variables": json.dumps(variables)
        }

    response = requests.get(url, headers=headers, params=params)
    return response.json()
