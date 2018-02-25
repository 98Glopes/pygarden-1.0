# db_inti.py
# criação do banco de dados
# tabela: id, date, hour, v1, v2, v3, s1, s2, s3, umid, temp

import sqlite3

# conectando...
conn = sqlite3.connect('pygarden.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE pygarden (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        date TEXT,
		s1 REAL NOT NULL,
		umid REAL NOT NULL,
		temp REAL NOT NULL
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()