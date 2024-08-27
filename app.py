from flask import Flask, render_template, request, redirect, url_for, flash
from twilio.rest import Client
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuração do Twilio
TWILIO_SID = 'AC91f6a0f4624bbe8c3b47a4d3483d6d9d'
TWILIO_AUTH_TOKEN = '5dce88c0859ba43471b2468500727a9f'
TWILIO_PHONE_NUMBER = '+12565790822'
RECIPIENT_PHONE_NUMBER = '+5518991497238'

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def connect_db():
    return sqlite3.connect('products.db')

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

@app.route('/')
def index():
    products_near_expiry = check_expiry_dates()

    if products_near_expiry:
        sms_body = f"Os seguintes produtos estão próximos da data de vencimento:\n" + \
                "\n".join([f"ID: {p[0]}, Descrição: {p[1]}, Código de Barras: {p[2]}, Data de Validade: {p[3]}" for p in products_near_expiry])
        send_sms(sms_body)
    
    return render_template('index.html', products_near_expiry=products_near_expiry)

@app.route('/add_product', methods=['POST'])
def add_product():
    description = request.form['description']
    barcode = request.form['barcode']
    expiry_date = request.form['expiry_date']

    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO products (description, barcode, expiry_date) VALUES (?, ?, ?)", 
            (description, barcode, expiry_date))
    conn.commit()
    conn.close()

    flash('Produto adicionado com sucesso!')
    return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('Produto excluído com sucesso!')
    return redirect(url_for('show_products'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
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
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('show_products'))

    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/show_products')
def show_products():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT id, description, barcode, expiry_date FROM products")
    products = c.fetchall()
    conn.close()

    # Formatar a data de validade como dd/mm/aaaa
    formatted_products = []
    for product in products:
        formatted_date = datetime.datetime.strptime(product[3], '%Y-%m-%d').strftime('%d/%m/%Y')
        formatted_products.append((product[0], product[1], product[2], formatted_date))
    
    return render_template('show_products.html', products=formatted_products)

if __name__ == '__main__':
    app.run(debug=True)
