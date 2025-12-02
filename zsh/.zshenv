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

# Fzf
export FZF_DEFAULT_COMMAND="rg --files --hidden --glob '!.git'"
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_COLORS="bg+:#1a1b26,\
fg:#a9b1d6,\
fg+:#c0caf5,\
border:#1a1b26,\
spinner:#3b4261,\
hl:#7dcfff,\
header:#e0af68,\
info:#7aa2f7,\
pointer:#7aa2f7,\
marker:#f7768e,\
prompt:#a9b1d6,\
hl+:#7aa2f7"
export FZF_DEFAULT_OPTS="--height 60 \
--border none \
--layout reverse \
--color '$FZF_COLORS' \
--prompt '∷ ' \
--pointer ▶ \
--marker ⇒"
export FZF_ALT_C_OPTS="--preview 'tree -C {} | head -n 10'"
export FZF_CTRL_T_OPTS="--height 60 \
--border none \
--layout reverse \
--color '$FZF_COLORS' \
--prompt '∷ ' \
--pointer ▶ \
--marker ⇒
--preview 'bat --color=always {}' \
--preview-window '~2',border-none"
export FZF_COMPLETION_DIR_COMMANDS="cd pushd rmdir tree ls"

# Less
export LESS="--chop-long-lines --HILITE-UNREAD --ignore-case --incsearch --jump-target=4 --LONG-PROMPT \
--no-init --quit-if-one-screen --RAW-CONTROL-CHARS --use-color --window=4"

# BTRFS snapshots synced with grub
export SNAP_PAC_GRUB_ASYNC=1
