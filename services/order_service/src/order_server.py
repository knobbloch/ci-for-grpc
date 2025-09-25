from concurrent import futures
import grpc
from generated import order_pb2, order_pb2_grpc

class OrderUpdateServiceServicer(order_pb2_grpc.OrderUpdateServiceServicer):
    def UpdateOrderStatus(self, request, context):
        print(f"Received update for order {request.order_id}, task {request.task_id}, status {request.status}")
        
        return order_pb2.UpdateOrderResponse(
            order_id=request.order_id,
            status=request.status
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderUpdateServiceServicer_to_server(OrderUpdateServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Order Service listening on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
