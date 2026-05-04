import cv2
from fastapi import Response
import numpy as np
import base64


def read_image(file_bytes):
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return Response(status_code=500, content={"message": "Img is invalid!"})

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0


def encode_image_base64(img: np.ndarray):
    img = (img * 255).astype(np.uint8)
    _, buffer = cv2.imencode(".jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    return base64.b64encode(buffer.tobytes()).decode("utf-8")


if __name__ == "__main__":
    print("The image_utils.py file is compiled and run successfully")
