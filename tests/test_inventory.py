import pytest
from datetime import datetime, timedelta
from models.product import Product
from models.location import Location
from models.inventory import Inventory, InventoryTransaction
from models.order import Order, OrderItem
from models.customer import Customer
from database import db

@pytest.fixture
def setup_test_data():
    """הגדרת נתוני בדיקה"""
    # יצירת מוצרים
    products = {
        'product1': Product(
            name='מוצר 1',
            sku='P001',
            description='מוצר בדיקה 1',
            unit_price=100,
            min_stock=10
        ),
        'product2': Product(
            name='מוצר 2',
            sku='P002',
            description='מוצר בדיקה 2',
            unit_price=200,
            min_stock=5
        )
    }

    # יצירת מיקומים
    locations = {
        'location1': Location(
            name='מדף A1',
            code='A1',
            description='מדף ראשון בשורה A'
        ),
        'location2': Location(
            name='מדף A2',
            code='A2',
            description='מדף שני בשורה A'
        ),
        'location3': Location(
            name='מדף B1',
            code='B1',
            description='מדף ראשון בשורה B'
        )
    }

    # יצירת לקוח
    customer = Customer(
        name='לקוח בדיקה',
        email='test@example.com',
        phone='0501234567'
    )

    # שמירת כל הנתונים
    for product in products.values():
        db.session.add(product)
    for location in locations.values():
        db.session.add(location)
    db.session.add(customer)
    db.session.commit()

    return {
        'products': products,
        'locations': locations,
        'customer': customer
    }

def test_inventory_receive(setup_test_data):
    """בדיקת קבלת מלאי"""
    product = setup_test_data['products']['product1']
    location = setup_test_data['locations']['location1']

    # קבלת מלאי
    transaction = InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=20,
        transaction_type='receive',
        reference='PO-001',
        notes='קבלת מלאי ראשונית',
        created_by=1
    )

    # בדיקת תנועת המלאי
    assert transaction.quantity == 20
    assert transaction.transaction_type == 'receive'
    assert transaction.reference == 'PO-001'

    # בדיקת המלאי הנוכחי
    inventory = Inventory.query.filter_by(
        product_id=product.id,
        location_id=location.id
    ).first()
    assert inventory.quantity == 20

def test_inventory_issue(setup_test_data):
    """בדיקת הוצאת מלאי"""
    product = setup_test_data['products']['product1']
    location = setup_test_data['locations']['location1']

    # קבלת מלאי ראשונית
    InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=20,
        transaction_type='receive',
        reference='PO-001',
        notes='קבלת מלאי ראשונית',
        created_by=1
    )

    # הוצאת מלאי
    transaction = InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=5,
        transaction_type='issue',
        reference='SO-001',
        notes='הוצאת מלאי להזמנה',
        created_by=1
    )

    # בדיקת תנועת המלאי
    assert transaction.quantity == 5
    assert transaction.transaction_type == 'issue'

    # בדיקת המלאי הנוכחי
    inventory = Inventory.query.filter_by(
        product_id=product.id,
        location_id=location.id
    ).first()
    assert inventory.quantity == 15

def test_inventory_transfer(setup_test_data):
    """בדיקת העברת מלאי"""
    product = setup_test_data['products']['product1']
    source_location = setup_test_data['locations']['location1']
    target_location = setup_test_data['locations']['location2']

    # קבלת מלאי ראשונית
    InventoryTransaction.create(
        product_id=product.id,
        location_id=source_location.id,
        quantity=20,
        transaction_type='receive',
        reference='PO-001',
        notes='קבלת מלאי ראשונית',
        created_by=1
    )

    # העברת מלאי
    transaction = InventoryTransaction.create(
        product_id=product.id,
        location_id=target_location.id,
        quantity=10,
        transaction_type='transfer_in',
        reference='TR-001',
        notes='העברת מלאי למדף אחר',
        created_by=1
    )

    # בדיקת המלאי במיקום המקור
    source_inventory = Inventory.query.filter_by(
        product_id=product.id,
        location_id=source_location.id
    ).first()
    assert source_inventory.quantity == 10

    # בדיקת המלאי במיקום היעד
    target_inventory = Inventory.query.filter_by(
        product_id=product.id,
        location_id=target_location.id
    ).first()
    assert target_inventory.quantity == 10

def test_order_with_shortages(setup_test_data):
    """בדיקת הזמנה עם חוסרים"""
    product = setup_test_data['products']['product1']
    customer = setup_test_data['customer']

    # יצירת הזמנה
    order = Order(
        order_number='ORD-001',
        customer_id=customer.id,
        status='new',
        shipping_address='כתובת בדיקה'
    )
    db.session.add(order)
    db.session.commit()

    # הוספת פריט להזמנה
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        requested_quantity=10,
        picked_quantity=0,
        status='pending'
    )
    db.session.add(order_item)
    db.session.commit()

    # בדיקת חוסרים
    assert order.has_shortages == True
    assert order.shortages_count == 1
    assert order_item.missing_quantity == 10

def test_restock_process(setup_test_data):
    """בדיקת תהליך השלמת מלאי"""
    product = setup_test_data['products']['product1']
    location = setup_test_data['locations']['location1']
    customer = setup_test_data['customer']

    # יצירת הזמנה
    order = Order(
        order_number='ORD-001',
        customer_id=customer.id,
        status='picking_completed',
        shipping_address='כתובת בדיקה'
    )
    db.session.add(order)
    db.session.commit()

    # הוספת פריט להזמנה
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        requested_quantity=10,
        picked_quantity=5,
        status='shortage'
    )
    db.session.add(order_item)
    db.session.commit()

    # התחלת תהליך השלמת מלאי
    order.status = 'waiting_for_restock'
    order.restock_started_at = datetime.utcnow()
    order.restock_notes = 'התחלת השלמת מלאי'
    db.session.commit()

    # השלמת מלאי
    transaction = InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=5,
        transaction_type='restock',
        reference=f'Order {order.order_number}',
        notes=f'השלמת מלאי להזמנה {order.order_number}',
        created_by=1
    )

    # עדכון פריט ההזמנה
    order_item.picked_quantity += 5
    order_item.status = 'restocked'
    order_item.restock_location = location.code
    db.session.commit()

    # בדיקת סטטוס הזמנה
    assert order_item.missing_quantity == 0
    assert order_item.status == 'restocked'
    assert order_item.restock_location == location.code

def test_inventory_validation(setup_test_data):
    """בדיקת וולידציה של מלאי"""
    product = setup_test_data['products']['product1']
    location = setup_test_data['locations']['location1']

    # בדיקת הוצאת מלאי מעל הכמות הקיימת
    with pytest.raises(Exception):
        InventoryTransaction.create(
            product_id=product.id,
            location_id=location.id,
            quantity=100,
            transaction_type='issue',
            reference='SO-001',
            notes='הוצאת מלאי מעל הכמות הקיימת',
            created_by=1
        )

def test_inventory_reports(setup_test_data):
    """בדיקת דוחות מלאי"""
    product = setup_test_data['products']['product1']
    location = setup_test_data['locations']['location1']

    # קבלת מלאי ראשונית
    InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=20,
        transaction_type='receive',
        reference='PO-001',
        notes='קבלת מלאי ראשונית',
        created_by=1
    )

    # בדיקת מלאי נמוך
    assert product.quantity_below_min_stock() == False

    # הוצאת מלאי מתחת למינימום
    InventoryTransaction.create(
        product_id=product.id,
        location_id=location.id,
        quantity=15,
        transaction_type='issue',
        reference='SO-001',
        notes='הוצאת מלאי מתחת למינימום',
        created_by=1
    )

    # בדיקת מלאי נמוך
    assert product.quantity_below_min_stock() == True

def test_location_management(setup_test_data):
    """בדיקת ניהול מיקומים"""
    location = setup_test_data['locations']['location1']

    # בדיקת קוד מיקום ייחודי
    with pytest.raises(Exception):
        duplicate_location = Location(
            name='מדף A1',
            code='A1',  # קוד כפול
            description='מדף ראשון בשורה A'
        )
        db.session.add(duplicate_location)
        db.session.commit()

    # בדיקת עדכון מיקום
    location.name = 'מדף A1 חדש'
    location.description = 'תיאור חדש'
    db.session.commit()

    updated_location = Location.query.get(location.id)
    assert updated_location.name == 'מדף A1 חדש'
    assert updated_location.description == 'תיאור חדש' 