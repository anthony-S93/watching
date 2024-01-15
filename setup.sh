#!/bin/sh
app_home="$(dirname "$(readlink -f "$0")")"
completion_dir="$HOME/.local/share/bash-completion/completions"

if [ "$(id -u)" = 0 ]
then
    echo "The setup script should not be run with sudo"
    echo "Aborting..."
    exit 1
else
    if type watching > /dev/null 2>&1
    then
        echo "A binary named 'watching' already exists in PATH"
        echo "Aborting..."
        exit 1
    fi

    if [ -e "/usr/local/bin/watching" ]
    then
        echo "Unable to create a symlink named 'watching' inside /usr/local/bin"
        echo "Please add the bin/ directory of this repo to your PATH manually"
    else
        echo "==> Creating symlink inside /usr/local/bin"
        if sudo ln -s "$app_home/bin/watching" "/usr/local/bin/watching" 2>&1
        then
            echo "==> Symlink /usr/local/bin/watching created"
        else
            echo "==> Failed to create symlink /usr/local/watching"
            echo "Please add the /bin directory of this repo to your PATH manually"
        fi
    fi

    # Add bash completion script
    if [ -d "$completion_dir" ]
    then
        echo "==> Adding bash completion"
        ln -s "$app_home/bash-completion/watching.bash" "$completion_dir/watching.bash"
    else
        if [ ! -e "$completion_dir" ]
        then
            echo "==> Adding bash completion"
            mkdir -p "$completion_dir"
            ln -s "$app_home/bash-completion/watching.bash" "$completion_dir/watching.bash"
        else
            echo "==> Failed to add bash-completion"
            echo "A file already exists at $completion_dir"
        fi
    fi
fi
