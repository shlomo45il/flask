from datetime import datetime
from database import db

class InventoryTransaction(db.Model):
    __tablename__ = 'inventory_transactions'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    reference = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # קשרים
    product = db.relationship('Product', backref='inventory_transactions')
    location = db.relationship('Location', backref='inventory_transactions')
    user = db.relationship('User', backref='inventory_transactions')

    @classmethod
    def create(cls, **kwargs):
        """יצירת תנועת מלאי ועדכון המלאי"""
        transaction = cls(**kwargs)
        db.session.add(transaction)
        
        # עדכון המלאי
        inventory = Inventory.query.filter_by(
            product_id=transaction.product_id,
            location_id=transaction.location_id
        ).first()
        
        if not inventory:
            inventory = Inventory(
                product_id=transaction.product_id,
                location_id=transaction.location_id,
                quantity=0
            )
            db.session.add(inventory)
        
        # עדכון הכמות בהתאם לסוג התנועה
        if transaction.transaction_type in ['receive', 'restock']:
            inventory.quantity += transaction.quantity
        elif transaction.transaction_type in ['issue', 'transfer_out']:
            inventory.quantity -= transaction.quantity
        
        db.session.commit()
        return transaction

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # קשרים
    product = db.relationship('Product', backref='inventory')
    location = db.relationship('Location', backref='inventory')

    __table_args__ = (
        db.UniqueConstraint('product_id', 'location_id', name='uix_product_location'),
    )

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 