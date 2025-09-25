from models.order import OrderItem, Order
from models.payment import Payment
from repositories import order_repo, payment_repo
from src.kitchen_client import KitchenClient

kitchen_client = KitchenClient(host="localhost", port=50051)

def create_order_and_send_to_kitchen(customer_id: str, items: list, delivery_address: str, amount: float, payment_method: str):
    """
    Создаёт заказ, оплачивает и отправляет на кухню через gRPC.
    """
    # --- 1. Создание заказа ---
    order_items = [OrderItem(**item) for item in items]
    total_price = sum(item.quantity * 100 for item in order_items)
    order_id = f"order_{len(order_items)}"
    order = Order(order_id, customer_id, order_items, delivery_address, total_price, status="created")
    order_repo.create_order_in_db(order)

    # --- 2. Оплата ---
    payment_id = f"payment_{len(order_items)}"
    payment = Payment(payment_id, order_id, amount, payment_method, status="completed")
    payment_repo.create_payment_in_db(payment)

    order.status = "paid"
    order_repo.update_order_in_db(order)

    # --- 3. Отправка на кухню ---
    dish_ids = [item.dish_id for item in order_items]
    kitchen_response = kitchen_client.create_kitchen_tasks(order_id, dish_ids, delivery_address)

    if kitchen_response.get("status") == "accepted":
        order.status = "in_kitchen"
    else:
        order.status = "kitchen_failed"
    
    order_repo.update_order_in_db(order)

    return order, payment, kitchen_response
