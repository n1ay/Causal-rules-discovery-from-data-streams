#!/bin/bash

HEAD=`head -n 1 $1`
LEN=`wc -l $1 | awk '{ print $1 }'`

REAL_LEN=`echo $[ $LEN-1 ] | awk '{ print $0/2.25 }'`

mult() {
	echo $1 | awk -v var=$2 '{ print $0*var }'
}

divi() {
	echo $1 | awk -v var=$2 '{ print $0/var }'
}

echo $HEAD
tail -n $(mult $REAL_LEN 1.75) $1 | head -n $REAL_LEN
