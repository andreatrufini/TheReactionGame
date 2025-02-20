#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as tkMessageBox
from PIL import Image, ImageTk
import random 
#sudo apt-get install python3 python-pygame
import pygame
import threading
from Music import *
from serialConnection import *


class ReactionTimer:
	def __init__(self, imageDir, imageScreenOne, imageScreenTwo, imageScreenThree, imageSerialPopup):
		# imageDir: directory for image
		# imageScreenOne: background image for the first screen
		# imageScreenTwo: background image for the second screen
		# imageScreenThree: background image for the third screen
		
		# initialization
		self.imageDir = imageDir
		self.imageScreenOne = imageScreenOne
		self.imageScreenTwo = imageScreenTwo
		self.imageScreenThree = imageScreenThree
		self.imageSerialPopup = imageSerialPopup
		# this are the proportion of us screen and will be used to 
		# change dimension of window if the computer of user has different dimension
		self.imageW = 1366
		self.imageH = 766
		self.minRandTime=10
		self.maxRandTime=20
		# we initialize variable for mean
		self.minPartialInit = 100000
		self.minPartial = self.minPartialInit
		self.minMeanInit = 100000
		self.minMean = self.minMeanInit
		self.count=0
		self.tot=0
		self.meanYPos=0
		self.flag_off = 0
		self.flag_on = 1
		self.__toggle=0
		# we initialize user variable
		self.__user=" "
		# we set a flag that is uset to know if play restart, in this case 
		# music mustn't restart
		self.__tryAgainFlagForMusic=0
		
		# we initialize rootscreen
		self.window=tk.Tk()
		self.window.title("The reaction game")
		#read the dimensions of the screen
		self.widthScreen, self.heightScreen = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
		#calculate the dimensions of the main window
		self.widthRoot, self.heightRoot = int(self.widthScreen/2),int(self.heightScreen/2)
		#setup of the window dimensions
		self.window.geometry("%dx%d" % (self.widthRoot, self.heightRoot)) 
		#block the possibility to resize the dimensions of the window
		self.window.resizable(width=False, height=False) 
		
		# we initialize serial object
		self.serialObj = serialConnection(self.window, self.imageDir, self.imageSerialPopup)
		
		# we start music
		self.music=Music(self.window,"Img/","sound_on.png","sound_off.png","Music/", "InstantCrush.wav")
		
	def __exit__(self):
		self.music.destroy()

	def setTimeButtonImage(self, imageRed, imageRedPressed, imageGreen, imageGreenPressed):
		# this function initialize variable and image for button in second screen 
		self.time_DimX=int(self.widthScreen*140/self.imageW)
		self.time_DimY=round(self.heightScreen*140/self.imageH)
		self.__toggle=0
		
		image_red = Image.open(self.imageDir+imageRed)
		image_red = image_red.resize((self.time_DimX,self.time_DimY), Image.ANTIALIAS)
		self.photoRed = ImageTk.PhotoImage(image_red)

		image_green = Image.open(self.imageDir+imageGreen)
		image_green = image_green.resize((self.time_DimX,self.time_DimY), Image.ANTIALIAS)
		self.photoGreen = ImageTk.PhotoImage(image_green)

		image_red_pressed = Image.open(self.imageDir+imageRedPressed)
		image_red_pressed = image_red_pressed.resize((self.time_DimX,self.time_DimY), Image.ANTIALIAS)
		self.photoRedPressed = ImageTk.PhotoImage(image_red_pressed)

		image_green_pressed = Image.open(self.imageDir+imageGreenPressed)
		image_green_pressed = image_green_pressed.resize((self.time_DimX,self.time_DimY), Image.ANTIALIAS)
		self.photoGreenPressed = ImageTk.PhotoImage(image_green_pressed)
	
	def setWelcomeImage(self,imageWelcome, welcW, welcH):
		# this function set variable and image used in welcome image that 
		# display also user id
		welcomeImg = Image.open(self.imageDir+imageWelcome)
		self.welcomeImg = ImageTk.PhotoImage(welcomeImg)
		self.welcW = welcW
		self.welcH = welcH
		
	def setStopImage(self,imageStop):
		# this function set variable and image used for stop button in second screen
		self.stopDimX=int(self.widthScreen*80/self.imageW)
		self.stopDimY=int(self.heightScreen*40/self.imageH)
		image_stop = Image.open(self.imageDir+imageStop)
		image_stop = image_stop.resize((self.stopDimX,self.stopDimY), Image.ANTIALIAS)
		self.photoStop = ImageTk.PhotoImage(image_stop)
	
	def setTryAgainImage(self, imageTryAgain, imageTryAgainPressed):
		# this function set variable used for try again button 
		# in the laste screen
		self.tryAgainDimX = int(self.widthScreen*100/self.imageW)
		self.tryAgainDimY = int(self.heightScreen*100/self.imageH)
		
		image_tryagain = Image.open(self.imageDir + imageTryAgain)
		image_tryagain = image_tryagain.resize((self.tryAgainDimX,self.tryAgainDimY), Image.ANTIALIAS)
		self.photoTryAgain = ImageTk.PhotoImage(image_tryagain)
	
		image_tryagain_pressed = Image.open(self.imageDir + imageTryAgainPressed)
		image_tryagain_pressed = image_tryagain_pressed.resize((self.tryAgainDimX,self.tryAgainDimY), Image.ANTIALIAS)
		self.photoTryAgainPressed = ImageTk.PhotoImage(image_tryagain_pressed)
		
	def setExitButton(self, imageExitButton):
		# this function set variable and image of exit button
		self.exitDimX = int(self.widthScreen*80/self.imageW)
		self.exitDimY = int(self.heightScreen*40/self.imageH)
		image_exit = Image.open(self.imageDir + imageExitButton)
		image_exit = image_exit.resize((self.exitDimX,self.exitDimY), Image.ANTIALIAS)
		self.photoExit = ImageTk.PhotoImage(image_exit)
	   
	def setBeginButton(self, imageBeginButton):
		# this function set variable and image of begin button
		self.beginDimX=int(self.widthScreen*90/self.imageW)
		self.beginDimY=int(self.heightScreen*45/self.imageH)
		image_begin = Image.open(self.imageDir + imageBeginButton)
		image_begin = image_begin.resize((self.beginDimX, self.beginDimY), Image.ANTIALIAS)
		self.photoBegin = ImageTk.PhotoImage(image_begin)
			
	
	#####################################################	
	################# PUBLIC METHODS ####################
	def start(self):
		# this function is a interface function, in this way 
		# when start is called program begin
		# we start first screen
		self.firstScreen()
		
	def firstScreen(self,event=None):
		# in this window the user can set its user name and start game
		# the real game begin when user press enter and the program start second screen
		
		# we set background
		self.__setBackground(self.imageScreenOne)
		# we start the music rising only if is the first time that we enter in this function
		if self.__tryAgainFlagForMusic==0:
			# we start music
			self.music.musicStart()		
		# we draw music button
		self.music.buttonDraw()			
		# we put entry box in centre of game screen
		# in which user can write its username
		self.__adminEntry()
		# we set this flag to 1, in this way
		# music doesn't restart when program restart
		self.__tryAgainFlagForMusic=1
		
		# we set button to begin game
		self.__buttonBegin()
		
		self.window.mainloop()
		
	def secondScreen(self,event=None):
		# this function begin the game and menage it
		
		self.serialObj.refresh=1
		# we save the user name
		self.__user = self.user_entry.get()
		
		### we destroy all old object, replace background and refresh music button
		# we destroy entry object
		self.user_entry.destroy()
		# we change background
		self.__setBackground(self.imageScreenTwo)
		# we refresh music button
		self.music.buttonRefresh()
		
		# we call serial menagment
		self.serialObj.start()
		# we set button that permit user to pass at thirtScreen
		self.__buttonStop()
		# we write welcome on screen
		self.__writeWelcome()
		# we set button used to start game
		self.__timeButton()
		# we start a continuously check of serial interface
		#self.window.after(0,self.serialObj.refreshPortsMenu)
		self.serialRefresh=threading.Thread(target=self.serialObj.refreshPortsMenu)
		self.serialRefresh.start()
		
		self.window.mainloop()
		
	def thirdScreen(self, event=None):
		# this function implement last screen, from this screen
		# user could exit or return to first screen
		
		self.serialObj.refresh=0
		self.circle.destroy()
		# we change background
		self.__setBackground(self.imageScreenThree)
		# we refresh music button
		self.music.buttonRefresh()
		# write best score
		self.__writeBestScore()
		# we display try again button
		self.__buttonTryAgain()
		# we display exit button
		self.__buttonExit()
		
		self.window.mainloop()
		
	#####################################################
	################ PRIVATE METHODS ####################
	
	####### GRAPHIC
	### SETUP
	def __setBackground(self, imageName):
		# this function set given image as background
		
		# we open image
		self.image = Image.open(self.imageDir+imageName)
		# if image hasn't correct dimension we must resize it
		if self.image.size != (self.widthRoot, self.heightRoot):
		    self.image = self.image.resize((self.widthRoot, self.heightRoot), Image.ANTIALIAS)
		
		self.image = ImageTk.PhotoImage(self.image)
		# we display image
		self.bgLabel = tk.Label(self.window, image = self.image)
		self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
		self.bgLabel.image = self.image
	
	### ENTRY
	def __adminEntry(self):
		# this function create admin entry in which user can set its username
		
		self.user_entry = Entry(self.window)
		self.user_entry.config(justify="center", font="times {0} italic".format(int(self.widthScreen*18/self.imageW)))
		self.user_entry.place(relx=.5, rely=.475, anchor=CENTER)
		self.user_entry.bind("<Return>", self.secondScreen)	

	
	###### BUTTONS
	
	## second screen buttons
	def __timeButton(self,event=None):
		# this function creates button in the centre of the screen and sets buttonToggle as function
		# to call when circle is pressed
		self.circle = Canvas(self.window,highlightthickness=0,bd=0,width=self.time_DimX, height=self.time_DimY,relief="raised")
		if self.flag_on:
			self.circleself=self.circle.create_image(self.time_DimX/2,self.time_DimY/2.01, image=self.photoRed, anchor='c')
		else:
			self.circleself=self.circle.create_image(self.time_DimX/2,self.time_DimY/2.01, image=self.photoGreen, anchor='c')
		self.window.update()
		self.circle.bind("<Button-1>", self.__buttonToggle)	
		self.circle.place(relx=.5, rely=.4,anchor=CENTER)
	
	def __buttonToggle(self,event=None):
		# this function toggles button and sends signal to serial
		if self.serialObj.serialIsDefined==1:
			self.circle.unbind("<Button-1>")
			if self.__toggle:
				self.__toggle=0
				self.__buttonOn()
			else:
				self.__toggle=1
				self.__buttonOff()
		#self.circle.bind("<Button-1>",self.__buttonToggle)
			
	def __buttonOn(self,event=None):
		# this function sends L0 to board and sets button on
		if self.flag_off == 1 and self.serialObj.serialIsDefined == 1:
			#print("button on")
			self.flag_off = 0	
			self.flag_on = 1
			self.circle.itemconfigure(self.circleself,image=self.photoGreenPressed) # the button change color
			self.window.update()
			#time.sleep(0.01)		
			rand_time=random.randint(self.minRandTime, self.maxRandTime)
			time.sleep(rand_time)
			self.circle.itemconfigure(self.circleself,image=self.photoRed) # the button change color
			self.window.update()
			self.serialObj.write(b'L0')
			self.__timeManage()
		
	def __buttonOff(self,event=None):	
		# this function send L1 to board and sets button off
		if self.flag_on == 1 and self.serialObj.serialIsDefined == 1:
			#print("button off")
			self.flag_off = 1
			self.flag_on = 0
			self.circle.itemconfigure(self.circleself,image=self.photoRedPressed) # the button change color
			self.window.update()
			#time.sleep(0.01)
			rand_time=random.randint(self.minRandTime, self.maxRandTime)
			time.sleep(rand_time)
			self.circle.itemconfigure(self.circleself,image=self.photoGreen) # the button change color
			self.window.update()
			self.serialObj.write(b'L1')
			self.__timeManage()
	
	def __buttonStop(self,event=None):
		# this function set button that could be uset to pass at the final screen
		self.stop_button = Button(self.window, image=self.photoStop, command=self.thirdScreen) 
		self.stop_button.config(width=self.stopDimX/self.widthScreen, height=self.stopDimY/self.heightScreen, bg="#64f4d2", bd=0, relief="raised", 
					highlightbackground="#64f4d2", activebackground="#f78ea2")
		self.stop_button.place(relx=.5, rely=.67, anchor=CENTER)	
	
	def __buttonBegin(self, event=None):
		self.begin_button = Button(self.window, image=self.photoBegin, command=self.secondScreen)
		self.begin_button.config(width=self.beginDimX, height=self.beginDimY, bg="#64f4d2", bd=0, relief="raised", 
					highlightbackground="#64f4d2", activebackground="#f78ea2")
		self.begin_button.place(relx=.51, rely=.65, anchor=CENTER)
	
	### third screen button	
	
	def __buttonTryAgain(self,event=None):
		# this function menage button used to rebegin program
		self.tryAgainButton = Canvas(self.window, highlightthickness=0,bd=0, width=self.tryAgainDimX, height=self.tryAgainDimY,relief="raised")
		self.tryAgainButtonself=self.tryAgainButton.create_image(self.tryAgainDimX/2,self.tryAgainDimY/2, image=self.photoTryAgain, anchor='c')	
		self.tryAgainButton.place(relx=.815, rely=.45,anchor=CENTER)
		self.tryAgainButton.bind("<Button-1>", self.__tryAgainMenage)
			
	def __buttonExit(self, event=None):
		self.exitButton = Button(self.window, image=self.photoExit, command=self.__ending) 
		self.exitButton.config(width=self.exitDimX, height=self.exitDimY, bg="#64f4d2", bd=0, relief="raised", 
				    highlightbackground="#64f4d2", activebackground="#f78ea2")
		self.exitButton.place(relx=.515, rely=.65, x=self.exitDimX/2, y=-(self.exitDimY)/2, anchor=NE)
	    
	def __ending(self, event=None):
		self.music.destroy()
		self.window.destroy()
	###### 	WRITING
	
	def __writeWelcome(self):
		# this fuction write welcome on screen
		self.welcomeCanvas = Canvas(self.window, highlightthickness=0, bd=0, width = self.widthRoot*self.welcW/self.imageW, 
					height=self.heightRoot*self.welcH/self.imageH,relief="raised")	
		self.welcomeCanvas.create_image((self.widthScreen*self.welcW/3)/self.imageW,(self.heightScreen*self.welcH/3)/self.imageH, image=self.welcomeImg, anchor='c')
		# 
		if self.__user=="":	
			self.welcomeCanvas.create_text(self.widthRoot*self.welcW/(2*self.imageW), self.heightRoot*self.welcH/(2.5*self.imageH), 
					text="Welcome !",font="MathJax_Math 15 bold",fill="#f0c448")
		else:
			self.welcomeCanvas.create_text(self.widthRoot*self.welcW/(2*self.imageW), self.heightRoot*self.welcH/(2.5*self.imageH), 
					text="Welcome, "+self.__user+"!",font="MathJax_Math 15 bold",fill="#f0c448")	
		self.welcomeCanvas.place(relx=.5, rely=.16, anchor=CENTER)
		
	def __writeBestScore(self):
		minPartialText = Text(self.window)

		if self.minPartial != self.minPartialInit:
			minPartialText.place(relx=.32, rely=.3)
			minPartialText.insert(END, " The best partial time: "+str(self.minPartial))
			minPartialText.config(state="disabled", font="times {0} italic".format(int(self.widthScreen*15/self.imageW)), fg="#efe26e", width=25, height=1, 
				relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
		else:
			minPartialText.place(relx=.33, rely=.3)
			minPartialText.insert(END, "  The best partial time: None")
			minPartialText.config(state="disabled", font="times {0} italic".format(int(self.widthScreen*15/self.imageW)), fg="#efe26e", width=24, height=1, 
				relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")

		minMeanText = Text(self.window)

		if self.minMean != self.minMeanInit:
			minMeanText.place(relx=.32, rely=.4)
			minMeanText.insert(END, 3*" "+"The best mean time: "+str("{0:.4f}".format(self.minMean)))
			minMeanText.config(state="disabled", font="times {0} italic".format(int(self.widthScreen*15/self.imageW)), fg="#efe26e", width=25, height=1, 
				relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
		else:
			minMeanText.place(relx=.33, rely=.4)
			minMeanText.insert(END, 3*" "+"The best mean time: None")
			minMeanText.config(state="disabled", font="times {0} italic".format(int(self.widthScreen*15/self.imageW)), fg="#efe26e", width=24, height=1, 
				relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
	
	
	######  MENAGE
	
	def __timeManage(self):
		# this function manage time data sent by board
		delay_time=int(self.serialObj.read(6)[1:6], 16)/1000 # the delay time is red from the

		# lists of times
		number_lenght = 11
		self.count = self.count+1
	
		# calculate the minimum reactive time of the user
		if self.minPartial>delay_time:
			self.minPartial=delay_time

		if self.count==8: # it deletes all the present times
			for i in range(1,8):
				self.text_user_l = Text(self.window)
				self.text_user_l.place(relx=.05, rely=i/11+0.07)
				self.text_user_l.insert(END, 2*" "+"N"+str(i)+":")	
				self.text_user_l.config(state="disabled", font="times 15 italic", fg="#efe26e", width=number_lenght, height=1, 
						relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
			self.count=1
		
		# we create text that display reaction time
		self.time_n = Text(self.window)
		self.time_n.place(relx=.05, rely=self.count/11+0.07)
		self.time_n.insert(END, 2*" "+"N"+str(self.count)+": "+str("{0:.4f}".format(delay_time)))	
		self.time_n.config(state="disabled", font="times 15 italic", fg="#efe26e", width=number_lenght, height=1, 
				relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
		self.tot=self.tot+delay_time
	
		#means		
		if self.count==7:
			self.meanYPos+=1
			self.mean=0
			self.mean=self.tot/self.count

			if self.minMean > self.mean: # calculate the minimum mean of the reactive time of the user
				minMean = self.mean

			self.mean_n = Text(self.window)
			self.mean_n.place(relx=.785, rely=self.meanYPos/11+0.07)
			self.mean_n.insert(END, 2*" "+"M"+str(self.meanYPos)+": "+str(self.mean))	
			self.mean_n.config(state="disabled", font="times 15 italic", fg="#efe26e", width=number_lenght, height=1, 
					relief=FLAT, bd=0, bg="#007972", highlightbackground="#64f4d2", highlightcolor="#007c74")
			self.tot=0
			if self.meanYPos==7:
				self.thirdScreen()

		self.circle.bind("<Button-1>", self.__buttonToggle)	
		
	def __tryAgainMenage(self, event=None):
		# this function change tryagainbutton image and restart program
		
		# we change try again photo
		self.tryAgainButton.itemconfigure(self.circleself, image=self.photoTryAgainPressed) # the button change color
		# we update window
		self.window.update()	
		# we sleep 100ms simulating button pressing
		time.sleep(0.1)
		# we reset board
		self.count = 0
		self.tot = 0
		self.meanYPos = 0
		self.minPartial = 100000
		self.minMean = 100000
		self.circle.destroy()
		self.firstScreen()

	
	####### SERIAL
	
	
	
	
	
	
	
screen = ReactionTimer("Img/", "firstscreen.png", "rootscreen.png", "finalscreen.png", "serial_window_bg.png")
screen.setTimeButtonImage("time_red_bg.png", "time_red_bg_pressed.png", "time_green_bg.png", "time_green_bg_pressed.png")
screen.setWelcomeImage("welcome.png", 600, 50)
screen.setStopImage("stop.png")
screen.setTryAgainImage("tryagain.png", "tryagain_pressed.png")
screen.setExitButton("exit.png")
screen.setBeginButton("begin.png")
screen.start()
	
	
	
	
