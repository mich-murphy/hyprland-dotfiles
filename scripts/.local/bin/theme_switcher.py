#!/usr/bin/env python

import argparse
import os
import subprocess
import tempfile
from enum import Enum
from pathlib import Path

import pytest


class Themes(Enum):
    tokyonight_night = "tokyonight-night"
    carbonfox = "carbonfox"


parser = argparse.ArgumentParser(
    prog="Theme Switcher",
    description="Manages switching of user specified system themes",
)
parser.add_argument("theme", choices=[theme.value for theme in Themes])
parser.add_argument("-t", "--theme-folder", default="colorschemes")
parser.add_argument("-c", "--config-path", default=os.environ["XDG_CONFIG_HOME"])
parser.add_argument("-d", "--data-path", default=os.environ["XDG_DATA_HOME"])
args = parser.parse_args()
theme = args.theme
theme_folder = args.theme_folder
config_path = args.config_path
data_path = args.data_path
working_directory = os.getcwd()


def validate_path_exists(path: str) -> Path:
    """Confirm user provided paths exist on file system."""
    if not os.path.exists(path):
        raise ValueError(f"Directory does not exist at: {path}")
    return Path(path)


CONFIG_PATH = validate_path_exists(config_path)
DATA_PATH = validate_path_exists(data_path)
THEME_PATH = validate_path_exists(f"{CONFIG_PATH}/{theme_folder}/{theme}")


def apply_rofi_theme(
    rofi_source: str = f"{THEME_PATH}/rofi/theme.rasi",
    rofi_target: str = f"{DATA_PATH}/rofi/theme.rasi",
):
    """Copy rofi config to set specified theme."""
    print("Applying Rofi theme...\n")
    valid_rofi_source = validate_path_exists(rofi_source)
    command = subprocess.run(["cp", valid_rofi_source, rofi_target])
    return command.returncode


if __name__ == "__main__":

    def test_validate_theme_path_invalid_folder():
        theme_folder = "fake-theme-dir"
        with pytest.raises(ValueError):
            validate_path_exists(theme_folder)

    def test_apply_rofi_theme():
        with tempfile.NamedTemporaryFile() as temp_rofi_source:
            with tempfile.TemporaryDirectory() as temp_rofi_target_dir:
                result = apply_rofi_theme(
                    f"{temp_rofi_source.name}",
                    f"{temp_rofi_target_dir}/{os.path.basename(temp_rofi_source.name)}",
                )
                assert result == 0

    test_validate_theme_path_invalid_folder()
    test_apply_rofi_theme()
