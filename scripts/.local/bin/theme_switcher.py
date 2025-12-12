#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
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
        "source": f"{THEME_PATH}/hypr/colorscheme.conf",
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
    ghostty = {
        "name": "wezterm",
        "source": f"{THEME_PATH}/ghostty/colorscheme",
        "target": f"{DOTFILES_PATH}/ghostty/.config/ghostty/colorscheme",
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


def apply_theme_file(application: Application) -> None:
    """Copy application files to set the specified theme from argparse command."""
    source = validate_path(application.value["source"])
    target = application.value["target"]
    stow_required = application.value["stow"]
    shutil.copyfile(source, target)
    if stow_required:
        subprocess.run(
            ["stow", application.value["name"]], cwd=DOTFILES_PATH, check=True
        )


def apply_theme_gtk(theme: Theme) -> None:
    """Set matching GTK theme for specified theme."""
    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.interface",
            "gtk-theme",
            theme.value["gtk"],
        ],
        check=True,
    )
    source = validate_path(f"{THEME_PATH}/gtk-4.0")
    target = f"{CONFIG_PATH}/gtk-4.0"
    os.makedirs(target, exist_ok=True)
    subprocess.run(["ln", "-sf", f"{source}/gtk.css", f"{target}/gtk.css"], check=True)
    subprocess.run(
        ["ln", "-sf", f"{source}/gtk-dark.css", f"{target}/gtk-dark.css"], check=True
    )
    subprocess.run(["ln", "-sfn", f"{source}/assets", f"{target}/assets"], check=True)


def reload_applications() -> None:
    """Reload applications to apply the new theme files."""
    print("Restarting applications...")
    subprocess.run(
        ["killall", "-9", "waybar"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.Popen("waybar", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(
        ["killall", "-9", "swaync"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.Popen("swaync", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # pgrep_wezterm = subprocess.run(
    #     ["pgrep", "wezterm"],
    #     capture_output=True,
    # )
    # subprocess.run(["xargs", "-r", "kill", "-SIGUSR1"], input=pgrep_wezterm.stdout)
    # pgrep_ghostty = subprocess.run(
    #     ["pgrep", "ghostty"],
    #     capture_output=True,
    # )
    # subprocess.run(["xargs", "-r", "kill", "-SIGUSR1"], input=pgrep_ghostty.stdout)


def main():
    try:
        # Apply vicinae theme - can be set via command line
        subprocess.run(["vicinae", "theme", "set", THEME], check=True)
        # Apply all remaining applicaiton themes following same pattern
        for application in Application:
            apply_theme_file(application)
        # Apply GTK theme - follows it's own steps
        gtk_theme = Theme[THEME.replace("-", "_")]
        apply_theme_gtk(gtk_theme)
        # Handle reporting of status
        print(f"{'*' * 20}")
        print(f"Theme has been successfully switched to: {THEME}")
        print(f"{'*' * 20}")
        # Handle reloading of applications all at the same time
        reload_applications()
    finally:
        os.chdir(WORKING_DIRECTORY)


if __name__ == "__main__":
    main()
