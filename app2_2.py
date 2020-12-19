import os
from time import time
from threading import Thread
from datetime import datetime
from camera2 import CameraCapture2

from gpiozero import MotionSensor
from dotenv import load_dotenv


load_dotenv()
pir_gpio_pin: int = int(os.getenv('PIR_GPIO_PIN'))
camera: CameraCapture2 = CameraCapture2()


def capture_and_upload():
    start = time()

    content: bytes = camera.capture()
    Thread(target=camera.upload_image, args=(content,)).start()

    print(f"uploading done in {time() - start}")


def main():
    pir: MotionSensor = MotionSensor(4)
    print("test started...")
    try:
        while True:
            pir.wait_for_motion()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:", "Intruders found\a")
            capture_and_upload()
    except KeyboardInterrupt:
        pass
    finally:
        pir.close()
        camera.close()
        print("\ntest ended...")


if __name__ == "__main__":
    main()
