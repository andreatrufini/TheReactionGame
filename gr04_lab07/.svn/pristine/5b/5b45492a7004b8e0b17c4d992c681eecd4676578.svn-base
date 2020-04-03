import pygame
import threading
from tkinter import *
from PIL import Image, ImageTk
import time


class Music:
	# this class menage music in a gui using a button and an audio file
	# typical use:
	#	root=tk.Tk()
	#	musicObject=Music(root,"Img/","sound_on.png","sound_off.png","Music/", "InstantCrush.wav")
	#	musicObject.buttonDraw()
	#	musicObject.musicStart()
	#	...
	# 	# when you want to refresh button because screen change
	#	nusicObject.buttonRefresh()
	#
	# When you create an object of this class it manage all about stop and play music and so it is
	# an entity that interacts alone with user
	
	def __init__(self, window, imageDir, imageOn, imageOff, musicDir, musicName, relx=.965, rely=.05, dimx=25, dimy=25):
		# window: the name of the tk window in which work
		# imageDir: path in which the name of image will be search
		# imageOn: On image
		# imageOff: Off image
		# musicDir: path for music file
		# musicName: name of audio file
		# relx: relative position along x direction
		# rely: relative position along y direction
		# dimx: x dimension of displayed photo in pixel
		# dimy: y dimension of displayed photo in pixel
		
		self.window=window
		self.imageDir=imageDir
		self.imageOn=imageOn
		self.imageOff=imageOff
		self.musicDir=musicDir
		self.musicName=musicName
		self.relx=relx
		self.rely=rely
		self.dimx=dimx
		self.dimy=dimy
		self.__musicOnOff=1
		
		# we initialize ON image for music button
		self.__imageMusic = Image.open(self.imageDir+self.imageOn)
		self.__imageMusic = self.__imageMusic.resize((self.dimx,self.dimy), Image.ANTIALIAS)
		self.__photoMusic = ImageTk.PhotoImage(self.__imageMusic)
		
		# we initialize OFF image for music button
		self.__imageMusicStop = Image.open(self.imageDir+self.imageOff)
		self.__imageMusicStop = self.__imageMusicStop.resize((self.dimx,self.dimy), Image.ANTIALIAS)
		self.__photoMusicStop = ImageTk.PhotoImage(self.__imageMusicStop)
		
		self.musicStop=0
		
		# initialize pygame
		pygame.init()
	
	def __exit__(self):
	    self.musicStop=1
	    
	    
	
	######### PUBLIC METHOD  ###############################################################
	
	## MUSIC METHOD
	def destroy(self):
		 self.musicStop=1
	
	def musicStart(self):
		# this function start a thread in which music begin 
		# with a low volume and increase
		self.t=threading.Thread(target=self.__musicRising)
		self.t.start()

	
	## BUTTON METHOD
			
	def buttonDraw(self):
		# this function draw for the first time music button and set it properties
		
		# if button exist we delete it and redraw
		try:
			self.__musicButton.destroy()
			#print(self.__musicOnOff)
		except AttributeError:
			pass
	
		# we set proper image using __musicOnOff flag
		if self.__musicOnOff==1:
			self.__musicButton = Button(self.window, image=self.__photoMusic, command=self.__musicToggle) 
		else:
			self.__musicButton = Button(self.window, image=self.__photoMusicStop, command=self.__musicToggle) 
		
		# we configure button
		self.__musicButton.config(width=self.dimx, height=self.dimy, bg="#007972", bd=0, relief="raised", 
				highlightbackground="#007972", activebackground="#007972")
		self.__musicButton.place(relx=self.relx, rely=self.rely, x=self.relx/2, y=-(self.rely)/2, anchor=CENTER)
		self.window.update()
		
	def buttonRefresh(self):
		# this function sees if music is playing and it refreshes music image
		# dipendig on musicOnOff flag
		self.buttonDraw()
		self.window.update()
		
	########## PRIVATE METHOD  ################################################
	
	## MUSIC METHOD
	
	def __musicToggle(self):
		# this function toggle music when called
		# inverto il flag
		self.__musicOnOff = not self.__musicOnOff
		
		if self.__musicOnOff==0:
			# we switch off music
			pygame.mixer.music.pause()
			# we change music photo to off music
			self.buttonRefresh()
		else:
			# we turn off music
			pygame.mixer.music.unpause()
			# we change music image to on music  
			self.buttonRefresh()
	
	def __musicRising(self):
		# in this function we begin to play music and we rise it slowly
		pygame.mixer.music.load(self.musicDir+self.musicName)
		pygame.mixer.music.set_volume(0.05)
		pygame.mixer.music.play()
		time.sleep(1)
		for i in range(5,50):
			if self.musicStop != 1:
				pygame.mixer.music.set_volume(i/100)
				time.sleep(0.1)
			else:
				pygame.mixer.music.pause()
				break
			
			
			
			
			
			
