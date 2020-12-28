import io
import cv2
import numpy as np
from typing import List
from threading import Lock
from camera import CameraCapture
from concurrent.futures import ThreadPoolExecutor


def transform_image(image: np.ndarray) -> bytes:
    _, image_buffer = cv2.imencode(".jpg", image)
    return image_buffer.tobytes()


class CameraCapture2(CameraCapture):
    
    def __init__(self):
        super().__init__()
        self.lock: Lock = Lock()
        self.excecutor: ThreadPoolExecutor = ThreadPoolExecutor()
        self.camera.start_preview()

    def capture(self, sequences: int = 15) -> List[np.ndarray]:
        buffers: List[np.ndarray] = [CameraCapture2._get_buffer() for _ in range(sequences)]
        self.camera.capture_sequence(buffers, 'bgr', use_video_port=True)
        return buffers

    def upload(self, sequences: int = 15):
        images: List[np.ndarray] = self.capture(sequences)
        self.excecutor.map(self._upload, images)
    
    @staticmethod
    def _get_buffer() -> np.ndarray:
        return np.empty((CameraCapture.height, CameraCapture.width, 3), dtype=np.uint8)
    
    def _upload(self, image: np.ndarray):
        image_bytes: bytes = transform_image(image)
        self._upload_image_bytes_to_firebase_storage(image_bytes)

    def _upload_image_bytes_to_firebase_storage(self, image: bytes) -> dict:
        self.lock.acquire()
        try:
            filename: str = CameraCapture._get_filename()
        finally:
            self.lock.release()
        return self._storage.child(filename).put(image, self._user['idToken'])

    def close(self):
        self.excecutor.shutdown()
        self.camera.stop_preview()
        self.camera.close()
