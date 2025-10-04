# Git Setup

This guide explains how to set up Git for working with multiple accounts.<br>
If you only have one Git account, you probably don't need multiple SSH keys.<br>
Make sure to also configure Git aliases for convenience.

### Create Files

* `<path/to/user>/.gitconfig`
```gitconfig
[includeIf "gitdir:<path/to/projects>/home/"]
    path = <path/to/projects>/home/.gitconfig

[includeIf "gitdir:<path/to/projects>/work/"]
    path = <path/to/projects>/work/.gitconfig

[core]
    sshCommand = C:/Windows/System32/OpenSSH/ssh.exe

[alias]
    l = log --pretty=format:'%h - %ad - %s' --date=iso-strict
    s = status
    r = restore .
    rs = restore --staged .
    a = add .
    cm = commit -m
    ca = commit --amend --no-edit
    pf = push --force
    b = branch
    c = checkout
    cb = checkout -b
    m = merge
    soft = reset --soft HEAD~1
    mixed = reset --mixed HEAD~1
    hard = reset --hard HEAD~1
```

* `<path/to/projects>/home/.gitconfig`
```gitconfig
[user]
    name = <full-name> ⚡
    email = <home@mail>
```

* `<path/to/projects>/work/.gitconfig`
```gitconfig
[user]
    name = <full-name> ⚡
    email = <work@mail>
```

* `<path/to/user>/.ssh/config`
```
Host home.github.com
    HostName github.com
    User git
    IdentityFile <path/to/user>/.ssh/id_ed25519_home
    IdentitiesOnly yes

Host work.github.com
    HostName github.com
    User git
    IdentityFile <path/to/user>/.ssh/id_ed25519_work
    IdentitiesOnly yes
```

### Run Commands

```bash
ssh-keygen -t ed25519 -C "<home@mail>" -f "<path/to/user>/.ssh/id_ed25519_home"
ssh-keygen -t ed25519 -C "<work@mail>" -f "<path/to/user>/.ssh/id_ed25519_work"

Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

ssh-add "<path/to/user>/.ssh/id_ed25519_home"
ssh-add "<path/to/user>/.ssh/id_ed25519_work"

git remote set-url origin git@home.github.com:<username>/<repo>.git # origin is already defined
git remote add origin git@home.github.com:<username>/<repo>.git     # origin is not defined yet
git clone git@home.github.com:<username>/<repo>.git
```
