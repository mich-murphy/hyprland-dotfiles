#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import unittest
from enum import Enum
from pathlib import Path


class Theme(Enum):
    """Allowed themes for which configuration files exist."""

    tokyonight_night = {
        "general": "tokyonight-night",
        "gtk": "TokyoNight-Dark",
    }
    carbonfox = {
        "general": "carbonfox",
        "gtk": "Nightfox-Dark",
    }

    @classmethod
    def instantiate(cls, theme):
        return cls(theme)


parser = argparse.ArgumentParser(
    prog="Theme Switcher",
    description="Manages switching of user specified system themes",
)
parser.add_argument("theme", choices=[theme.value["general"] for theme in Theme])
parser.add_argument("-t", "--theme-folder", default="colorschemes")
parser.add_argument("-c", "--config-path", default=os.environ["XDG_CONFIG_HOME"])
parser.add_argument("-d", "--dotfiles-path", default=os.environ["DOTFILES"])
args = parser.parse_args()


def validate_path(path: str) -> Path:
    """Confirm specified paths exist on file system."""
    if not os.path.exists(path):
        raise ValueError(f"Directory does not exist at: {path}")
    return Path(path)


THEME = args.theme
CONFIG_PATH = validate_path(args.config_path)
DOTFILES_PATH = validate_path(args.dotfiles_path)
THEME_PATH = validate_path(f"{CONFIG_PATH}/{args.theme_folder}/{THEME}")
WORKING_DIRECTORY = os.getcwd()


class Application(Enum):
    """Allowed applications along with specification of theme files."""

    hyprland = {
        "name": "hypr",
        "source": f"{THEME_PATH}/hypr/colorscheme.rasi",
        "target": f"{DOTFILES_PATH}/hypr/.config/hypr/colorscheme.conf",
        "stow": True,
    }
    waybar = {
        "name": "waybar",
        "source": f"{THEME_PATH}/waybar/colorscheme.css",
        "target": f"{DOTFILES_PATH}/waybar/.config/waybar/colorscheme.css",
        "stow": True,
    }
    swaync = {
        "name": "swaync",
        "source": f"{THEME_PATH}/swaync/colorscheme.css",
        "target": f"{DOTFILES_PATH}/swaync/.config/swaync/colorscheme.css",
        "stow": True,
    }
    wezterm = {
        "name": "wezterm",
        "source": f"{THEME_PATH}/wezterm/colorscheme.lua",
        "target": f"{DOTFILES_PATH}/wezterm/.config/wezterm/colorscheme.lua",
        "stow": True,
    }
    zathura = {
        "name": "zathura",
        "source": f"{THEME_PATH}/zathura/colorscheme",
        "target": f"{DOTFILES_PATH}/zathura/.config/zathura/colorscheme",
        "stow": True,
    }
    git = {
        "name": "git",
        "source": f"{THEME_PATH}/git/colorscheme",
        "target": f"{DOTFILES_PATH}/git/.config/git/colorscheme",
        "stow": True,
    }
    zsh = {
        "name": "zsh",
        "source": f"{THEME_PATH}/zsh/colorscheme.zsh",
        "target": f"{DOTFILES_PATH}/zsh/.config/zsh/colorscheme.zsh",
        "stow": True,
    }
    neovim = {
        "name": "nvim",
        "source": f"{THEME_PATH}/nvim/lua/plugins/colorscheme.lua",
        "target": f"{CONFIG_PATH}/nvim/lua/plugins/colorscheme.lua",
        "stow": False,
    }


def apply_theme_file(application: Application) -> int:
    """Copy application files to set the specified theme from argparse command."""
    source = validate_path(application.value["source"])
    target = application.value["target"]
    stow_required = application.value["stow"]
    print(f"Copying {application.name.title()} theme file...\n")
    shutil.copyfile(source, target)
    if stow_required:
        os.chdir(DOTFILES_PATH)
        stow = subprocess.run(["stow", application.value["name"]])
        if stow.returncode != 0:
            return stow.returncode
    return 0


def apply_gtk_theme(theme: Theme) -> int:
    """Set matching GTK theme for specified theme."""
    print(f"Setting GTK theme to {theme.value['gtk']}...")
    gsettings = subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.interface",
            "gtk-theme",
            theme.value["gtk"],
        ]
    )
    if gsettings.returncode != 0:
        return gsettings.returncode
    source = validate_path(f"{THEME_PATH}/gtk-4.0")
    target = f"{CONFIG_PATH}/gtk-4.0"
    print(f"Linking GTK theme files for {theme.value['gtk']}...")
    os.makedirs(target, exist_ok=True)
    os.symlink(f"{source}/gtk.css", f"{target}/gtk.css")
    os.symlink(f"{source}/gtk-dark.css", f"{target}/gtk-dark.css")
    os.symlink(f"{source}/assets", f"{target}/assets", target_is_directory=True)
    return 0


def reload_applications() -> int:
    """Reload applications to apply the new theme files."""
    print("Reloading Zsh config...\n")
    source_zsh = subprocess.run(["source", f"{CONFIG_PATH}/zsh/.zshrc"])
    if source_zsh != 0:
        return source_zsh.returncode
    print("Restarting Waybar and SwayNC...\n")
    restart_waybar = subprocess.run(["killall", "-9", "waybar", "&&", "waybar", "&"])
    restart_swaync = subprocess.run(["killall", "-9", "swaync", "&&", "swaync", "&"])
    if restart_swaync.returncode != 0 or restart_waybar.returncode != 0:
        return restart_waybar.returncode + restart_swaync.returncode
    return 0


def main():
    try:
        success = []
        failure = []
        # Apply vicinae theme - can be set via command line
        vicinae = subprocess.run(["vicinae", "theme", "set", THEME])
        if vicinae.returncode == 0:
            success.append("vicinae")
        else:
            failure.append("vicinae")
        # Apply all remaining applicaiton themes following same pattern
        for application in Application:
            result = apply_theme_file(application)
            if result == 0:
                success.append(application.name)
            else:
                failure.append(application.name)
        # Apply GTK theme - follows it's own steps
        gtk_theme = Theme.instantiate(THEME)
        if apply_gtk_theme(gtk_theme) == 0:
            success.append("gtk")
        else:
            failure.append("gtk")
        # Handle reporting of status
        if len(success) > 0:
            print("The following applications had theme successfully applied: \n")
            for app in success:
                print(f"{app} \n")
        if len(failure) > 0:
            print(
                "The following applications had errors during their theme being applied: \n"
            )
            for app in failure:
                print(f"{app} \n")
        # Handle reloading of applications all at the same time
        reload = reload_applications()
        if reload != 0:
            print(f"Reloading applications failed with exit code: {reload}")
    finally:
        os.chdir(WORKING_DIRECTORY)


if __name__ == "__main__":

    class TestThemeSwitcher(unittest.TestCase):
        def test_validate_path(self):
            expected = Path("/tmp")
            result = validate_path("/tmp")
            self.assertEqual(expected, result)
            with self.assertRaises(ValueError):
                validate_path("fake-theme-dir")

    unittest.main()
