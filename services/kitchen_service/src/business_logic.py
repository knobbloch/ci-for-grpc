from repositories import kitchen_repo
from models.kitchen_models import KitchenTask

def prepare_order(order_id: str, dish_ids: list):
    tasks = []
    for dish_id in dish_ids:
        dish = kitchen_repo.get_dish(dish_id)
        if not dish:
            raise ValueError(f"Dish {dish_id} not found")

        for ingredient_name, required in dish["ingredients"].items():
            ing = kitchen_repo.get_ingredient(ingredient_name)
            if not ing or ing["quantity"] < required:
                raise ValueError(f"Not enough {ingredient_name} for dish {dish_id}")

        for ingredient_name, required in dish["ingredients"].items():
            ing = kitchen_repo.get_ingredient(ingredient_name)
            kitchen_repo.update_ingredient(ingredient_name, ing["quantity"] - required)

        task_id = f"task_{order_id}_{dish_id}"
        task = KitchenTask(task_id=task_id, order_id=order_id, dish_id=dish_id)
        kitchen_repo.create_task(task)
        tasks.append(task)
    return tasks

def update_task_status(task_id: str, status: str):
    task = kitchen_repo.get_task(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    kitchen_repo.update_task(task_id, status=status)
    return task

def cancel_task(task_id: str):
    task = kitchen_repo.get_task(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")

    dish = kitchen_repo.get_dish(task["dish_id"])
    for ingredient_name, amount in dish["ingredients"].items():
        ing = kitchen_repo.get_ingredient(ingredient_name)
        kitchen_repo.update_ingredient(ingredient_name, ing["quantity"] + amount)

    kitchen_repo.update_task(task_id, status="cancelled")
    return kitchen_repo.get_task(task_id)
