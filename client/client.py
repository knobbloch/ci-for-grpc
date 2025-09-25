import grpc
from generated import order_pb2, order_pb2_grpc
from generated import kitchen_pb2, kitchen_pb2_grpc

def run():
    # ===== OrderService =====
    order_channel = grpc.insecure_channel('localhost:50051')
    order_stub = order_pb2_grpc.OrderServiceStub(order_channel)

    create_order_request = order_pb2.CreateOrderRequest(
        customer_id="12345",
        items=[
            order_pb2.OrderItem(dish_id="dish_1", quantity=2),
            order_pb2.OrderItem(dish_id="dish_2", quantity=1),
        ],
        delivery_address="123 Main Street",
        total_price=29.99
    )

    create_order_response = order_stub.CreateOrder(create_order_request)
    print("Order created:", create_order_response.order_id, create_order_response.status)

    order_id = create_order_response.order_id

    status_request = order_pb2.GetOrderStatusRequest(order_id=order_id)
    status_response = order_stub.GetOrderStatus(status_request)
    print("Order status:", status_response.status)

    # ===== KitchenService =====
    kitchen_channel = grpc.insecure_channel('localhost:50052')
    kitchen_stub = kitchen_pb2_grpc.KitchenServiceStub(kitchen_channel)

    kitchen_request = kitchen_pb2.KitchenOrderRequest(
        order_id=order_id,
        items=[
            kitchen_pb2.KitchenOrderItem(dish_id="dish_1", quantity=2),
            kitchen_pb2.KitchenOrderItem(dish_id="dish_2", quantity=1),
        ]
    )

    kitchen_response = kitchen_stub.ProcessOrder(kitchen_request)
    print("Kitchen task:", kitchen_response.task_id, kitchen_response.status)

    task_status_request = kitchen_pb2.KitchenTaskStatusRequest(task_id=kitchen_response.task_id)
    task_status_response = kitchen_stub.GetTaskStatus(task_status_request)
    print("Kitchen task status:", task_status_response.status)

if __name__ == "__main__":
    run()
