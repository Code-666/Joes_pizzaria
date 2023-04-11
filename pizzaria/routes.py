from flask import render_template, url_for, request, redirect, session
import pandas as pd
from pizzaria import app, db
from pizzaria.models import Pizza, Order, Customer, Admin, Cart, cart_pizza

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/menu')
def menu():
    pizzas = Pizza.query.all()
    for pizza in pizzas:
        print(pizza.id_)
    return render_template("menu.html", title='Menu', pizzas=pizzas)

@app.route("/received")
def received():
    if "user" in session:
        orders = Order.query.all()
        return render_template('orders.html', orders=orders)
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        a1 = request.form['nm']
        p1 = request.form['pw']
        admin = Admin.query.filter_by(name=a1).first()
        if admin and p1 == admin.password:
            session['user'] = a1
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST', 'DELETE'])
def admin():
    if 'user' in session:
        return render_template('admin.html')

@app.route('/add_pizza', methods=['POST'])
def add_pizza():
    name = request.form['name']
    price = request.form['price']
    size = request.form['size']
    toppings = request.form['toppings']
    pizza = Pizza(name=name, price=price, size=size, toppings=toppings)
    db.session.add(pizza)
    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/delete_pizza', methods=['POST'])
def delete_pizza():
    pizza_id = request.form['id']
    print(pizza_id)
    pizza = Pizza.query.filter_by(name=pizza_id).first()
    print(pizza)
    if pizza:
        db.session.delete(pizza)
        db.session.commit()
        return redirect(url_for('menu'))
    else:
        return redirect(url_for('admin'))

def cart_item(customer, pizza):
    cart = Cart.query.filter_by(customer_id=customer.id_).first()
    if not cart:
        cart = Cart(customer_id=customer.id_)
        db.session.add(cart)
        db.session.commit()
    pizza = Pizza.query.filter_by(name=pizza).first()
    cart.pizzas.append(pizza)
    db.session.commit()

def order_item(customer):
    cart = Cart.query.all()
    order = Order(customer_id=customer.id_)
    db.session.add(order)
    db.session.commit()
    for pizza in cart[0].pizzas:
        order.pizzas.append(pizza)
    db.session.query(Cart).delete()
    db.session.query(cart_pizza).delete()
    db.session.commit()

@app.route('/checkout', methods=['POST'])
def checkout():
    c = Customer.query.filter_by(name='customer').first()
    order_item(c)
    return redirect(url_for('home'))

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    # Access data in Flask server
    name = data['name']
    price = data['price']
    size = data['size']
    toppings = data['toppings']

    print(name)
    print(price)
    print(size)
    print(toppings)

    c = Customer.query.filter_by(name='customer').first()
    cart_item(c, name)

    return 'Data received and processed by Flask server'

@app.route('/populate_db')
def populate_db():
    # Read the CSV file into a Pandas dataframe
    df = pd.read_csv('pizzeria.csv')

    # Loop through the rows and add them to the database
    for index, row in df.iterrows():
        my_data = Pizza(name=row['Name'], price=row['Price'], size=row['Size'], toppings=row['Toppings'])
        db.session.add(my_data)

    # Commit the changes to the database
    db.session.commit()

    return 'Database populated successfully!'