import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def decode_image(file_bytes:bytes) -> np.ndarray:

    np_array = np.frombuffer(file_bytes,np.uint8)
    image = cv2.imdecode(np_array,cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not decode image.Make sure it is a valid image file")
    return image

def encode_image_to_bytes(image : np.ndarray,format : str = "JPEG") -> bytes:
    image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)

    buffer = BytesIO()

    pil_image.save(buffer,format = format,quality = 95)
    buffer.seek(0)

    return buffer.read()