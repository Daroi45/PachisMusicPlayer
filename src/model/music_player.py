import vlc
import time
import os

class MusicPlayer():
	def __init__(self):
		vlc_args = [
			'--no-xlib',
			'--quiet',
			'--no-video',
			'--network-caching=3000',
			'--file-caching=3000',
			'--live-caching=3000'
		]
		self.instance = vlc.Instance(vlc_args)
		self.player = self.instance.media_player_new()
		
		self.playlist = []
		self.current_index = -1
		
		self.current_file = None
		self.playing = False
		self.paused = False
		
		self.label_file_control = []
		self.label_file_control.append(False)
		self.label_file_control.append(" ")

	def get_player(self):
		return self.player
	
	def get_instance(self):
		return self.instance
	
	def get_playing(self):
		return self.playing
	
	def get_paused(self):
		return self.paused
	
	def get_playlist(self):
		return self.playlist
	
	def get_label_file_control(self):
		return self.label_file_control
	
	def set_playlist(self, playlist):
		self.playlist = playlist
	
	def load_song(self, index):
		if 0 <= index < len(self.playlist):
			self.current_index = index
			self.current_file = self.playlist[index]
			media = self.instance.media_new(self.current_file)
			self.player.set_media(media)
			self.play_song()
			#self.player.play()

			tries = 0
			self.duration = 0
			while self.duration == 0 and tries < 30:
				self.duration = self.player.get_length() / 1000
				time.sleep(0.1)
				tries += 1

			self.playing = True
			self.paused = False
			#self.btn_play.config(text="Pausa")
			#self.label_file.config(text=os.path.basename(self.current_file)) # Arreglar
			
			self.label_file_control[0] = True
			self.label_file_control[1] = os.path.basename(self.current_file)
			
			self.updating_slider = True
			#self.time_scale.set(0) # Arreglar
			self.updating_slider = False
	
	def play_pause(self):
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
		self.player.play()
	
	def pause_song(self):
		self.player.pause()
	
	def prev_song(self):
		if self.playlist:
			prev_index = (self.current_index - 1) % len(self.playlist)
			self.load_song(prev_index)
	
	def next_song(self):
		if self.playlist:
			next_index = (self.current_index + 1) % len(self.playlist)
			self.load_song(next_index)
	
	def set_volume(self, val):
		volume = int(float(val))
		self.player.audio_set_volume(volume)


	def update_time(self):
		while True:
			if self.playing and not self.paused:
				length = self.player.get_length()
				if length > 0:
					self.duration = length / 1000
					current_time = self.player.get_time() / 1000
					pos = (current_time / self.duration) * 100 if self.duration > 0 else 0
					self.updating_slider = True
					try:
						self.time_scale.set(pos) # arreglar
					except:
						pass
					self.updating_slider = False
					state = self.player.get_state()
					if state == vlc.State.Ended:
						self.next_song()
			time.sleep(0.3)









