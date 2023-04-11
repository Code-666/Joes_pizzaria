from pizzaria import db

# A customer can place many orders
class Customer(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    orders = db.relationship('Order', backref='customer_order', lazy=True)
    carts = db.relationship('Cart', backref='customer_cart', lazy=True)

    def __repr__(self):
        return f'name: {self.name}'

# One order can have many products and one product can be in many orders


order_pizza = db.Table('order_pizza', db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
                         db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'))
                         )

cart_pizza = db.Table('cart_pizza', db.Column('cart_id', db.Integer, db.ForeignKey('cart.id')),
                         db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'))
                         )


class Order(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    pizzas = db.relationship(
        'Pizza', secondary=order_pizza, backref='pizza_order')

    def __repr__(self):
        return f'id: {self.id_}'

class Cart(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    pizzas = db.relationship(
        'Pizza', secondary=cart_pizza, backref='pizza_cart')

    def __repr__(self):
        return f'id: {self.id_}'


class Pizza(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    size = db.Column(db.String(50))
    toppings = db.Column(db.Text)


    def __repr__(self):
        return f'name: {self.name}'

class Admin(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self):
        return f'name: {self.name}'
