import cv2
import numpy as np


def encode_image(image):
    init8_image = np.uint8(image)
    enc = cv2.imencode('.png', init8_image)[1]
    data_encode = np.array(enc)
    buff_encode = data_encode.tobytes()
    return buff_encode


def decode_image(buffer):
    nparr = np.frombuffer(buffer, np.uint8)
    img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_decode
