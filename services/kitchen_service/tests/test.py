import pytest
from models.kitchen_models import Dish, Ingredient
from db.mock_mongo import db
from src import business_logic
from repositories import kitchen_repo

@pytest.fixture(autouse=True)
def clear_db():
    db.dishes._data.clear()
    db.ingredients._data.clear()
    db.kitchen_tasks._data.clear()
    db.cooks._data.clear()
    yield

# --- Тест 1: подготовка заказа ---
def test_prepare_order():
    kitchen_repo.create_dish(Dish(dish_id="dish_1", name="Pizza", ingredients={"cheese": 100, "dough": 200}))
    kitchen_repo.create_ingredient(Ingredient(name="cheese", quantity=500))
    kitchen_repo.create_ingredient(Ingredient(name="dough", quantity=1000))

    order_id = "order_1"
    dish_ids = ["dish_1"]

    tasks = business_logic.prepare_order(order_id, dish_ids)

    assert len(tasks) == 1
    task = tasks[0]
    assert task.order_id == order_id
    assert task.dish_id == "dish_1"
    assert task.status == "pending"

    cheese = kitchen_repo.get_ingredient("cheese")
    dough = kitchen_repo.get_ingredient("dough")
    assert cheese["quantity"] == 400  # 500 - 100
    assert dough["quantity"] == 800   # 1000 - 200

# --- Тест 2: отмена задачи ---
def test_cancel_task():
    # Подготовка данных
    kitchen_repo.create_dish(Dish(dish_id="dish_2", name="Salad", ingredients={"lettuce": 50, "tomato": 30}))
    kitchen_repo.create_ingredient(Ingredient(name="lettuce", quantity=200))
    kitchen_repo.create_ingredient(Ingredient(name="tomato", quantity=100))

    order_id = "order_2"
    dish_ids = ["dish_2"]
    tasks = business_logic.prepare_order(order_id, dish_ids)
    task = tasks[0]

    cancelled_task = business_logic.cancel_task(task.task_id)

    assert cancelled_task["status"] == "cancelled"

    lettuce = kitchen_repo.get_ingredient("lettuce")
    tomato = kitchen_repo.get_ingredient("tomato")
    assert lettuce["quantity"] == 200 
    assert tomato["quantity"] == 100
