import requests
import time
import json
from datetime import datetime
import sqlite3
from prog_config.settings import MERCADOS, DB_PATH
from src.database.manager import  salvar_produto
from src.database.manager import pesquisa_produto_db, carregar_db
#import src.mercados.atacadao.parser as parser
import pandas as pd

print(datetime.now().date())