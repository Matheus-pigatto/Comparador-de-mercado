# Teste corrigido
import requests

def testar_webshare_proxy():
    # Sua API key está correta
    api_key = #inserir a chave da API
    
    # URL correta do Webshare (note o "p.webshare.io")
    proxy_url = f"https://ipv4.webshare.io/"
    
    proxies = {
        "http": ,#insira a URL do proxy http
        "https": #insira a URL do proxy https 
    }
    
    try:
        response = requests.get(
            'http://httpbin.org/ip',  # Serviço que mostra seu IP
            proxies=proxies,
            timeout=10
        )
        print("✅ Proxy funcionando!")
        print("Status code:", response.status_code)
        print("Headers:", dict(response.headers))
        print("Conteúdo:", response.text[:200])  # Primeiros 200 caracteres
        return True
    except Exception as e:
        print(f"❌ Proxy não está funcionando: {e}")
        return False

# Execute o teste
if __name__ == "__main__":
    testar_webshare_proxy()
