import requests
from src.core.utils import delay_inteligente

# ✅ Proxy que está funcionando
PROXY_USERNAME = "Tafokaproxy01"
PROXY_PASSWORD = "qrpiwu2311ks"
PROXY_IP = "23.95.150.145"
PROXY_PORT = "6114"
api_key = "78eqnwoctd1vq19iutuu7vwngb5t72jyi4ebsvo6"

PROXY_URL = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}/"

class WebshareProxy:
    def __init__(self, username=None, password=None, ip=None, port=None):
        self.username = username or PROXY_USERNAME
        self.password = password or PROXY_PASSWORD
        self.ip = ip or PROXY_IP
        self.port = port or PROXY_PORT
        
        # ✅ Configuração correta que você testou
        self.proxy_url = f"http://{self.username}:{self.password}@{self.ip}:{self.port}/"
        self.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url,
        }
        print(f"Proxy configurado: {self.proxy_url}")
    
    def get(self, url, headers=None, params=None, **kwargs):
        """Faz requisição GET com proxy rotativo"""
        try:
            response = requests.get(
                url,
                proxies=self.proxies,
                headers=headers,
                params=params,
                timeout=30,
                **kwargs
            )
            delay_inteligente()
            return response
        except Exception as e:
            print(f"Erro na requisição GET: {e}")
            return None
    
    def post(self, url, headers=None, data=None, **kwargs):
        """Faz requisição POST com proxy rotativo"""
        try:
            response = requests.post(
                url,
                proxies=self.proxies,
                headers=headers,
                data=data,
                timeout=30,
                **kwargs
            )
            delay_inteligente()
            return response
        except Exception as e:
            print(f"Erro na requisição POST: {e}")
            return None
        
def fazer_requisicao(url, username=None, password=None, method='GET', headers=None, params=None, data=None, max_retries=3):
    """
    Função de alto nível para fazer requisições com proxy e retry automático
    """
    if not url:
        print("Erro: URL é obrigatório")
        return None
    
    proxy_manager = WebshareProxy(username=username, password=password)
    
    for attempt in range(max_retries):
        try:
            if method.upper() == 'POST':
                response = proxy_manager.post(url, headers=headers, data=data)
            else:
                response = proxy_manager.get(url, headers=headers, params=params)
            
            if response and response.status_code == 200:
                return response
            elif response and response.status_code == 429:  # Rate limit
                print("Limite de requisições atingido. Esperando...")
                delay_inteligente()
            elif attempt < max_retries - 1:
                print(f"Tentativa {attempt + 1} falhou, tentando novamente...")
                delay_inteligente()
                
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou com erro: {e}")
            if attempt < max_retries - 1:
                delay_inteligente()
    
    print(f"Todas as {max_retries} tentativas falharam")
    return None


