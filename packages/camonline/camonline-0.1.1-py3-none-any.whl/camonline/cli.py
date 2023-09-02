import signal

import click

from camonline.config import CONFIG_PATH, ConfigLoader
from camonline.log import logger
from camonline.monitor import RotateMonitor


@click.command()
@click.option("--config", default=CONFIG_PATH, help=f"Config file path, default: {CONFIG_PATH}")
def start(config):
    config = ConfigLoader(config).load_config()
    m = RotateMonitor(config)
    m.start()

    def _shutdown(sig=None, frame=None):
        logger.info("Exiting...")
        m.shutdown()
        m.camera.shutdown()
        exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)
    logger.info("Waiting for KeyboardInterrupt or SIGTERM...")
    while True:
        signal.pause()


@click.group()
def cli():
    pass


cli.add_command(start)


if __name__ == "__main__":
    cli(["start"])
