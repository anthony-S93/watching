_watching_completion() {
    local cur prev
    _init_completion || return

    case "$prev" in
        watching)
            readarray -t COMPREPLY < <(compgen -W "-n --interval -h --help -t --no-title -w --no-wrap" -- "$cur")
            ;;
    esac
}

complete -o nosort -F _watching_completion watching
