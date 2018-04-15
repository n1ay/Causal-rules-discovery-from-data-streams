#!/bin/bash

ME=$(basename "$0")

if [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
	echo -e " First argument: config file path. Second: shift value.\n Usage example:\n ./$ME config 1000\n\n If third argument is -m then the script will multiply ranges by specified value instead of adding:\n ./$ME config 2 -m \n--------------------"
	exit
fi

if [ "$3" == "-m" ]
then
	for i in `cat $1 | tr -d ' \|\t'`
	do
		PRE=$(echo $i | awk -F";" '{ print $1 ";" $2 ";" $3 ";" }')
		POST=$(echo $i | awk -F";" '{ print $6 }')
		FROM=$(echo $i | awk -F";" '{ print $4 }' | awk -v val="$2" -F"=" '{ print $2*=val }')
		TO=$(echo $i | awk -F";" '{ print $5 }' | awk -v val="$2" -F"=" '{ print $2*=val }')
		echo "${PRE}from=${FROM};to=${TO};$POST"
	done
	exit
fi

for i in `cat $1 | tr -d ' \|\t'`
do
	PRE=$(echo $i | awk -F";" '{ print $1 ";" $2 ";" $3 ";" }')
	POST=$(echo $i | awk -F";" '{ print $6 }')
	FROM=$(echo $i | awk -F";" '{ print $4 }' | awk -v val="$2" -F"=" '{ print $2+=val }')
	TO=$(echo $i | awk -F";" '{ print $5 }' | awk -v val="$2" -F"=" '{ print $2+=val }')
	echo "${PRE}from=${FROM};to=${TO};$POST"
done
