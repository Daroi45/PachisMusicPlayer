import vlc
import time
import os

class MusicPlayer():
	'''This class covers everything related
	to playing music.
	'''
	def __init__(self):
		'''Defines and instantiates attributes
		'''
		
		vlc_args = [
			'--no-xlib',
			'--quiet',
			'--no-video',
			'--network-caching=3000',
			'--file-caching=3000',
			'--live-caching=3000'
		]
		
		# vlc instance
		self.instance = vlc.Instance(vlc_args)
		self.player = self.instance.media_player_new()
		
		# Songs playlist
		self.playlist = []
		
		# Control index
		self.current_index = -1
		
		# Control variables
		self.current_file = None
		self.playing = False
		self.paused = False
		
		# Control list, takes a boolean value and a string
		self.label_file_control = []
		self.label_file_control.append(False)
		self.label_file_control.append(" ")

	def get_player(self):
		'''Return the player which
		provides methods such as playing
		music.
		
		Returns:
			object: self.player 
		'''
		return self.player
	
	def get_instance(self):
		'''Return the instance.
		
		Returns:
			object: self.instance
		'''
		return self.instance
	
	def get_playing(self):
		'''Return the playing.
		
		Returns:
			list: self.playing
		'''
		return self.playing
	
	def get_paused(self):
		'''Return the control varibale paused.
		
		Returns:
			boolean: self.paused
		'''
		return self.paused
	
	def get_playlist(self):
		'''Return the music playlist.
		
		Returns:
			list: self.playlist
		'''
		return self.playlist
	
	def set_playlist(self, playlist):
		'''Set a value to playlist.
		
		Args:
			playlist (list): new value
		'''
		self.playlist = playlist
	
	def get_label_file_control(self):
		'''Return the label file control text.
		
		Returns:
			string: self.label_file_control
		'''
		return self.label_file_control
	
	def load_song(self, index):
		'''This method is responsible
		for loading and playing songs.
		
		Args:
			index (int): song position
		'''
		if 0 <= index < len(self.playlist):
			self.current_index = index
			self.current_file = self.playlist[index]
			media = self.instance.media_new(self.current_file)
			self.player.set_media(media)
			self.play_song()
			
			tries = 0
			self.duration = 0
			while self.duration == 0 and tries < 30:
				self.duration = self.player.get_length() / 1000
				time.sleep(0.1)
				tries += 1

			'''
			Control variables
			'''
			self.playing = True
			self.paused = False

			self.label_file_control[0] = True
			self.label_file_control[1] = os.path.basename(self.current_file)
			
			self.updating_slider = True
			self.updating_slider = False
	
	def play_pause(self):
		'''This method is responsible for
		passing or playing the music
		'''
		if not self.playing:
			if self.current_file:
				self.play_song()
				self.playing = True
				self.paused = False
			elif self.playlist:
				self.load_song(0)
		elif self.paused:
			self.play_song()
			self.paused = False
		else:
			self.pause_song()
			self.paused = True
	
	def play_song(self):
		'''This is responsible for playing the music
		'''
		self.player.play()
	
	def pause_song(self):
		'''This is responsible for pause the music
		'''
		self.player.pause()
	
	def prev_song(self):
		'''Play a previus song
		'''
		if self.playlist:
			prev_index = (self.current_index - 1) % len(self.playlist)
			self.load_song(prev_index)
	
	def next_song(self):
		'''Play a next song
		'''
		if self.playlist:
			next_index = (self.current_index + 1) % len(self.playlist)
			self.load_song(next_index)
	
	def set_volume(self, val):
		'''Set the volume of the music
		'''
		volume = int(float(val))
		self.player.audio_set_volume(volume)
