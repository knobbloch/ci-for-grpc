from dataclasses import dataclass

@dataclass
class Payment:
    payment_id: str
    order_id: str
    amount: float
    payment_method: str
    status: str = "pending"
