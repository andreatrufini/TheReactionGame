#!/usr/bin/python3

import sys 
from termios import tcflush, TCIFLUSH #Useful to flush the input stream before reading a new data
import serial
import TerminalSupport as func

#Initialization of variables
ledstatus=0
QuitCond=0
mean=0
BestScore=65535
anywinner=0 #Identification of the presence of a winner between different gamers
GameSet=7 #Number of the game sets


#Setting of the dictionary in which the name of the champion is stored with his best score
winner={"Name":"Unknown",
	"Score": BestScore
	}

func.PrintTitle() #Print of the game title
func.PrintStr("Welcome to the terminal version of the game!")
func.PrintStr("The possible input commands are L0 to turn ON")
func.PrintStr("the Led on the board and L1 to switch it OFF. \n")
func.PrintLine('━')


#Verification of the serial port available on the PC
portlist=func.availableSerialPort()
if (not portlist):
	func.PrintStr("Board not connected. Retry!",file=sys.stderr)
	sys.exit(1)

#Print of the available serial port
SelectedPort=func.PrintMenu(portlist)
porta = serial.Serial("{0}".format(SelectedPort), 115200, bytesize=8, parity="N", stopbits=1, xonxoff=0, rtscts=0, dsrdtr=0)

#Reset the led on the board
porta.write(bytes("%s" %"R", encoding="ascii"))


#Game loop
while True:

	func.PrintTitle() #Print of the game title
	name=input("Insert your name: ")

	if(name==""):
		name=input("\nIt seems you've forgiven to insert your name. Please, do it now: ")
	
	func.PrintTitle() #New terminal 'page' inserted
	func.PrintStr("Welcome %s! Let's get started!" %name)
	func.PrintStr("Now, you have to switch on or turn off the LED on the")
	func.PrintStr("board easily putting L1 and L0 commands in the following line.")
	func.PrintStr("Be careful: you can only toggle the LED and")
	func.PrintStr("no others commands are accepted.\n")
	func.PrintStr("To exit from the game session and return to the menu ")
	func.PrintStr("you have to input the command 'Q'.\n")
	func.PrintLine("━")
	
	count=1
	bestscore_single=BestScore #Reset of the best score related to the actual gamer
	scoreMean=0 #Reset of the average score related to the actual gamer
	
	#Evaluation of the reaction time through GameSet numbers of trials
	while count<=GameSet:
				
		tcflush(sys.stdin, TCIFLUSH)	
		comm=input("Input the command number %d [L1, L0, Q]: " %count)
		
		if(comm=='Q'):
			QuitCond=1
			break

		InfoComm=func.Matchcommand(comm, ledstatus) #It checks if the command is valid, also through the led state
		
		#Loop until the input command is valid
		while (InfoComm[0]!=1):
			comm=input("Input the command number %d [L1, L0, Q]: " %count)
			InfoComm=func.Matchcommand(comm, ledstatus)
			
		ledstatus=InfoComm[1] #Update of the led state
		print("Ready?")
		func.DelayGenerator() #Wait until the random delay is expired
		porta.write(bytes("%s" %comm, encoding="ascii")) #Command that toggles the led
		timehex = porta.read(6) #Read of the results sent from the uC
		time=float(int(timehex[1:6], 16))/1000 #Conversion of the reaction time in ms
		print("\tReaction time is: %fs\n" %time)

		#Verification if the score is the best one for the current gamer
		if(time<bestscore_single):
			bestscore_single=time
		
		scoreMean+=time
		count+=1
	
	tcflush(sys.stdin, TCIFLUSH)
	if(QuitCond==0):
		scoreMean=scoreMean/GameSet #Evaluation of the average reaction time

		#Verification if the best result of the actual gamer is better than the actual champion's one
		if(scoreMean<winner["Score"]):
			winner["Name"]=name
			winner["Score"]=bestscore_single
			anywinner=1
		
		
		print("")
		func.PrintLine('━')
		func.PrintStr("Well %s, your best score is %fs and" %(name,bestscore_single))
		func.PrintStr("your average response time is %fs.\n" %scoreMean)

		if(anywinner):
			func.PrintStr("CONGRATULATION!")
			func.PrintStr("You scored the best result!\n")
		else:
			func.PrintStr("You lose! It seems %s is faster\n!" %winner["Name"])
	
		func.PrintLine('━')

	else:
		QuitCond=0
		func.PrintLine('━')
		if(bestscore_single < BestScore):
			print("")
			func.PrintStr("Well %s, your best score is %fs.\n" %(name,bestscore_single))		
		else:
			print("")
			func.PrintStr("Well %s, I'm sorry you haven't played any matches.\n" %(name))	


	choice = func.inputMultiStr("Would you like to retry? (y/n): ")

	while(choice!='Y' and choice!='y' and choice!='N' and choice!='n'):
		print("")
		choice = func.inputMultiStr("Bad command, type y or n.\n Would you like to retry? (y/n): ")

	if(choice=='N' or choice=='n'):
		porta.close()
		sys.exit(1)		
	func.PrintLine('━')
	
	count=1
	anywinner=0
