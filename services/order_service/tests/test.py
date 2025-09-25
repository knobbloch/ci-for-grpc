import pytest
from models.order import OrderItem
from src.business_logic import create_order_with_payment, refund_order_payment
from db.mock_db import db 

#проверки бизнес-логики

@pytest.fixture(autouse=True)
def clear_db():
    db.orders.clear()
    db.payments.clear()
    db._order_counter = 1
    db._payment_counter = 1
    yield

def test_create_order_with_payment():
    items = [{"dish_id": "dish_1", "quantity": 2}, {"dish_id": "dish_2", "quantity": 1}]
    customer_id = "cust_1"
    delivery_address = "123 Test St"
    amount = 300
    payment_method = "card"

    order, payment = create_order_with_payment(customer_id, items, delivery_address, amount, payment_method)

    assert order.order_id in db.orders
    assert payment.payment_id in db.payments
    assert order.status == "paid"
    assert payment.status == "completed"
    assert order.total_price == sum([i['quantity'] * 100 for i in items])


def test_refund_order_payment():
    items = [{"dish_id": "dish_1", "quantity": 1}]
    customer_id = "cust_2"
    delivery_address = "456 Test Ave"
    amount = 100
    payment_method = "cash"

    order, payment = create_order_with_payment(customer_id, items, delivery_address, amount, payment_method)

    refunded_payment = refund_order_payment(payment.payment_id)

    assert refunded_payment.status == "refunded"
    assert db.orders[order.order_id].status == "created"
