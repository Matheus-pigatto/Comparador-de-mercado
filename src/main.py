#import requests
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from datetime import datetime

from mercados.shibata.api_client import routine_shibata
from mercados.atacadao.api_client import coleta_departamento, routine_atacadao
def main():

    inicio = datetime.now()
    #routine_shibata()
    routine_atacadao()
    final = datetime.now()
    tempo_total = final - inicio
    
    print(f"O tempo de atualização foi de {tempo_total}")


if __name__ == "__main__":
    main()