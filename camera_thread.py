import numpy as np
from threading import Thread
from dotenv import load_dotenv


load_dotenv()


class CameraStream(object):
    def __init__(self):
        # initialize the camera and stream

        # initialize the frame and the stop flag
        self.frame = None
        self.stopped = False

    def start(self):
        Thread(target=self._update, args=()).start()
        return self

    def read(self) -> np.ndarray:
        return self.frame

    def stop(self):
        self.stopped = True

    def _update(self):
        for f in self.stream:
            self._read_array(f)
            if self.stopped:
                self._post_process()
                self._close()
                return

    def _read_array(self, f):
        self.frame = f.array

    def _post_process(self):
        pass

    def _close(self):
        pass
