#!/usr/bin/env python3
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import logging

app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.INFO)


@app.route("/api/add/<int:a>/<int:b>", methods=["GET", "POST"])
def add(a, b):
    response = {"sum": str(a + b)}
    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/rawimage", methods=["POST"])
def rawimage():
    try:
        img = Image.open(io.BytesIO(request.data))
        response = {"width": img.size[0], "height": img.size[1]}
    except Exception as e:
        response = {"width": 0, "height": 0, "error": str(e)}

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/dotproduct", methods=["POST"])
def dotproduct():
    try:
        data = request.get_json(force=True)
        a = data.get("a", [])
        b = data.get("b", [])
        result = sum(x * y for x, y in zip(a, b))
        response = {"dotproduct": result}
    except Exception as e:
        response = {"dotproduct": 0, "error": str(e)}

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/jsonimage", methods=["POST"])
def jsonimage():
    try:
        data = request.get_json(force=True)
        img_b64 = data.get("image", "")
        img_bytes = base64.b64decode(img_b64)
        img = Image.open(io.BytesIO(img_bytes))
        response = {"width": img.size[0], "height": img.size[1]}
    except Exception as e:
        response = {"width": 0, "height": 0, "error": str(e)}

    return Response(
        response=jsonpickle.encode(response),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
