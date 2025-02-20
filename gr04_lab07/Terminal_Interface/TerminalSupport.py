#!/usr/bin/python3.6
import sys
import os

#Function to control which serial ports can be used
def availableSerialPort():
	import serial.tools.list_ports as port_list
	portsList=[]
	ports = list(port_list.comports())
	for p in ports: 
		portsList.append((p)[0])

	return (portsList)#return a list with all the name of the available ports


#Function to control if the second symbol passed is 0 or 1 and to check if the command is valid
def Matchcommand(command, ledstatus):

	correctness=0

	if(command == "L0" or command == "L1"):
		if(command=="L0" and ledstatus== 1): 
			ledstatus=0
			correctness=1
		else:
			if (command=="L1" and ledstatus == 0): 
				ledstatus=1
				correctness=1
			elif (correctness == 0):
				print("You have to toggle the led!\n")
				
	else:
		print("The command must be L0 or L1!\n")
		
	return correctness, ledstatus  	#Rturns the correctness and the status (on=1 or off=0) of Led


#Function to generate a delay 
def DelayGenerator():
	import random
	from time import sleep
	delay=random.randrange(10000, 20000, 1) #Random delay between 10000 and 20000 ms
	sleep(delay/1000) #Delay expressed in seconds


#Function to print the menu of the serial port connected to the PC and to acquire the correct selection
def PrintMenu(portlist):

	PrintStr("SERIAL PORT SELECTION:\n")
	PrintStr("List of the devices connected to the PC:")
	index = 0
	for port in portlist:
		PrintStr("{0}. {1}".format(index, port))
		index+=1
	print("")
	PrintStr("Insert the index corresponding to the port")
	Col=os.get_terminal_size().columns
	index_sel=input(int((Col-len("path in which the board is connected: "))/2)*" "+"path in which the board is connected: ")
	while(index_sel<'0' or ord(index_sel)>=(index+48)):
		PrintStr("Invalid selection. Retry!")
		PrintStr("Insert the index corresponding to the")
		index_sel=input(int((Col-len("path in which the board is connected: "))/2)*" "+"path in which the board is connected: ")		
	return portlist[ord(index_sel)-48]
			

#Function to print the title of the game and to clear the terminal page
def PrintTitle():
	sys.stdout.write("\x1b[2J\x1b[H")
	Col=os.get_terminal_size().columns #Acquisition of the width of the display
	print('━'*Col)
	print("THE REACTION GAME".center(os.get_terminal_size().columns))
	print('━'*Col)
	print("")

def PrintLine(str):
	Col=os.get_terminal_size().columns #Acquisition of the width of the display
	print(str*Col)
	print("")
	
def PrintStr(str):
	Col=os.get_terminal_size().columns #Acquisition of the width of the display
	if Col<len(str):
		print(str)
	else:
		sys.stdout.write(int((Col-len(str))/2)*" ")
		print(str)
def PrintMultiStr(str):
	for i in str.split("\n"):
		PrintStr(i)

def inputStr(str):
	Col=os.get_terminal_size().columns
	return input(int( (Col-len(str))/2 )*" "+str)

def inputMultiStr(str):
	for i in str.split("\n")[0:-1]:
		PrintStr(i)
	return inputStr( str.split("\n")[-1] )
