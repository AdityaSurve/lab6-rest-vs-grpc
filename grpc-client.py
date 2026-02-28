import grpc
import sys
import time
import base64
import random
import lab6_pb2
import lab6_pb2_grpc

IMAGE_PATH = "Flatirons_Winter_Sunrise_edit_2.jpg"

def run(addr, cmd, reps):
    img_bytes = open(IMAGE_PATH, "rb").read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    channel = grpc.insecure_channel(addr)
    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    start = time.perf_counter()
    for _ in range(reps):
        if cmd == "add":
            stub.Add(lab6_pb2.AddMsg(a=5, b=10))
        elif cmd == "rawImage":
            stub.RawImage(lab6_pb2.RawImageMsg(img=img_bytes))
        elif cmd == "jsonImage":
            stub.JsonImage(lab6_pb2.JsonImageMsg(img=img_b64))
        elif cmd == "dotProduct":
            a = [random.random() for _ in range(100)]
            b = [random.random() for _ in range(100)]
            stub.DotProduct(lab6_pb2.DotProductMsg(a=a, b=b))
        else:
            raise SystemExit(f"Unknown command: {cmd}")

    delta_ms = ((time.perf_counter() - start) / reps) * 1000
    print(f"Took {delta_ms} ms per operation")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <server_ip:port> <cmd> <reps>")
        raise SystemExit(1)
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
