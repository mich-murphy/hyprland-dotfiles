set -g fish_key_bindings fish_vi_key_bindings
set -g fish_greeting

if status is-login
  set -x BROWSER chromium
end

if status is-interactive
    alias ls="eza -la --icons --group-directories-first"
    starship init fish | source
    direnv hook fish | source
    zoxide init fish | source
    fzf --fish | source
end
