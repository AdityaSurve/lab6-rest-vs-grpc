#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import time
import sys
import base64
import random

IMAGE_PATH = "Flatirons_Winter_Sunrise_edit_2.jpg"


def doRawImage(addr, img_bytes, debug=False):
    headers = {"content-type": "image/png"}
    url = addr + "/api/rawimage"
    r = requests.post(url, data=img_bytes, headers=headers)
    if debug:
        print("Response:", r.json())


def doAdd(addr, debug=False):
    headers = {"content-type": "application/json"}
    url = addr + "/api/add/5/10"
    r = requests.post(url, headers=headers)
    if debug:
        print("Response:", r.json())


def doDotProduct(addr, debug=False):
    headers = {"content-type": "application/json"}
    url = addr + "/api/dotproduct"
    payload = {
        "a": [random.random() for _ in range(100)],
        "b": [random.random() for _ in range(100)],
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if debug:
        print("Response:", r.json())


def doJsonImage(addr, img_b64_str, debug=False):
    headers = {"content-type": "application/json"}
    url = addr + "/api/jsonimage"
    payload = {"image": img_b64_str}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if debug:
        print("Response:", r.json())


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <server_ip> <cmd> <reps>")
        print("where <cmd> is one of: add, rawImage, dotProduct, jsonImage")
        print("and <reps> is the integer number of repetitions for measurement")
        sys.exit(1)

    host = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])

    addr = f"http://{host}:5000"
    print(f"Running {reps} reps against {addr}")

    # Preload image once (so you measure network/RPC, not disk I/O)
    img_bytes = open(IMAGE_PATH, "rb").read()
    img_b64_str = base64.b64encode(img_bytes).decode("utf-8")

    start = time.perf_counter()
    for _ in range(reps):
        if cmd == "rawImage":
            doRawImage(addr, img_bytes)
        elif cmd == "add":
            doAdd(addr)
        elif cmd == "jsonImage":
            doJsonImage(addr, img_b64_str)
        elif cmd == "dotProduct":
            doDotProduct(addr)
        else:
            print("Unknown option:", cmd)
            sys.exit(1)

    delta_ms = ((time.perf_counter() - start) / reps) * 1000
    print(f"Took {delta_ms} ms per operation")


if __name__ == "__main__":
    main()
