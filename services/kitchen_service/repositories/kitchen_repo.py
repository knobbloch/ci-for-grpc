from db.mock_mongo import db
from models.kitchen_models import Dish, Ingredient, KitchenTask, Cook

# --- Dishes ---
def create_dish(dish: Dish):
    return db.dishes.insert_one(dish.__dict__)

def get_dish(dish_id: str):
    return db.dishes.find_one({"dish_id": dish_id})

# --- Ingredients ---
def create_ingredient(ingredient: Ingredient):
    return db.ingredients.insert_one(ingredient.__dict__)

def get_ingredient(name: str):
    return db.ingredients.find_one({"name": name})

def update_ingredient(name: str, quantity: int):
    return db.ingredients.update_one({"name": name}, {"$set": {"quantity": quantity}})

# --- Kitchen Tasks ---
def create_task(task: KitchenTask):
    return db.kitchen_tasks.insert_one(task.__dict__)

def get_task(task_id: str):
    return db.kitchen_tasks.find_one({"task_id": task_id})

def update_task(task_id: str, **kwargs):
    return db.kitchen_tasks.update_one({"task_id": task_id}, {"$set": kwargs})

def delete_task(task_id: str):
    return db.kitchen_tasks.delete_one({"task_id": task_id})

# --- Cooks ---
def create_cook(cook: Cook):
    return db.cooks.insert_one(cook.__dict__)

def get_cook(cook_id: str):
    return db.cooks.find_one({"cook_id": cook_id})
