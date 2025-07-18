from view.view import View
from model.music_player import MusicPlayer
import threading
import time

class Presenter():
	'''Conect the model to the view
	'''
	def __init__(self, root):
		'''Initializes the model and view and
		connects them.
		'''
		self.music_player = MusicPlayer()
		self.view = View(self.music_player, root)
		
		self.start()
		
		# update_button thread
		self.update_thread = threading.Thread(target=self.update_button)
		self.update_thread.daemon = True
		self.update_thread.start()
		
		# update_label thread
		self.update_thread = threading.Thread(target=self.update_label)
		self.update_thread.daemon = True
		self.update_thread.start()

	def start(self):
		'''Start the main screen
		'''
		self.view.initial_screen()
		
	def update_button(self):
		'''This method is responsible of
		update the play button depending on
		the information from the control variables.
		'''
		while(True):
			if self.music_player.get_paused():
				self.view.update_text_button("Play")
			else:
				self.view.update_text_button("Pausa")
			time.sleep(0.3)
	
	def update_label(self):
		'''This method is responsible of
		update the file_control label depending on
		the information from the control variables.
		'''
		while(True):
			if self.music_player.get_label_file_control()[0]:
				self.view.update_label_file(
					self.music_player.get_label_file_control()[1]
				)
			time.sleep(0.3)
