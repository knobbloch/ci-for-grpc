from typing import List
from dataclasses import dataclass

@dataclass
class OrderItem:
    dish_id: str
    quantity: int

@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    delivery_address: str
    total_price: float
    status: str = "created"
