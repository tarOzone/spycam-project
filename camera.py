import os
import json

import pyrebase
import numpy as np

from PIL import Image
from typing import Union
from picamera import PiCamera
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


class CameraCapture:

    quality = int(os.getenv('QUALITY'))
    width, height = (int(os.getenv('RESOLUTION_WIDTH')), int(os.getenv('RESOLUTION_HEIGHT')))

    def __init__(self):
        self.camera: PiCamera = PiCamera()
        self.camera.resolution = (CameraCapture.width, CameraCapture.height)

        self._firebase = pyrebase.initialize_app(self._read_firebase_config())
        self._storage = self._firebase.storage()
        self._auth = self._firebase.auth()
        self._user = self._auth.sign_in_with_email_and_password(os.getenv('EMAIL'), os.getenv('PASSWORD'))

        self.buffer = np.empty((CameraCapture.height, CameraCapture.width, 3), dtype=np.uint8)
        self.output: bytes = None

    def capture(self, filename: str):
        self.camera.capture(self.buffer, 'rgb')
        image: Image = Image.fromarray(self.buffer)
        image.save(filename, optimize=True, quality=CameraCapture.quality)

    def close(self):
        self.camera.close()

    def upload_image(self, content: Union[str, bytes]) -> dict:
        filename: str = CameraCapture._get_filename()
        id_token: str = self._user['idToken']
        return self._storage.child(filename).put(content, id_token)

    def upload_database(self, content: Union[str, bytes]):
        ret: dict = self.upload_image(content)
        url: str = self._storage.child(f"/{ret['name']}").get_url(ret['downloadTokens'])
        data: dict = CameraCapture._get_data_format(url, ret['timeCreated'])
        date: str = datetime.now().strftime("%Y-%m-%d")
        time: str = datetime.now().strftime("%H:%M:%S")
        self._database.child(date).child(time).push(data, self._user['idToken'])

    def retrieve(self):
        for item in self._database.get().each():
            print(item.key(), ":", json.dumps(item.val(), indent=4))

    @staticmethod
    def get_filename(ext: str = 'jpg') -> str:
        return "data/" + CameraCapture._get_filename(ext)

    @staticmethod
    def _get_datetime_string() -> str:
        return datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

    @staticmethod
    def _read_firebase_config() -> dict:
        return json.loads(open("./secrets.json", "r").read())

    @staticmethod
    def _get_data_format(url: str, time_created: str, lat: float = 0., lng: float = 0.) -> dict:
        return {
            'imageUrl': url,
            'timeCreated': time_created,
            'coordinates': {
                'latitude': lat,
                'longitude': lng,
            },
        }

    @staticmethod
    def _get_filename(ext: str = 'jpg') -> str:
        return f'/saved-image_{CameraCapture._get_datetime_string()}.{ext}'


# instantiate here
camera: CameraCapture = CameraCapture()


def run():
    filename: str = camera.get_filename(ext='jpg')
    camera.capture(filename)
    camera.upload_image(content=filename)


if __name__ == '__main__':
    run()
