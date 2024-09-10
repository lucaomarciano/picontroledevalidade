from flask import app
import pytest
from app import connect_db, check_expiry_dates, send_sms
import datetime
from twilio.rest import Client

def test_connect_db(client):
    conn = connect_db()
    assert conn is not None, "Deve conectar ao banco de dados"

def test_check_expiry_dates(client):
    conn = connect_db()
    conn.execute("INSERT INTO products (description, barcode, expiry_date) VALUES (?, ?, ?)", 
                 ("Produto Teste", "123456789", (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')))
    conn.commit()
    products = check_expiry_dates()
    assert len(products) == 1, "Deve encontrar um produto próximo do vencimento"
    assert products[0][1] == "Produto Teste", "Deve encontrar o produto correto"

def test_send_sms(mocker):
    mock_client = mocker.patch.object(Client, 'messages', autospec=True)
    
    send_sms("Teste de SMS")
    
    mock_client.create.assert_called_once_with(
        body="Teste de SMS",
        from_='+12565790822',
        to='+5518991497238'
    )

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Controle de Validade de Produtos" in response.get_data(as_text=True)

def test_add_product(client):
    response = client.post('/add_product', data={
        'description': 'Produto Teste',
        'barcode': '123456789',
        'expiry_date': '2024-09-15'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Produto adicionado com sucesso!" in response.get_data(as_text=True)

    # Verifica se o produto foi adicionado
    conn = connect_db()
    product = conn.execute("SELECT * FROM products WHERE description = ?", ("Produto Teste",)).fetchone()
    assert product is not None, "Produto deve ser adicionado ao banco de dados"

def test_delete_product(client):
    conn = connect_db()
    conn.execute("INSERT INTO products (description, barcode, expiry_date) VALUES (?, ?, ?)",
                 ("Produto para Excluir", "987654321", "2024-09-15"))
    conn.commit()

    product = conn.execute("SELECT * FROM products WHERE description = ?", ("Produto para Excluir",)).fetchone()
    assert product is not None, "Produto deve existir antes de ser excluído"

    response = client.post(f'/delete_product/{product[0]}', follow_redirects=True)
    assert response.status_code == 200
    assert "Produto excluído com sucesso!" in response.get_data(as_text=True)

    product = conn.execute("SELECT * FROM products WHERE description = ?", ("Produto para Excluir",)).fetchone()
    assert product is None, "Produto deve ser excluído do banco de dados"

def test_edit_product(client):
    conn = connect_db()
    conn.execute("INSERT INTO products (description, barcode, expiry_date) VALUES (?, ?, ?)",
                 ("Produto para Editar", "111222333", "2024-09-15"))
    conn.commit()

    product = conn.execute("SELECT * FROM products WHERE description = ?", ("Produto para Editar",)).fetchone()
    assert product is not None, "Produto deve existir antes de ser editado"

    response = client.post(f'/edit_product/{product[0]}', data={
        'description': 'Produto Editado',
        'barcode': '444555666',
        'expiry_date': '2024-10-10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Produto atualizado com sucesso!" in response.get_data(as_text=True)

    product = conn.execute("SELECT * FROM products WHERE id = ?", (product[0],)).fetchone()
    assert product[1] == "Produto Editado", "Descrição do produto deve ser atualizada"
    assert product[2] == "444555666", "Código de barras deve ser atualizado"
    assert product[3] == "2024-10-10", "Data de validade deve ser atualizada"
