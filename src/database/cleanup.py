import sqlite3
from prog_config.settings import DB_PATH


conn = sqlite3.connect(database=DB_PATH["shibata"])
cursor = conn.cursor()

# Identificar os registros duplicados e manter apenas o com a data_coleta mais antiga
cursor.execute('''
    DELETE FROM produtos
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM produtos
        GROUP BY produto_id
    )
''')

conn.commit()
conn.close()
print("Registros duplicados removidos com sucesso.")


