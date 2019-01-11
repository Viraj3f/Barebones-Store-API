"""
Database Models the store
"""
from barebones import db


class Serializable:
    """
    Mixin that provides an "as_dict" method for JSON serializtion
    """

    def as_dict(self):
        raise NotImplementedError


class Producer(db.Model, Serializable):
    """
    Model for the producer, those who can create products.
    """
    __tablename___ = 'producer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    products = db.relationship("Product")

    def as_dict(self):
        d = {
            "id": self.id,
            "username": self.username,
            "products": []
        }

        for product in self.products:
            d["products"].append(product.as_dict())

        return d


class Product(db.Model, Serializable):
    """
    Model for specific products.
    """
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(20), nullable=False)
    inventory_count = db.Column(db.Integer, nullable=False, default=0)

    @db.validates('price')
    def validate_price(self, key, price):
        assert price >= 0.1
        return price

    @db.validates('inventory_count')
    def validate_inventory_count(self, key, inventory_count):
        assert inventory_count >= 0
        return int(inventory_count)

    def as_dict(self):
        return {
            "id": self.id,
            "producer_id": self.producer_id,
            "title": self.title,
            "price": float(self.price),
            "inventory_count": self.inventory_count
        }


class ShoppingCart(db.Model, Serializable):
    """
    Model for the shopping cart, which will contain elements of an eventual
    purchase.
    """
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    cached_price = db.Column(db.Integer)

    # One to many relationship
    shopping_cart_entries = db.relationship("ShoppingCartEntry")

    def as_dict(self):
        d = {
                "id": self.id,
                "cached_price": self.cached_price,
                "shopping_cart_entries": []
            }

        for entry in self.shopping_cart_entries:
            d["shopping_cart_entries"].append(entry.as_dict())

        return d

    def recalculate_price(self):
        new_price = 0
        for entry in self.shopping_cart_entries:
            quantity = entry.quantity
            price = entry.product.price
            new_price += quantity * price

        self.cached_price = new_price

    def create_or_modify_shopping_cart_entry(self, product, quantity):
        assert 0 <= quantity <= product.inventory_count

        for entry in self.shopping_cart_entries:
            if entry.product_id == product.id:
                if quantity == 0:
                    self.cached_price = \
                        ShoppingCart.cached_price - \
                        entry.quantity * product.price
                    db.session.delete(entry)
                else:
                    self.cached_price = \
                        ShoppingCart.cached_price + \
                        product.price * (quantity - entry.quantity)
                    entry.quantity = quantity

                return

        if quantity > 0:
            entry = ShoppingCartEntry(
                    shopping_cart_id=self.id,
                    quantity=quantity,
                    product_id=product.id)
            self.cached_price = \
                ShoppingCart.cached_price + quantity * product.price
            db.session.add(entry)


class ShoppingCartEntry(db.Model, Serializable):
    """
    Model for the shopping cart entry, which corresponds to a specfic
    number of products.
    """
    __tablename__ = 'shopping_cart_entry'
    id = db.Column(db.Integer, primary_key=True)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey("shopping_cart.id"))
    quantity = db.Column(db.Integer, nullable=False, default=0)

    # Many to one relationship
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product")

    @db.validates('quantity')
    def validate_quantity(self, key, quantity):
        assert quantity > 0
        return int(quantity)

    def as_dict(self):
        return {
                "id": self.id,
                "shopping_cart_id": self.shopping_cart_id,
                "quantity": self.quantity,
                "product_id": self.product_id,
                "product": self.product.as_dict()
            }
