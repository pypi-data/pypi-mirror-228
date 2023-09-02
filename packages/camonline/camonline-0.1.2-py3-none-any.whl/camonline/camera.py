import threading

import cv2 as cv

from camonline.log import logger


class CameraManager:
    _cache = {}
    _mutex = threading.Lock()

    @classmethod
    def get_or_create(cls, index):
        if index not in cls._cache:
            with cls._mutex:
                if index not in cls._cache:
                    cls._cache[index] = Camera(index)
        return cls._cache[index]


class Camera:
    def __init__(self, index) -> None:
        self.cap = cv.VideoCapture(index)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        logger.info(f"Camera fps is {self.fps}")
        self.resolution = (
            int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
        )
        logger.info(f"Camera resolution is {self.resolution}")

        self.callbacks = []

    def _read_fream(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def poll(self):
        frame = self._read_fream()
        if frame is None:
            return
        for callback in self.callbacks:
            callback(frame)

    def shutdown(self):
        self.cap.release()


if __name__ == "__main__":
    index = 4
    c = Camera(index)

    def show_frame(frame):
        cv.imshow("frame", frame)
        cv.waitKey(1)

    c.add_callback(show_frame)

    while True:
        c.poll()
