from app import db


class Producer(db.Model):
    __tablename___ = 'producer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    products = db.relationship("Product")


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    inventory_count = db.Column(db.Integer, nullable=False, default=0)


class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    cached_price = db.Column(db.Integer)

    # One to many relationship
    # shopping_cart_entries = db.relationship("shopping_cart_entry")


class ShoppingCartEntry(db.Model):
    __tablename__ = 'shopping_cart_entry'
    id = db.Column(db.Integer, primary_key=True)
    # shopping_cart_id = db.Column(db.Integer, db.ForeignKey("shopping_cart.id"))
    quantity = db.Column(db.Integer, nullable=False, default=0)

    # Many to one relationship
    # product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # product = db.relationship("product")
