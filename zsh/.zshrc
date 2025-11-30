# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -v
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/mm/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
eval "$(starship init zsh)"

export EDITOR=/usr/bin/nvim
export VISUAL=/usr/bin/nvim
export SNAP_PAC_GRUB_ASYNC=1
