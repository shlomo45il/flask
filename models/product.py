from datetime import datetime
from database import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    min_stock = db.Column(db.Integer, default=0)
    max_stock = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # קשרים
    category = db.relationship('Category', backref='products')
    supplier = db.relationship('Supplier', backref='products')

    def quantity_below_min_stock(self):
        """בדיקה האם המלאי מתחת למינימום"""
        total_quantity = sum(inv.quantity for inv in self.inventory)
        return total_quantity < self.min_stock

    def get_total_quantity(self):
        """קבלת סך הכמות במלאי"""
        return sum(inv.quantity for inv in self.inventory)

    def get_quantity_by_location(self, location_id):
        """קבלת כמות במלאי לפי מיקום"""
        inventory = next((inv for inv in self.inventory if inv.location_id == location_id), None)
        return inventory.quantity if inventory else 0

    def get_locations_with_stock(self):
        """קבלת רשימת מיקומים עם מלאי"""
        return [inv.location for inv in self.inventory if inv.quantity > 0]

    def get_stock_value(self):
        """חישוב ערך המלאי"""
        return self.get_total_quantity() * self.unit_price

    def get_stock_turnover(self, days=30):
        """חישוב קצב המכירות (יחידות ליום)"""
        from datetime import timedelta
        from models.order import OrderItem

        start_date = datetime.utcnow() - timedelta(days=days)
        sold_items = OrderItem.query.join(Order).filter(
            OrderItem.product_id == self.id,
            Order.created_at >= start_date,
            Order.status == 'completed'
        ).all()

        total_sold = sum(item.requested_quantity for item in sold_items)
        return total_sold / days

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # קשרים
    parent = db.relationship('Category', remote_side=[id], backref='children')

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 