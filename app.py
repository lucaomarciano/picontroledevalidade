import os
from flask import Flask, render_template, request, redirect, url_for, flash
from twilio.rest import Client
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import sqlite3
import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

# Configuração do Twilio usando variáveis de ambiente
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RECIPIENT_PHONE_NUMBER = '+5518991497238'  # Pode ser movido para o .env

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Registrar adaptadores para datas e datetimes
def adapt_date(date):
    return date.isoformat()

def adapt_datetime(timestamp):
    return timestamp.isoformat()

def convert_date(date_string):
    return datetime.date.fromisoformat(date_string)

def convert_datetime(timestamp_string):
    return datetime.datetime.fromisoformat(timestamp_string)

# Registra os adaptadores e conversores com o SQLite
sqlite3.register_adapter(datetime.date, adapt_date)
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("timestamp", convert_datetime)

# Função de conexão com banco de dados
def connect_db():
    return sqlite3.connect('products.db', detect_types=sqlite3.PARSE_DECLTYPES)

# Classe do usuário para autenticação
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None

# Criar tabela de usuários
def create_users_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_users_table()

# Funções principais
def check_expiry_dates():
    today = datetime.date.today()
    upcoming_expiry = today + datetime.timedelta(days=10)

    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE expiry_date BETWEEN ? AND ?", 
            (today, upcoming_expiry))
    products = c.fetchall()
    conn.close()
    
    return products

def send_sms(body):
    client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=RECIPIENT_PHONE_NUMBER
    )

# Rotas do aplicativo
@app.route('/')
@login_required
def index():
    products_near_expiry = check_expiry_dates()

    if products_near_expiry:
        sms_body = f"Os seguintes produtos estão próximos da data de vencimento:\n" + \
                "\n".join([f"ID: {p[0]}, Descrição: {p[1]}, Código de Barras: {p[2]}, Data de Validade: {p[3]}" for p in products_near_expiry])
        send_sms(sms_body)
    
    return render_template('index.html', products_near_expiry=products_near_expiry)

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    description = request.form['description']
    barcode = request.form['barcode']
    expiry_date = request.form['expiry_date']

    if not description or not barcode or not expiry_date:
        flash('Todos os campos são obrigatórios!', 'danger')
        return redirect(url_for('index'))

    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO products (description, barcode, expiry_date) VALUES (?, ?, ?)", 
            (description, barcode, expiry_date))
    conn.commit()
    conn.close()

    flash('Produto adicionado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('show_products'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    conn = connect_db()
    c = conn.cursor()
    
    if request.method == 'POST':
        description = request.form['description']
        barcode = request.form['barcode']
        expiry_date = request.form['expiry_date']
        
        c.execute("UPDATE products SET description = ?, barcode = ?, expiry_date = ? WHERE id = ?",
                (description, barcode, expiry_date, product_id))
        conn.commit()
        conn.close()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('show_products'))

    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/show_products')
@login_required
def show_products():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT id, description, barcode, expiry_date FROM products")
    products = c.fetchall()
    conn.close()

    formatted_products = []
    for product in products:
        formatted_date = datetime.datetime.strptime(product[3], '%Y-%m-%d').strftime('%d/%m/%Y')
        formatted_products.append((product[0], product[1], product[2], formatted_date))
    
    return render_template('show_products.html', products=formatted_products)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            user_obj = User(id=user[0], username=user[1], password=user[2])
            login_user(user_obj)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = connect_db()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe!', 'danger')
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
