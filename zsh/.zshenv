# For dotfiles
export XDG_CONFIG_HOME="$HOME/.config"

# For specific data
export XDG_DATA_HOME="$HOME/.local/share"

# For cached files
export XDG_CACHE_HOME="$HOME/.cache"

# For cached files
export XDG_STATE_HOME="$HOME/.local/state"

# Default editor
export EDITOR="nvim"
export VISUAL="nvim"
export TERMINAL="wezterm"
export BROWSER="firefox"

# Zsh config files
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"

# History filepath
export HISTFILE="$XDG_STATE_HOME/zsh/history"
# Maximum events for internal history
export HISTSIZE=10000
# Maximum events in history file
export SAVEHIST=10000

# Dotfiles
export DOTFILES="$HOME/dotfiles"

# Cargo directory
export CARGO_HOME="$XGD_DATA_HOME/cargo"

# NPM config
export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"

# GTK 2
export GTK2_RC_FILES="$XDG_CONFIG_HOME/gtk-2.0/gtkrc"

# Ripgrep
export RIPGREP_CONFIG_PATH="$XDG_CONFIG_HOME/ripgrep/ripgreprc"

# Less
export LESS="--chop-long-lines --HILITE-UNREAD --ignore-case --incsearch --jump-target=4 --LONG-PROMPT \
--no-init --quit-if-one-screen --RAW-CONTROL-CHARS --use-color --window=4"

# BTRFS snapshots synced with grub
export SNAP_PAC_GRUB_ASYNC=1
