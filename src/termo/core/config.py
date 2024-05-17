from pathlib import Path
from appdirs import user_data_dir, user_config_dir
from termo import __name__

DATA_DIR = Path(user_data_dir(__name__))
CONFIG_DIR = Path(user_config_dir(__name__))