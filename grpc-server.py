from concurrent import futures
import grpc
import lab6_pb2
import lab6_pb2_grpc
from PIL import Image
import io
import base64

import time

class Lab6ServiceServicer(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        return lab6_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        img = Image.open(io.BytesIO(request.img))
        return lab6_pb2.ImageReply(width=img.size[0], height=img.size[1])

    def JsonImage(self, request, context):
        img_bytes = base64.b64decode(request.img)
        img = Image.open(io.BytesIO(img_bytes))
        return lab6_pb2.ImageReply(width=img.size[0], height=img.size[1])

    def DotProduct(self, request, context):
        dot = sum(x*y for x, y in zip(request.a, request.b))
        return lab6_pb2.DotProductReply(dotproduct=dot)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6ServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
