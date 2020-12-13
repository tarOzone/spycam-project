import io
from PIL import Image
from camera import CameraCapture


class CameraCapture2(CameraCapture):

    def __init__(self):
        super().__init__()
        self.output: bytes = None

    def capture(self):
        self.camera.capture(self.buffer, 'rgb')
        output = io.BytesIO()
        image = Image.fromarray(self.buffer)
        image.save(output, format="JPEG")
        self.output = bytes(self.output.getbuffer())

    def upload_image(self) -> dict:
        filename: str = CameraCapture._get_filename()
        id_token: str = self._user['idToken']
        return self._storage.child(filename).put(self.output, id_token)


# instantiate here
camera: CameraCapture2 = CameraCapture2()


def run():
    camera.capture()
    camera.upload_image()


if __name__ == '__main__':
    run()
