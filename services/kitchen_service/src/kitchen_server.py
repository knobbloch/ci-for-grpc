from concurrent import futures
import grpc
from generated import kitchen_pb2, kitchen_pb2_grpc

class KitchenOrderServiceServicer(kitchen_pb2_grpc.KitchenOrderServiceServicer):
    def CreateKitchenTasks(self, request, context):
        task_ids = [f"task_{request.order_id}_{item.dish_id}" for item in request.items]
        return kitchen_pb2.CreateKitchenTasksResponse(
            task_ids=task_ids,
            status="accepted"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kitchen_pb2_grpc.add_KitchenOrderServiceServicer_to_server(KitchenOrderServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Kitchen Service listening on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
