#!/bin/bash

GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

THEME="$1"
THEME_DIR="$XDG_CONFIG_HOME/colorschemes/$THEME"
CURRENT_DIR=$(pwd)

if [ -z "$THEME" ]; then
  echo -e "${YELLOW}Usage: $0 <theme-name>${NC}"
  exit 1
fi

if [ ! -d "$THEME_DIR" ]; then
  echo -e "${YELLOW}Theme '$THEME' does not exist at $THEME_DIR${NC}"
  notify-send "Theme Error" "Theme '$THEME' not found" -u critical
  exit 1
fi

# Vicinae theme
echo -e "${CYAN}-> Applying Vicinae theme...${NC}"
vicinae theme set $THEME
echo ""

# Hyprland config
echo -e "${CYAN}-> Updating Hyprland configuration...${NC}"
cp "$THEME_DIR/hypr/colorscheme.conf" "$DOTFILES/hypr/.config/hypr/colorscheme.conf" >/dev/null 2>&1
cd "$DOTFILES" && stow hypr
echo ""

# Waybar & SwayNC
echo -e "${CYAN}-> Applying Waybar and SwayNC theme...${NC}"
cp "$THEME_DIR/waybar/colorscheme.css" "$DOTFILES/waybar/.config/waybar/colorscheme.css" >/dev/null 2>&1
cd "$DOTFILES" && stow waybar
cp "$THEME_DIR/swaync/colorscheme.css" "$DOTFILES/swaync/.config/swaync/colorscheme.css" >/dev/null 2>&1
cd "$DOTFILES" && stow swaync
echo -e "${CYAN}-> Restarting Waybar and SwayNC...${NC}"
~/.config/waybar/scripts/launch.sh > /dev/null 2>&1 & disown
echo ""

# GTK Theme
if [ -f "$THEME_DIR/gtk-theme" ]; then
  GTK_THEME_NAME=$(cat "$THEME_DIR/gtk-theme")
  echo -e "${CYAN}-> Setting GTK theme to '$GTK_THEME_NAME'...${NC}"
  gsettings set org.gnome.desktop.interface gtk-theme "$GTK_THEME_NAME" >/dev/null 2>&1
else
  echo -e "${YELLOW}-> GTK theme file not found. Skipping.${NC}"
fi
echo ""

GTK4_SRC="$THEME_DIR/gtk-4.0"
GTK4_DST="$XDG_CONFIG_HOME/gtk-4.0"

if [[ -d "$GTK4_SRC" ]]; then
  echo -e "${CYAN}-> Linking GTK4 theme files...${NC}"
  mkdir -p "$GTK4_DST"
  ln -sf "$GTK4_SRC/gtk.css" "$GTK4_DST/gtk.css"
  ln -sf "$GTK4_SRC/gtk-dark.css" "$GTK4_DST/gtk-dark.css"
  ln -sfn "$GTK4_SRC/assets" "$GTK4_DST/assets"
else
  echo -e "${YELLOW}-> No GTK4 theme files found in $GTK4_SRC. Skipping.${NC}"
fi
echo ""

# Terminal theme
case $TERMINAL in
wezterm)
  echo -e "${CYAN}-> Applying terminal theme...${NC}"
  cp "$THEME_DIR/wezterm/colorscheme.lua" "$DOTFILES/wezterm/.config/wezterm/colorscheme.lua" >/dev/null 2>&1
  cd "$DOTFILES" && stow wezterm
  # pgrep wezterm | xargs -r kill -SIGUSR1 >/dev/null 2>&1
  echo ""
  ;;
ghostty)
  echo -e "${CYAN}-> Applying terminal theme...${NC}"
  cp "$THEME_DIR/ghostty/colorscheme" "$DOTFILES/ghostty/.config/ghostty/colorscheme" >/dev/null 2>&1
  cd "$DOTFILES" && stow wezterm
  # pgrep ghostty | xargs -r kill -SIGUSR1 >/dev/null 2>&1
  echo ""
  ;;
*)
  echo ""
  ;;
esac

# Neovim theme
echo -e "${CYAN}-> Applying Neovim theme...${NC}"
cp "$THEME_DIR/nvim/lua/plugins/colorscheme.lua" "$XDG_CONFIG_HOME/nvim/lua/plugins/colorscheme.lua" >/dev/null 2>&1
echo -e "${CYAN}-> Theme will auto-reload in Neovim (within 2 seconds)${NC}"
echo ""

# Zathura theme
echo -e "${CYAN}-> Applying Zathura theme...${NC}"
cp "$THEME_DIR/zathura/colorscheme" "$DOTFILES/zathura/.config/zathura/colorscheme" >/dev/null 2>&1
cd "$DOTFILES" && stow zathura
echo ""

# FZF theme
echo -e "${CYAN}-> Applying FZF theme...${NC}"
cp "$THEME_DIR/zsh/colorscheme.zsh" "$DOTFILES/zsh/.config/zsh/colorscheme.zsh" >/dev/null 2>&1
cd "$DOTFILES" && stow zsh
echo -e "${CYAN}-> Sourcing .zshrc...${NC}"
source "$HOME/.config/zsh/.zshrc"
echo ""

# Git Delta theme
echo -e "${CYAN}-> Applying Git Delta theme...${NC}"
cp "$THEME_DIR/git/colorscheme" "$DOTFILES/git/.config/git/colorscheme" >/dev/null 2>&1
cd "$DOTFILES" && stow git
echo ""

# Final success notification
cd "$CURRENT_DIR"
notify-send "Theme Applied" "Successfully switched to: $THEME" -t 5000
