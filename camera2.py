import io
from PIL import Image
from camera import CameraCapture


class CameraCapture2(CameraCapture):
    
    def capture(self) -> bytes:
        output: io.BytesIO = io.BytesIO()
        self.camera.capture(self.buffer, 'rgb')
        image = Image.fromarray(self.buffer)
        image.save(output, format="JPEG")
        return bytes(output.getbuffer())

    def upload_image(self, content: bytes) -> dict:
        filename: str = CameraCapture._get_filename()
        id_token: str = self._user['idToken']
        return self._storage.child(filename).put(content, id_token)
