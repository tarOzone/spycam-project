import os
import RPi.GPIO as GPIO
from time import time
from threading import Thread
from camera2 import CameraCapture2
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
pir_gpio_pin: int = int(os.getenv('PIR_GPIO_PIN'))
camera: CameraCapture2 = CameraCapture2()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir_gpio_pin, GPIO.IN)


def capture_and_uploads(n: int):
    for _ in range(n):
        start = time()
        content: bytes = camera.capture()
        Thread(target=camera.upload_image, args=(content,)).start()
        print(f"uploading done in {time() - start}")


def callback(channel):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:", "Intruders found\a")
    capture_and_uploads(10)


GPIO.add_event_detect(
    pir_gpio_pin, GPIO.RISING,
    callback=callback,
    bouncetime=300
)

try:
    print("test started...")
    while True:
        continue
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    camera.close()
    print("")
    print("test ended...")

