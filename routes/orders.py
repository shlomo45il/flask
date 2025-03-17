from flask import Blueprint, render_template, request, jsonify, current_app
from models.order import Order
from models.product import Product
from models.inventory import InventoryTransaction
from datetime import datetime
from utils.auth import login_required

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/shortages')
@login_required
def shortages():
    """הצגת רשימת חוסרים בהזמנות"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    search = request.args.get('search')

    query = Order.query.filter(Order.has_shortages == True)

    if status:
        query = query.filter(Order.status == status)
    if date_from:
        query = query.filter(Order.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Order.created_at <= datetime.strptime(date_to, '%Y-%m-%d'))
    if search:
        query = query.filter(
            (Order.order_number.ilike(f'%{search}%')) |
            (Order.customer.has(name=search))
        )

    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )

    return render_template('orders/shortages.html',
                         orders=orders.items,
                         page=page,
                         total_pages=orders.pages,
                         status=status,
                         date_from=date_from,
                         date_to=date_to,
                         search=search)

@orders_bp.route('/shortage-detail/<int:order_id>')
@login_required
def shortage_detail(order_id):
    """הצגת פרטי חוסרים בהזמנה ספציפית"""
    order = Order.query.get_or_404(order_id)
    return render_template('orders/shortage_detail.html', order=order)

@orders_bp.route('/restock/<int:order_id>')
@login_required
def restock(order_id):
    """הצגת דף השלמת מלאי להזמנה"""
    order = Order.query.get_or_404(order_id)
    if order.status != 'waiting_for_restock':
        return jsonify({'error': 'ההזמנה אינה במצב המתאים להשלמת מלאי'}), 400
    return render_template('orders/restock.html', order=order)

@orders_bp.route('/api/orders/start-restock', methods=['POST'])
@login_required
def start_restock():
    """התחלת תהליך השלמת מלאי"""
    data = request.get_json()
    order_id = data.get('order_id')
    notes = data.get('notes')

    order = Order.query.get_or_404(order_id)
    if order.status != 'picking_completed':
        return jsonify({'error': 'ההזמנה אינה במצב המתאים להשלמת מלאי'}), 400

    order.status = 'waiting_for_restock'
    order.restock_started_at = datetime.utcnow()
    order.restock_notes = notes
    order.save()

    return jsonify({'message': 'תהליך השלמת המלאי הותחל בהצלחה'})

@orders_bp.route('/api/orders/complete-restock', methods=['POST'])
@login_required
def complete_restock():
    """השלמת תהליך השלמת מלאי"""
    data = request.get_json()
    order_id = data.get('order_id')
    items = data.get('items', {})

    order = Order.query.get_or_404(order_id)
    if order.status != 'waiting_for_restock':
        return jsonify({'error': 'ההזמנה אינה במצב המתאים להשלמת מלאי'}), 400

    try:
        for item_id, item_data in items.items():
            order_item = order.items.filter_by(id=item_id).first()
            if not order_item:
                continue

            quantity = item_data.get('quantity', 0)
            location = item_data.get('location')

            # עדכון כמות שנאספה
            order_item.picked_quantity += quantity
            order_item.restock_location = location

            # יצירת תנועת מלאי
            InventoryTransaction.create(
                product_id=order_item.product_id,
                location_id=location,
                quantity=quantity,
                transaction_type='restock',
                reference=f'Order {order.order_number}',
                notes=f'השלמת מלאי להזמנה {order.order_number}'
            )

        # בדיקה האם כל הפריטים הושלמו
        all_completed = all(
            item.picked_quantity >= item.requested_quantity
            for item in order.items
        )

        if all_completed:
            order.status = 'restock_completed'
            order.restock_completed_at = datetime.utcnow()

        order.save()
        return jsonify({'message': 'השלמת המלאי הושלמה בהצלחה'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500 