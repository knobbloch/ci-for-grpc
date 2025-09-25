from dataclasses import dataclass
from typing import Dict

@dataclass
class Dish:
    dish_id: str
    name: str
    ingredients: Dict[str, int]  # ingredient_name -> required_amount

@dataclass
class Ingredient:
    name: str
    quantity: int

@dataclass
class KitchenTask:
    task_id: str
    order_id: str
    dish_id: str
    status: str = "pending"

@dataclass
class Cook:
    cook_id: str
    name: str
