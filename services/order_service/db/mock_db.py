from typing import Dict
from models.order import Order
from models.payment import Payment

class MockDB:
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.payments: Dict[str, Payment] = {}
        self._order_counter = 1
        self._payment_counter = 1

    def next_order_id(self):
        oid = f"order_{self._order_counter}"
        self._order_counter += 1
        return oid

    def next_payment_id(self):
        pid = f"payment_{self._payment_counter}"
        self._payment_counter += 1
        return pid

db = MockDB()