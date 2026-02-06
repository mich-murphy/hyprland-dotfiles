alias ls="eza -la --icons --group-directories-first"

set -g fish_key_bindings fish_vi_key_bindings

if status is-interactive
    # Commands to run in interactive sessions can go here
end

starship init fish | source
direnv hook fish | source
zoxide init fish | source
fzf --fish | source
