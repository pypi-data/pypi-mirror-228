import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["CAMONLINE_LOG_LEVEL"] = "DEBUG"

import importlib.metadata as importlib_metadata
import re
import sys
from pathlib import Path


def load_entry_point(distribution, group, name):
    dist_obj = importlib_metadata.distribution(distribution)
    eps = [ep for ep in dist_obj.entry_points if ep.group == group and ep.name == name]
    if not eps:
        raise ImportError("Entry point %r not found" % ((group, name),))
    return eps[0].load()


config_file = Path("./config.toml")

if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
    sys.argv.append("start")
    sys.argv.extend(["--config", config_file.resolve().as_posix()])
    sys.exit(load_entry_point("camonline", "console_scripts", "camonline")())
