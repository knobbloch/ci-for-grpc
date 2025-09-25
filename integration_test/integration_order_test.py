import grpc
import pytest
from generated.order_pb2 import KitchenTaskStatus
from generated.order_pb2_grpc import OrderUpdateServiceStub

@pytest.fixture
def sample_task_status():
    return {
        "order_id": "order_123",
        "task_id": "task_1",
        "dish_id": "dish_1",
        "status": "done",
        "message": "Dish prepared"
    }

def test_update_order_status(sample_task_status):
    channel = grpc.insecure_channel("localhost:50052")
    client = OrderUpdateServiceStub(channel)

    task_status = KitchenTaskStatus(
        order_id=sample_task_status["order_id"],
        task_id=sample_task_status["task_id"],
        dish_id=sample_task_status["dish_id"],
        status=sample_task_status["status"],
        message=sample_task_status["message"]
    )

    response = client.UpdateOrderStatus(task_status)

    assert response.status == "done"
    assert response.order_id == sample_task_status["order_id"]
