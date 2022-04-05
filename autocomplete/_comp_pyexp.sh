#!/bin/bash
_comp_pyexp()
{
    has_name_opt="show del artifacts diff"
    if [ "${#COMP_WORDS[@]}" == "2" ]; then
        COMPREPLY=($(compgen -W "list show new sel del add rm artifacts diff save cmd -h --help --version" -- "${COMP_WORDS[1]}"))
        return 0
    elif [ "${#COMP_WORDS[@]}" == "3" ]; then
        if [ "${COMP_WORDS[1]}" == "add" ]; then
            COMPREPLY=($(compgen -f -d -- "${COMP_WORDS[2]}"))
            return 0
        elif [ "${COMP_WORDS[1]}" == "sel" ]; then
            list="$(ls ~/.pyexp/)"
            list=("${list[@]/_selected}")
            COMPREPLY=($(compgen -W "$list" -- "${COMP_WORDS[2]}"))
            return 0
        elif [ "${COMP_WORDS[1]}" == "save" ]; then
            COMPREPLY=($(compgen -W "-n --name -h --help" -f -- "${COMP_WORDS[2]}"))
            return 0
        elif [[ "$has_name_opt" == *"${COMP_WORDS[1]}"* ]]; then
            COMPREPLY=($(compgen -W "-n --name -h --help" -- "${COMP_WORDS[2]}"))
            return 0
        else
            COMPREPLY=($(compgen -W "-h, --help" -- "${COMP_WORDS[2]}"))
            return 0
        fi
    elif [ "${#COMP_WORDS[@]}" == "4" ]; then
        if [[ "$has_name_opt save" == *"${COMP_WORDS[1]}"* ]] && [[ "-n --name" == *"${COMP_WORDS[2]}"* ]]; then
            list="$(ls ~/.pyexp/)"
            list=("${list[@]/_selected}")
            COMPREPLY=($(compgen -W "$list" -- "${COMP_WORDS[3]}"))
            return 0
        fi
    elif [ "${#COMP_WORDS[@]}" == "5" ] && [ "${COMP_WORDS[1]}" == "save" ] && [[ "-n --name" == *"${COMP_WORDS[2]}"* ]]; then
        COMPREPLY=($(compgen -f -- "${COMP_WORDS[4]}"))
        return 0
    fi
    
    

    return 0
}
complete -o filenames -o nospace -o bashdefault -F _comp_pyexp pyexp