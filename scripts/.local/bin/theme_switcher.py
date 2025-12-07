#!/usr/bin/env python

import argparse
import os
from enum import Enum
from pathlib import Path
from typing import Optional

import pytest


class Themes(Enum):
    tokyonight_night = "tokyonight-night"
    carbonfox = "carbonfox"


parser = argparse.ArgumentParser(
    prog="Theme Switcher",
    description="Manages switching of user specified system themes",
)
parser.add_argument("theme", choices=[theme.value for theme in Themes])
args = parser.parse_args()
theme = args.theme
working_directory = os.getcwd()


def validate_dirs(
    theme: str = theme,
    theme_dir: str = "colorschemes",
    config_dir: str = os.environ["XDG_CONFIG_HOME"],
) -> Optional[Path]:
    if not os.path.exists(config_dir):
        raise ValueError(f"Config directory does not exist at: {config_dir}")
    theme_dir = os.path.join(config_dir, theme_dir, theme)
    if not os.path.exists(theme_dir):
        raise ValueError(
            f"Colorscheme directory not found at: {config_dir}/colorschemes/{theme}"
        )
    return Path(theme_dir)


if __name__ == "__main__":

    def test_validate_dirs(theme: str = theme):
        expected = Path(f"/home/mm/.config/colorschemes/{theme}")
        result = validate_dirs(theme)
        assert result == expected

    @pytest.mark.parametrize(
        theme_dir, config_dir,
        [
            ("fake-theme-dir", os.environ["ZDG_CONFIG_HOME"]),
            ("colorschemes", "fake-config-dir"),
        ],
    )
    def test_validate_dirs_invalid_config_dir(theme: str = theme, theme_dir, config_dir):
        with pytest.raises(ValueError):
            validate_dirs(theme, config_dir="fake-config-dir")

    def test_validate_dirs_invalid_theme_dir(theme: str = theme):
        with pytest.raises(ValueError):
            validate_dirs(theme, theme_dir="fake-theme-dir")

    test_validate_dirs()
    test_validate_dirs_invalid_config_dir()
    test_validate_dirs_invalid_theme_dir()
