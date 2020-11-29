import cv2
import numpy as np


def generate_random_image(width: int = 1920, height: int = 1080, ext: str = ".jpg") -> bytes:
    image = np.random.rand(height, width, 3) * 255
    ret, image = cv2.imencode(ext, image)
    image = image.tobytes()
    return image
