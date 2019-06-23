#!/bin/bash
log_file='log_file-seq2-9600.txt'
values=(0.00001 0.00003 0.0001 0.0003 0.001 0.003 0.01 0.03 0.1 0.3 1)

cat /dev/null > $log_file

for a1 in ${values[*]}
do
    for a2 in ${values[*]}
    do
        for a3 in ${values[*]}
        do
            for a4 in ${values[*]}
            do
                python3 CRDiS_evaluation.py $a1 $a2 $a3 $a4 | tee -a $log_file
            done
        done
    done
done
