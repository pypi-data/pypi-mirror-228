"""
Functions to create a JSON file ready to used by HTML
"""

import typing as t

import yaml

DEFAULT_CONFIG_PATH = "./config.yaml"


def load_config(config_path: t.Optional[str] = None):
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    with open(config_path, "r", encoding="utf8") as config_file:
        return yaml.safe_load(config_file)
