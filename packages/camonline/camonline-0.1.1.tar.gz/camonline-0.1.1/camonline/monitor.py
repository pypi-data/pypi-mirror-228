import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union

import cv2 as cv

from camonline.camera import Camera, CameraManager
from camonline.config import Config, Configuable
from camonline.log import logger


class RotateMonitor(Configuable):
    default_config = {
        "camera": {
            "device": 0,
            "resolution": [640, 480],
            "fps": 30.0,
        },
        "storage": {
            "record_dir": "~/.camonline/storage",
            "fourcc": "PIM1",
            "suffix": ".mkv",
            "days": 30,
        },
    }

    def __init__(self, config: Optional[Union[Config, Dict[str, Any]]] = None, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.camera: Camera = CameraManager.get_or_create(self.config.camera.device)
        self.record_dir.mkdir(parents=True, exist_ok=True)
        self.start_day = datetime.now().strftime("%Y-%m-%d")
        self.shutdown_event = threading.Event()

        self._attatch_func = None
        self._shutdown_callback = None
        self._thread = None
        self._rotate_thread = None

    @property
    def record_dir(self) -> Path:
        return Path(self.config.storage.record_dir).expanduser().absolute()

    @property
    def current_record_file(self) -> Path:
        today = datetime.now().strftime("%Y-%m-%d")
        return (self.record_dir / today).with_suffix(self.config.storage.suffix).as_posix()

    def attatch(self):
        fourcc = cv.VideoWriter_fourcc(*self.config.storage.fourcc)
        out = cv.VideoWriter(
            self.current_record_file,
            fourcc,
            self.config.camera.fps,
            self.config.camera.resolution,
        )

        def _(frame):
            logger.debug(frame)
            out.write(frame)

        logger.info(f"Attatch to {self.current_record_file}")
        self._attatch_func = _
        self.camera.add_callback(_)

        def _close():
            out.release()

        self._shutdown_callback = _close

    def reattatch(self):
        logger.info("Reattatch triggerd")
        if self._attatch_func:
            self.camera.remove_callback(self._attatch_func)
        if self._shutdown_callback:
            self._shutdown_callback()
        self.attatch()

    def start(self):
        self.shutdown_event.clear()
        self.attatch()

        def _():
            while not self.shutdown_event.is_set():
                self.camera.poll()
                self.shutdown_event.wait(1 / self.config.camera.fps)

        def _rotate():
            while not self.shutdown_event.is_set():
                today = datetime.now().strftime("%Y-%m-%d")
                if today != self.start_day:
                    self.reattatch()
                    self.start_day = today
                    to_remove_day = (
                        datetime.now() - timedelta(days=self.config.storage.days)
                    ).strftime("%Y-%m-%d")
                    logger.info(
                        f"Delete {self.config.storage.days} days before record:{to_remove_day}"
                    )
                    (self.record_dir / to_remove_day).with_suffix(
                        self.config.storage.suffix
                    ).unlink(missing_ok=True)

                self.shutdown_event.wait(1)

        self._thread = threading.Thread(target=_)
        self._thread.start()

        self._rotate_thread = threading.Thread(target=_rotate)
        self._rotate_thread.start()

    def shutdown(self):
        self.shutdown_event.set()
        self._thread.join()
        self._rotate_thread.join()

        self.camera.remove_callback(self._attatch_func)

        self._shutdown_callback()
        self._shutdown_callback = None

        self._attatch_func = None
        self._thread = None
        self._rotate_thread = None


if __name__ == "__main__":
    from pathlib import Path

    from camonline.config import ConfigLoader

    _HERE = Path(__file__).parent
    config_loader = ConfigLoader(_HERE / "static" / "config.toml")

    monitor = RotateMonitor(config_loader.load_config())
    monitor.start()
    input()
    monitor.shutdown()
