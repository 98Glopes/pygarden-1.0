# 06_read_data.py
import sqlite3

conn = sqlite3.connect('pygarden.db')
cursor = conn.cursor()

# lendo os dados
cursor.execute("""
SELECT * FROM pygarden;
""")

result = cursor.fetchall()
result = result[len(result)-20:]
retorno = [[1],[],[],[],[]]
for linha in result:
	for i in [0,1,2,3,4]:
		retorno[i].append(linha[i])
return retorno
conn.close()
