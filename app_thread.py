import os
import RPi.GPIO as GPIO
from time import time
from dotenv import load_dotenv
from camera_thread import CameraStream


load_dotenv()
pir_gpio_pin: int = int(os.getenv('PIR_GPIO_PIN'))
sleep_time: float = float(os.getenv('SLEEP_TIME'))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# setup GPIO pins
GPIO.setup(pir_gpio_pin, GPIO.IN)

# assign output to GPIO pins
# GPIO.output(pir_gpio_pin, False)


def read_pir_input() -> int:
    return GPIO.input(pir_gpio_pin)


def main():
    some_object: CameraStream = CameraStream()
    print("test started...")
    try:
        while True:
            if read_pir_input():
                some_object.start()
                while read_pir_input():
                    time.sleep(sleep_time)
            else:
                some_object.stop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("test ended...")


if __name__ == '__main__':
    main()
