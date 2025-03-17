from datetime import datetime
from database import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='new')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    picking_completed_at = db.Column(db.DateTime)
    restock_started_at = db.Column(db.DateTime)
    restock_completed_at = db.Column(db.DateTime)
    restock_notes = db.Column(db.Text)
    notes = db.Column(db.Text)
    shipping_address = db.Column(db.Text, nullable=False)

    # קשרים
    customer = db.relationship('Customer', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True)
    shortage_history = db.relationship('OrderShortageHistory', backref='order', lazy=True)
    restock_history = db.relationship('OrderRestockHistory', backref='order', lazy=True)

    @property
    def has_shortages(self):
        """בדיקה האם יש חוסרים בהזמנה"""
        return any(item.missing_quantity > 0 for item in self.items)

    @property
    def shortages_count(self):
        """מספר הפריטים עם חוסרים"""
        return sum(1 for item in self.items if item.missing_quantity > 0)

    @property
    def status_display(self):
        """תצוגת סטטוס בעברית"""
        status_map = {
            'new': 'חדשה',
            'picking': 'בתהליך ליקוט',
            'picking_completed': 'ליקוט הושלם',
            'waiting_for_restock': 'ממתין להשלמת מלאי',
            'restock_completed': 'השלמת מלאי הושלמה',
            'packing': 'בתהליך אריזה',
            'packing_completed': 'אריזה הושלמה',
            'shipping': 'בתהליך משלוח',
            'completed': 'הושלמה',
            'cancelled': 'בוטלה'
        }
        return status_map.get(self.status, self.status)

    @property
    def status_color(self):
        """צבע סטטוס"""
        color_map = {
            'new': 'primary',
            'picking': 'info',
            'picking_completed': 'success',
            'waiting_for_restock': 'warning',
            'restock_completed': 'success',
            'packing': 'info',
            'packing_completed': 'success',
            'shipping': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        }
        return color_map.get(self.status, 'secondary')

    @property
    def can_restock(self):
        """בדיקה האם ניתן להתחיל תהליך השלמת מלאי"""
        return self.status == 'picking_completed' and self.has_shortages

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    requested_quantity = db.Column(db.Integer, nullable=False)
    picked_quantity = db.Column(db.Integer, default=0)
    restock_location = db.Column(db.String(50))
    shortage_reason = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')

    # קשרים
    product = db.relationship('Product', backref='order_items')

    @property
    def missing_quantity(self):
        """חישוב כמות חסרה"""
        return max(0, self.requested_quantity - self.picked_quantity)

    @property
    def status_display(self):
        """תצוגת סטטוס בעברית"""
        status_map = {
            'pending': 'ממתין',
            'picked': 'נאסף',
            'shortage': 'חוסר',
            'restocked': 'הושלם'
        }
        return status_map.get(self.status, self.status)

    @property
    def status_color(self):
        """צבע סטטוס"""
        color_map = {
            'pending': 'secondary',
            'picked': 'success',
            'shortage': 'warning',
            'restocked': 'success'
        }
        return color_map.get(self.status, 'secondary')

class OrderShortageHistory(db.Model):
    __tablename__ = 'order_shortage_history'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    event = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def event_display(self):
        """תצוגת אירוע בעברית"""
        event_map = {
            'shortage_detected': 'זוהה חוסר',
            'restock_started': 'התחלת השלמת מלאי',
            'restock_completed': 'השלמת מלאי הושלמה'
        }
        return event_map.get(self.event, self.event)

class OrderRestockHistory(db.Model):
    __tablename__ = 'order_restock_history'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    event = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def event_display(self):
        """תצוגת אירוע בעברית"""
        event_map = {
            'restock_started': 'התחלת השלמת מלאי',
            'item_restocked': 'פריט הושלם',
            'restock_completed': 'השלמת מלאי הושלמה'
        }
        return event_map.get(self.event, self.event) 