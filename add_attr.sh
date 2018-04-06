#!/bin/bash

############################################
#FUNCTIONS
############################################

get_attr() {
	# $1 is attr, e.g $1=a means attr='a'
	# $2 is attribute name, $3 is value of the attribute, e.g $2=value and $3=1 means value=1
	
	echo $INPUT_FILE | xargs cat  | tr -d ' \|\t' | grep -i "attr='$1'" | grep "$2=$3"
}

get_attribute_value() {
	# from given line $1 returns value of attribute named $2, e.g returns 2 for value=2 when $2=value
	IFS=';'; LINE=($1); unset IFS;
	for i in ${LINE[*]}
	do
		case $i in
			"$2"=*)
			VAL="${i#*=}"
			shift # past argument=value
			;;
		esac
	done
	echo $VAL
}

find_line() {
	RET=$1
	LEN=2
	for i in $(get_attr $1 'value' $2)
	do
		for j in $(get_attr $1 'value' $3)
		do
			TO1=$(get_attribute_value $i 'to')
			FROM2=$(get_attribute_value $j 'from')

			if [ "$FROM2" == "$TO1" ]
			then
				TO2=$(get_attribute_value $j 'to')
				FROM1=$(get_attribute_value $i 'from')
				RET=$RET":($FROM1,$TO1,$TO2)"
				LEN=$[ $LEN+1 ]
			fi
		done
	done
	
	echo "$LEN:${RET[*]}"
}
get_item() {
	if [ $# -eq 4 ]
	then
		echo $1 | sed "s/[$4]//g" | awk -F"$2" "{ print \$$3 }"
	else
		echo $1 | awk -F"$2" "{ print \$$3 }"
	fi
}

intercepts() {
	if [ "$1" == "null" ] || [ "$2" == "null" ]
	then
		echo "null"
		return
	fi
	case $# in
		1)
			echo "null"
			return
		;;
		2)
			F1=$(get_item $1 "," 1 "()")
			F2=$(get_item $2 "," 1 "()")
			T1=$(get_item $1 "," 2 "()")
			T2=$(get_item $2 "," 2 "()")
			if [ $F2 -ge $F1 ] && [ $F2 -le $T1 ]
			then
				echo $2
			elif [ $F1 -ge $F2 ] && [ $F1 -le $T2 ]
			then
				echo $1
			else
				echo "null"
				return
			fi
		;;
		*)
			echo $(intercepts $(intercepts $1 $2) ${@:3})
		;;
	esac
}

find_range() {

	#----INIT----
	RET=()
	for i in `seq 1 $#`
	do
		COUNTERS[$i]=3
		LENGTHS[$i]=$[ $(get_item ${@:$i:1} ":" 1) ]
	done
	#------------
	
	
	while true
	do
		BREAK=1
		#---MAIN PART---
		for i in `seq 1 $#`
		do
			RANGES[$i]=$(get_item ${@:$i:1} ":" ${COUNTERS[$i]})
		done
		
		RES=$(intercepts ${RANGES[*]})
		if [ "$RES" != "null" ]
		then
			RET+=($RES)
		fi
		
		#---------------
		#---STOP PART---
		for i in `seq 1 $#`
		do
			if [ ${COUNTERS[$i]} -ne ${LENGTHS[$i]} ]
			then
				BREAK=0
			fi
		done
		if [ $BREAK -eq 1 ]
		then
			break
		fi
		#---------------
		#---INCR PART---
		COUNTERS[1]=$[ ${COUNTERS[1]}+1 ]
		for i in `seq 1 $#`
		do
			if [ ${COUNTERS[$i]} -gt ${LENGTHS[$i]} ]
			then
				COUNTERS[$i]=3
				COUNTERS[$[ $i+1 ]]=$[ ${COUNTERS[$[ $i+1 ]]}+1 ]
			fi
		done
		#---------------
	done
	echo ${RET[*]}
}

produce_rules() {
	#$1 - attr
	#$2 - (value1,value2)
	#$3 - domain
	#$4 - (from,change,to)
	#$5 - probability
	#echo 'attr='a';value=1;domain=[1,2,3,4]; from=-300;to=-280;probability=0.8'
	
	echo "attr=$1;value="$(get_item $2 , 1 "()")";domain=$3;from="$(get_item $4 , 1 "()")";to="$(get_item $4 , 2 "()")";probability=$5"
	echo "attr=$1;value="$(get_item $2 , 2 "()")";domain=$3;from="$(get_item $4 , 2 "()")";to="$(get_item $4 , 3 "()")";probability=$5"
}

############################################
#MAIN PART GOES HERE
############################################

INPUT_FILE=""
RULES_FILE=""
OUTPUT_FILE=""

## INPUT ARGUMENTS ##
ME=$(basename "$0")
while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-i|--input)
		INPUT_FILE="$2"
		shift # past argument
		shift # past value
		;;
		-r|--rules)
		RULES_FILE="$2"
		shift # past argument
		shift # past value
		;;
		-a|--append)
		APPEND=true
		shift # past argument
		;;
		-s|-o|--output|--save)
		OUTPUT_FILE="$2"
		shift # past argument
		shift # past value
		;;
		-h|--help)
		echo -en "\n -i/--input for input file path\n -o/--output/-s/--save for output file path\n -r/--rules for rules file path\n -a/--append if this option is used, the script will print input and then print result\n\n example:\n ./$ME -i config1 -r rules -o config2\n\n Input and rules files are requied. If output is not specified, the result will be written to the stdout.\n---------------------\n"
		shift
		;;
		*)
		echo "Invalid input. Try -h or --help option for help."
		exit
		;;
	esac
done

if [ "$INPUT_FILE" == "" ] || [ "$RULES_FILE" == "" ]
then
	echo "Invalid input. Try -h or --help option for help."
	exit
elif
	[ ! -f "$INPUT_FILE" ]
then
	echo "Such file does not exist."
	exit
fi

## PARSING RULES ##

for j in $(echo $RULES_FILE | xargs cat | tr -d ' \|\t')
do
	IFS=';'; LINE=($j); unset IFS;
	for i in ${LINE[*]}
	do
	case $i in
		attr=*)
		ATTR="${i#*=}"
		shift # past argument=value
		;;
		value=*)
		VALUE="${i#*=}"
		shift # past argument=value
		;;
		probability=*)
		PROBABILITY="${i#*=}"
		shift # past argument=value
		;;
		domain=*)
		DOMAIN="${i#*=}"
		shift # past argument=value
		;;
		*)
		      # unknown option
		;;
	esac
	done
	
	
	TEMP=$(echo $VALUE | sed -e 's/[()]//g')
	IFS=','; VALUES=($TEMP); unset IFS;
	TEMP=${VALUES[${#VALUES[*]}-1]}
	IFS='->'; VAL_CHANGE=($TEMP); unset IFS;
	
	VAL_CHANGE_FROM=${VAL_CHANGE[0]}
	VAL_CHANGE_TO=${VAL_CHANGE[2]}

	
	ATTR_NAME=()
	VAL_CH_FROM=()
	VAL_CH_TO=()
	
	for i in `seq 0 $[${#VALUES[*]}-2]`
	do
		TEMP=${VALUES[$i]}
		IFS='='; VAL_CHANGE=($TEMP); unset IFS;
		ATTR_NAME+=(${VAL_CHANGE[0]})
		
		IFS='->'; TEMP=(${VAL_CHANGE[1]}); unset IFS;
		VAL_CH_FROM+=(${TEMP[0]})
		VAL_CH_TO+=(${TEMP[2]})
		
	done
	
	LINES=()
	for i in ${!ATTR_NAME[*]}
	do
		LINES+=($(find_line ${ATTR_NAME[$i]} ${VAL_CH_FROM[$i]} ${VAL_CH_TO[$i]}))
	done
	
	cat $INPUT_FILE
	if [ -z "$OUTPUT_FILE" ]
	then
		for i in $(find_range ${LINES[*]})
		do
			produce_rules $ATTR "($VAL_CHANGE_FROM,$VAL_CHANGE_TO)" $DOMAIN $i $PROBABILITY
		done
	else
		for i in $(find_range ${LINES[*]})
		do
			produce_rules $ATTR "($VAL_CHANGE_FROM,$VAL_CHANGE_TO)" $DOMAIN $i $PROBABILITY >> $OUTPUT_FILE
		done
	fi		
done
