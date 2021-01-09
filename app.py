import os
from time import time
import RPi.GPIO as GPIO
from camera_rapid import CameraCaptureRapid
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
pir_gpio_pin: int = int(os.getenv('PIR_GPIO_PIN'))
camera: CameraCaptureRapid = CameraCaptureRapid()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir_gpio_pin, GPIO.IN)


def capture_and_uploads(n: int):
    for _ in range(n):
        start = time()
        camera.upload()
        print(f"uploading done in {time() - start}")


def callback(_):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:", "Intruders found\a")
    capture_and_uploads(3)


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

