from models.order import Order, OrderItem
from models.payment import Payment
from repositories.order_repo import create_order_in_db, get_order_from_db, update_order_in_db
from repositories.payment_repo import create_payment_in_db, get_payment_from_db, update_payment_in_db

def create_order_with_payment(customer_id: str, items: list, delivery_address: str, amount: float, payment_method: str):
    """
    Создает заказ и сразу оплачивает его.
    """
    order_items = [OrderItem(**item) for item in items]
    total_price = sum(item.quantity * 100 for item in order_items)
    order_id = f"order_{len(order_items)}"
    order = Order(order_id, customer_id, order_items, delivery_address, total_price)
    create_order_in_db(order)
    
    payment_id = f"payment_{len(order_items)}"
    payment = Payment(payment_id, order_id, amount, payment_method, status="completed")
    create_payment_in_db(payment)
    
    order.status = "paid"
    update_order_in_db(order)
    
    return order, payment


def pay_existing_order(order_id: str, amount: float, payment_method: str):
    """
    Оплачивает уже существующий заказ.
    """
    order = get_order_from_db(order_id)
    if not order:
        raise ValueError("Order not found")
    if order.status == "paid":
        raise ValueError("Order already paid")
    if amount < order.total_price:
        raise ValueError("Insufficient amount")
    
    payment_id = f"payment_{len(order.items)}"
    payment = Payment(payment_id, order_id, amount, payment_method, status="completed")
    create_payment_in_db(payment)
    
    order.status = "paid"
    update_order_in_db(order)
    
    return payment


def refund_order_payment(payment_id: str):
    """
    Возврат оплаты и возврат заказа в статус 'created'.
    """
    payment = get_payment_from_db(payment_id)
    if not payment:
        raise ValueError("Payment not found")
    if payment.status != "completed":
        raise ValueError("Payment cannot be refunded")
    
    payment.status = "refunded"
    update_payment_in_db(payment)
    
    order = get_order_from_db(payment.order_id)
    if order:
        order.status = "created"
        update_order_in_db(order)
    
    return payment
