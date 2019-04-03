#!/usr/bin/env bash

if [[ "$1" = "-h" ]] || [[ "$1" = "--help" ]] || [[ $# -eq 0 ]]
then
    echo 'Usage: ./generate_bayesian_model.sh (n_params) (mem_len)'
    exit
fi

n_params=$1; shift
mem_len=$1; shift

len=${#mem_len}

add_leading_zeros() {
    number=$1; shift
    value=$((${#mem_len}-${#number}))
    case ${value} in
    1) echo '0'${number} ;;
    2) echo '00'${number} ;;
    3) echo '000'${number} ;;
    4) echo '0000'${number} ;;
    5) echo '00000'${number} ;;
    6) echo '000000'${number} ;;
    *) echo ${number} ;;
    esac
}

for (( i = 0; i < $((${n_params}-1)); ++i )); do
    for (( j = 0; j < ${mem_len}; ++j )); do
        echo "('v_${i}$(add_leading_zeros ${j})', 'v_${i}$(add_leading_zeros $((${j}+1)))'),"
        echo "('v_${i}$(add_leading_zeros ${j})', 'v_$((${n_params}-1))$(add_leading_zeros ${j})'),"
    done
done

for (( i = 0; i < $((${n_params}-1)); ++i )); do
    echo "('v_${i}${mem_len}' ,'v_$((${n_params}-1))${mem_len}'),"
done


for (( i = 0; i < ${mem_len}; ++i )); do
    echo "('v_$((${n_params}-1))$(add_leading_zeros ${i})', 'v_$((${n_params}-1))$(add_leading_zeros $((${i}+1)))'),"
done
