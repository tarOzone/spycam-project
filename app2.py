import os
import RPi.GPIO as GPIO
from time import time
from camera2 import camera
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
pir_gpio_pin: int = int(os.getenv('PIR_GPIO_PIN'))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir_gpio_pin, GPIO.IN)


def capture_and_upload():
    for _ in range(10):
        camera.capture()
        camera.upload_image()


def callback(channel):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:", "Intruders found\a")
    start = time()
    capture_and_upload()
    print(f"uploading done in {time() - start}")


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

