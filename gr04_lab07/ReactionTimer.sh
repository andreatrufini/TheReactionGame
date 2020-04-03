#!/bin/bash 

function printStr {
	# this function take:
	# $1 -> string to print
	# $2 -> if equal to "sp" print space up to and of terminal after str
	# 	if equal to "ret" print only a carriage return after str 
	#	if it isn't one of the previous function doesn't print
	#		anything after str 
	# and print strig centred in terminal
	Str=$1
	lenStr=${#Str}
	isodd=$(($lenStr%2))
	nspace1=$((($var-$lenStr)/2))
	nspace2=$(($nspace1+$isodd))
	for i in `seq 1 $nspace1`;
	do
		echo -n " "
	done
	echo -n $Str
	# if the caller want function print
	# space after str
	case $2 in
	"sp")
		for i in `seq 1 $nspace2`;
        	do
                	echo -n " "
        	done
		;;
	"ret")
		echo ""
		;;
	*)
		echo -n ""
		;;
	esac
}	

chmod u+x GUI_Interface/GUI.py
chmod u+x Terminal_Interface/Terminal.py

var=$(tput cols)
tput clear
tput bold
tput setaf 3
tput cup 1 0
tput rev 
printStr "The reaction game" sp
tput sgr0
tput cup 3 0
tput setaf 7
printStr "Set the execution mode of the game:" ret
tput cup 5 0
tput setaf 6
printStr "1. Terminal" ret
tput cup 7 0
tput setaf 6
printStr "2. GUI     " ret

tput bold
tput cup 9 0
tput setaf 7
printStr "Enter your choice [1-2]:"
read choice



case $choice in
        1)
	    clear
	    tput sgr0 
	    cd Terminal_Interface
	    ./Terminal.py	    
	    ;;
	
	2)
       	    clear
       	    tput sgr0
	    cd GUI_Interface
	    log=$(./GUI.py 2>&1)
	    echo $log > log.txt
	    ;;

	*)
	    tput setaf 6
	    printStr "Error of the input. Retry"
	    ;;
esac
