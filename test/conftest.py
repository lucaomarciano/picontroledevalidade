import pytest
from app import app, connect_db
import os
import tempfile

@pytest.fixture
def client():
    # Cria um banco de dados temporário para os testes
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            conn = connect_db()
            conn.execute("DROP TABLE IF EXISTS products")  # Limpa a tabela se já existir
            conn.execute("""
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY, 
                    description TEXT, 
                    barcode TEXT, 
                    expiry_date TEXT
                )
            """)
            conn.commit()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
