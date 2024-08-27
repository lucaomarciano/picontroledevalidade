import sqlite3

# Conectar ao banco de dados (cria se não existir)
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Criar a tabela 'products' se não existir
c.execute('''CREATE TABLE IF NOT EXISTS products
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            barcode TEXT NOT NULL,
            expiry_date TEXT NOT NULL)''')

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Tabela 'products' criada com sucesso (se não existia).")
