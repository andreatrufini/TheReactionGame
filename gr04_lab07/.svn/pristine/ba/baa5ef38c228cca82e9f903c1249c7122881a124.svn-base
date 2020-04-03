# this file implement a class that could be used to menage a serial
# comunication with a board, it create a dropdown menu with avaiable 
# ports and if there isn't avaiable port create a popup that said
# user to connect board

import tkinter as tk
from tkinter import *
from tkinter import messagebox as tkMessageBox
import time
import serial
import serial.tools.list_ports as port_list
import serial.serialutil
import threading
from PIL import Image, ImageTk

class serialConnection:
	def __init__(self, window, imageDir, imageSerialPopup):
		self.window = window
		self.imageDir = imageDir
		self.imageSerialPopup = imageSerialPopup
		self.portsList=[]
		self.refresh=1
		self.serialIsDefined=0
		self.SerialPort=0
		self.progressFlag=0
		self.port_choose=0
		
	def __exit__(self):
		self.refresh=0
	
	#####################################################	
	########### PUBLIC METHODS ##########################	
	def start(self):
		# this function verify a correct connection and 
		# if there are connection problem interact with user 
		# in order to resolve it
		
		# we save available ports
		self.getPortAvailable()
		
		# creation of connect window that wait for connection of usb 	
		# this is done only if there aren't ports available
		if len(self.portsList)==0:
			self.__connectBoard()
		
		
		# set default option for menu
		self.tkvar = StringVar(self.window)
		if self.port_choose!=0:
			self.tkvar.set(self.port_choose)
		else: 
			self.tkvar.set('Set port') 
		
		# creation of popup menù
		self.__portMenu()
		
		self.window.update()
		
		self.tkvar.trace('w', self.__changeDropdownMenu)
		
		
					
	def getPortAvailable(self):
		# this function return and save a list of current usb ports
		self.ports = list(port_list.comports())
		self.portsList=[]
		for p in self.ports: 
			self.portsList.append((p)[0])
			#print((p)[0])
		return self.portsList
	
	def refreshPortsMenu(self):
	    while self.refresh==1:
	    	self.getPortAvailable()
	    	if self.progressFlag==0:
		    	if len(self.portsList)==0:
		    		self.__connectBoard()	
		    	self.__portMenu()
		    	self.window.update()
	    	#self.window.update()
	    	time.sleep(2)	
		
	def write(self, text):
		if self.serialIsDefined:
			self.SerialPort.write(text)
	
	def read(self, number):
		if self.serialIsDefined:
			return self.SerialPort.read(number)
	
	#####################################################
	########### PRIVATE METHODS #########################			
				
	def __portMenu(self):
		# this function set menu used to set port
		#try:
		#	self.popupMenu.destroy()
		#except AttributeError:
		#	pass
		#set menu option using portsList that has beed update before
		self.popupMenu = OptionMenu(self.window, self.tkvar, *self.portsList)
		self.popupMenu.place(relx=.5, rely=.83, anchor=CENTER)
		self.popupMenu.config(bd=0, bg="#f74c6e", activebackground="#f10e3c", highlightbackground="#ce0c39", 
				font="times 15", relief=GROOVE, width=12)
		self.popupMenu['menu'].config(bg="#f74c6e", activebackground="#f10e3c", 
				font="times 15")
	
	def __connectBoard(self):		
		# this function interact with user waiting while a usb is connected
		# when it is connected this function wait until a correct comunication 
		# is performed
		
		# we create a popup that says to the user to connect a usb
		self.connect = Toplevel()
		self.connect.title("Serial connection")

		# we set popup proportion and image
		width_screen, height_screen = self.connect.winfo_screenwidth(), self.connect.winfo_screenheight() #read the dimensions of the screen
		width_root, height_root = int(width_screen/3),int(height_screen/3) #calculate the dimensions of the main window
		self.connect.geometry("%dx%d" % (width_root, height_root)) #setup of the window dimensions
		self.connect.resizable(width=False, height=False) #block the possibility to resize the dimensions of the window

		# backgroud setup
		image = Image.open(self.imageDir + self.imageSerialPopup)
		if image.size != (int(width_root), int(height_root)):
		    image = image.resize((int(width_root), int(height_root)), Image.ANTIALIAS)
		
		self.image = ImageTk.PhotoImage(image)
		self.bg_label = tk.Label(self.connect, image = self.image)
		self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
		self.bg_label.image = self.image
		
		# we save in portsList all port connected
		self.getPortAvailable()

		self.connect.update()

		# we wait for usb to be connected
		while len(self.portsList)==0:
			self.getPortAvailable()
			time.sleep(0.3)
	
		self.connect.destroy()
		
	def __changeDropdownMenu(self,*args):
		# This function is called when a port is selected in menù option
		# when called this function try to establish a connection to board
		# and until the connection isn't stable it show a progress bar. 
		# This function:
		# 	if usb choose can't connect
		#		-call __waitForSerialConnection as subprocess, this function
		#			wait for usb to be available and when it is delete loading bar
		#		-call __loadingBar that create a loading bar while __waitForSerialConnection
		#			is waiting for connection
		
		# save user choose
		old_choose = self.port_choose
		self.port_choose = self.tkvar.get()
		
		if old_choose!=self.port_choose:
			# set progress flag
			self.progressFlag=0

		
			if self.port_choose!="Set port":
				# this subprocess is used to repeatedly wait for connection,
				# when connection is stable progress bar is deleted
				tg=threading.Thread(target=self.__waitForSerialConnection)
				tg.start()
			
				# attempt to send message on serial port choosen
				try:
					self.SerialPort = serial.Serial(self.port_choose, 115200, bytesize=8, parity="N", 
									stopbits=1, timeout=None, xonxoff=0, rtscts=0, dsrdtr=0)		
					# the value 'R' is sent to initially turn off the LED to syncronize it with the GUI setup
					self.SerialPort.write(b'R')
				
				# we start loading bar if connection isn't stable
				except (OSError, serial.SerialException):
					self.popupMenu.destroy()
					self.__loadingBar()	
					self.progressFlag=1	
				
	
	def __waitForSerialConnection(self):
		# this function wait for serial connection 
		# and destroy progress bar if you establish connection
		
		connected=0
		
		# we wait until connection is established
		while not connected:
			try:
				self.SerialPort = serial.Serial(self.port_choose, 115200, bytesize=8, parity="N", stopbits=1, timeout=None, xonxoff=0, rtscts=0, dsrdtr=0)			# the value 'R' is sent to initially turn off the LED to syncronize it with the GUI setup
				self.SerialPort.write(b'R') 
				connected=1
			except (OSError, serial.SerialException):			
				connected=0
				time.sleep(0.5)
	
		# if loading bar was created we destroy it
		if self.progressFlag:
			self.progress.destroy()
			self.refresh=1
			
		self.serialIsDefined=1
		
		# we update menu
		self.__portMenu()

		self.window.update()
		
	def __loadingBar(self):
		# this function create a loading bar that 
		# that keeps bouncing from side to side
		# this bar will be destroy by __waitForSerialConnection whe you establish 
		# connection with board
	
		s = ttk.Style()
		s.theme_use('classic')
		s.configure("red.Horizontal.TProgressbar") #foreground ='red', background='yellow'
		self.progress=ttk.Progressbar(self.window, orient=HORIZONTAL, length=200, mode='indeterminate')
		self.progress.place(relx=.5, rely=.82, anchor=CENTER)
		self.progress.start(10)
	
		
		
		
		
