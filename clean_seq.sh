#!/bin/bash

if [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
    echo -e "Usage:\n./clean_seq filename [-s/--save] [-o/--overwrite]\n\t-s/--save\t\tsave file instead of printing to stdout\n\t-o/--overwrite\t\toverwrite input file. This option works only with -s/--save option"
    exit 0
fi

HEAD=`head -n 1 $1`
LEN=`wc -l $1 | awk '{ print $1 }'`

REAL_LEN=`echo $[ $LEN-1 ] | awk '{ print $0/2.25 }'`

mult() {
	echo $1 | awk -v var=$2 '{ print $0*var }'
}

divi() {
	echo $1 | awk -v var=$2 '{ print $0/var }'
}

if [ "$2" == "-s" ] || [ "$2" == "--save" ] || [ "$2" == "-so" ]
then
	FNAME=`echo $1 | sed 's/\.csv//g'`
	FNAME="${FNAME}_clean.csv"
	echo "$HEAD" > "$FNAME"
	tail -n $(mult $REAL_LEN 1.75) $1 | head -n $REAL_LEN >> "$FNAME"
else
	echo "$HEAD"
	tail -n $(mult $REAL_LEN 1.75) $1 | head -n $REAL_LEN
fi

if [ "$2" == "-so" ] || [ "$3" == "-o" ] || [ "$3" == "--overwrite" ]
then
    rm $1
    mv $FNAME $1
fi