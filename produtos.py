import sqlite3

def exibir_produtos():
    # Conectar ao banco de dados
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Executar a consulta para selecionar todos os produtos
    c.execute("SELECT * FROM products")
    produtos = c.fetchall()

    # Exibir os produtos
    if produtos:
        print(f"{'ID':<5} {'Descrição':<20} {'Código de Barras':<20} {'Data de Validade':<15}")
        print("="*60)
        for produto in produtos:
            id, descricao, codigo_barras, data_validade = produto
            print(f"{id:<5} {descricao:<20} {codigo_barras:<20} {data_validade:<15}")
    else:
        print("Nenhum produto encontrado.")

    # Fechar a conexão com o banco de dados
    conn.close()

if __name__ == "__main__":
    exibir_produtos()
