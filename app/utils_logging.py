# utils_logging.py
import logging.config
import yaml
import os
import shutil
from pathlib import Path

from utils import repo_absolute_path


def setup_logging(
        log_config_path=None,
        default_level=logging.INFO,
):
    """Setup logging configuration"""

    if log_config_path is None:
        log_config_path = os.path.join(
            repo_absolute_path(),
            'config',
            'logging.yaml',
        )

    # Set up logs folder
    logs_folder = os.path.join(str(repo_absolute_path()), 'logs')
    if os.path.exists(logs_folder):
        shutil.rmtree(logs_folder)
    Path(logs_folder).mkdir(parents=True, exist_ok=True)    

    # Config logger
    if os.path.exists(log_config_path):
        with open(log_config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def close_log_handlers():
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)