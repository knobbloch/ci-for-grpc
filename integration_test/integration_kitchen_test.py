import grpc
import pytest

from generated.kitchen_pb2 import DishItem, Order as KitchenOrder
from generated.kitchen_pb2_grpc import KitchenOrderServiceStub

@pytest.fixture
def sample_order():
    return {
        "order_id": "order_123",
        "items": [
            {"dish_id": "dish_1", "quantity": 2},
            {"dish_id": "dish_2", "quantity": 1}
        ],
        "delivery_address": "123 Main Street"
    }

def test_create_kitchen_tasks(sample_order):
    # Подключаемся к реально работающему Kitchen Service
    channel = grpc.insecure_channel("localhost:50051")
    client = KitchenOrderServiceStub(channel)

    order_message = KitchenOrder(
        order_id=sample_order["order_id"],
        items=[DishItem(dish_id=i["dish_id"], quantity=i["quantity"]) for i in sample_order["items"]],
        delivery_address=sample_order["delivery_address"]
    )

    response = client.CreateKitchenTasks(order_message)

    assert response.status == "accepted"
    assert len(response.task_ids) == len(sample_order["items"])
