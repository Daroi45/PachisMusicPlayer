from view.view import View
from model.music_player import MusicPlayer
import threading
import time

class Presenter():
	def __init__(self, root):
		self.music_player = MusicPlayer()
		self.view = View(self.music_player, root)
		
		self.start()
		
		self.update_thread = threading.Thread(target=self.update_button)
		self.update_thread.daemon = True
		self.update_thread.start()
		
		self.update_thread = threading.Thread(target=self.update_label)
		self.update_thread.daemon = True
		self.update_thread.start()

	def start(self):
		self.view.initial_screen()
		
	def update_button(self):
		while(True):
			if self.music_player.get_paused():
				self.view.update_text_button("Play")
			else:
				self.view.update_text_button("Pausa")
			time.sleep(0.3)
	
	def update_label(self):
		while(True):
			if self.music_player.get_label_file_control()[0]:
				self.view.update_label_file(
					self.music_player.get_label_file_control()[1]
				)
			time.sleep(0.3)










