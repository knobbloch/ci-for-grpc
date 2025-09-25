from models.order import Order
from db.mock_db import db

def create_order_in_db(order: Order) -> Order:
    db.orders[order.order_id] = order
    return order

def get_order_from_db(order_id: str) -> Order:
    return db.orders.get(order_id)

def update_order_in_db(order: Order) -> Order:
    db.orders[order.order_id] = order
    return order

def delete_order_from_db(order_id: str) -> bool:
    return db.orders.pop(order_id, None) is not None
