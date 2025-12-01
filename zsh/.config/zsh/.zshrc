typeset -U path cdpath fpath manpath
fpath+=(/usr/share/zsh/site-functions /usr/share/zsh/$ZSH_VERSION/functions /usr/share/zsh/vendor-completions)

HISTSIZE=10000
SAVEHIST=10000
HISTFILE=$ZDOTDIR/.zsh_history
mkdir -p "$(dirname "$HISTFILE")"

unsetopt APPEND_HISTORY
setopt HIST_FCNTL_LOCK
setopt EXTENDED_HISTORY
setopt HIST_IGNORE_SPACE
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS
setopt HIST_VERIFY
setopt autocd
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt PUSHD_SILENT
setopt CORRECT
setopt CDABLE_VARS

# Vim Keys
bindkey -v

# Vi navigation in completion menu
zmodload zsh/complist
bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -M menuselect 'l' vi-forward-char

# Limit zcomdump to once daily
autoload -Uz compinit
for dump in $ZDOTDIR/.zcompdump(N.mh+24); do
  compinit
done
compinit -C

# Completions
zstyle ':completion:*' completer _extensions _complete _approximate
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path "$XDG_CACHE_HOME/zsh/.zcompcache"
zstyle ':completion:*' complete true
zstyle ':completion:*' menu select
zstyle ':completion:*' complete-options true
zstyle ':completion:*' file-sort modification
zstyle ':completion:*:*:*:*:corrections' format '%F{yellow}!- %d (errors: %e) -!%f'
zstyle ':completion:*:*:*:*:descriptions' format '%F{blue}-- %D %d --%f'
zstyle ':completion:*:*:*:*:messages' format ' %F{purple} -- %d --%f'
zstyle ':completion:*:*:*:*:warnings' format ' %F{red}-- no matches found --%f'
zstyle ':completion:*:*:cd:*' tag-order local-directories directory-stack path-directories
zstyle ':completion:*' group-name ''
zstyle ':completion:*:*:-command-:*:*' group-order aliases builtins functions commands
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' keep-prefix true

# Setup fzf to be support in zsh-vi-mode
zvm_after_init_commands+=('[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh')
set rtp+=/usr/bin/fzf
zle -N fzf-cd-widget
bindkey -M emacs '^e' fzf-cd-widget
bindkey -M vicmd '^e' fzf-cd-widget
bindkey -M viins '^e' fzf-cd-widget

# Vim mode cursor styles
function zvm_config() {
  ZVM_INSERT_MODE_CURSOR=$ZVM_CURSOR_BEAM
  ZVM_NORMAL_MODE_CURSOR=$ZVM_CURSOR_BLOCK
  ZVM_VI_SURROUND_BINDKEY=s-prefix
}

source "$XDG_CONFIG_HOME/zsh/aliases"
source /usr/share/zsh/plugins/zsh-vi-mode/zsh-vi-mode.plugin.zsh
source /usr/share/zsh/plugins/zsh-autopair/autopair.zsh
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh
source /usr/share/zsh/plugins/zsh-you-should-use/you-should-use.plugin.zsh
if [[ $options[zle] = on ]]; then
  source <(/usr/bin/fzf --zsh)
fi

# Zsh-history-substring-search
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# Initialise utils
eval "$(direnv hook zsh)"
eval "$(zoxide init zsh)"
eval "$(starship init zsh)"
