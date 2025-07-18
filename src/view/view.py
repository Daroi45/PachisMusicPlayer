from tkinter import ttk, Label, Button, Frame, filedialog, Toplevel, Text, DISABLED, CENTER
from tkinterdnd2 import DND_FILES, TkinterDnD
import webbrowser

import os
import threading
import time

import vlc

class View():
	'''This class is responsible for
	managing the interface
	'''
	def __init__(self, music_player, root):
		self.root = root
		self.music_player = music_player
	
	def initial_screen(self):
		'''This method displays all elements of the main
		screen
		'''
		self.root.title("Pachis Music Player")
		self.root.geometry("380x140")  # Un poco más alto para el texto
		self.root.resizable(False, False)

		# Label
		self.label_file = Label(
			self.root, 
			text="Sin archivo cargado", 
			anchor="w", 
			font=("Arial", 10)
		)
		self.label_file.pack(fill="x", padx=10, pady=5)

		# Scale
		self.time_scale = ttk.Scale(
			self.root, 
			from_=0, 
			to=100, 
			orient="horizontal", 
			command=self.on_seek
		)
		
		self.time_scale.pack(fill="x", padx=10)

		control_frame = Frame(self.root)
		control_frame.pack(pady=5)

		btn_width = 5  # más pequeño

		# Prev button
		self.btn_prev = Button(
			control_frame, 
			text="Anterior", 
			width=btn_width, 
			font=("Arial", 9), 
			command=self.music_player.prev_song
		)
		
		self.btn_prev.grid(row=0, column=0, padx=2)

		# Play button
		self.btn_play = Button(
			control_frame, 
			text="Play", 
			width=btn_width, 
			font=("Arial", 9), 
			command=self.music_player.play_pause
		)
		
		
		self.btn_play.grid(row=0, column=1, padx=2)

		# Next button
		self.btn_next = Button(
			control_frame, 
			text="Siguiente", 
			width=btn_width, 
			font=("Arial", 9), 
			command=self.music_player.next_song
		)
		
		self.btn_next.grid(row=0, column=2, padx=2)

		# Open button
		self.btn_open = Button(
			control_frame, text="Abrir", 
			width=btn_width, 
			font=("Arial", 9), 
			command=self.open_file
		)
		
		self.btn_open.grid(row=0, column=3, padx=2)

		# About button
		self.btn_about = Button(
			control_frame, 
			text="Acerca", 
			width=btn_width, 
			font=("Arial", 9), 
			command=self.show_about
		)
		
		self.btn_about.grid(row=0, column=4, padx=2)

		volume_frame = Frame(self.root)
		volume_frame.pack(pady=5, fill="x", padx=10)

		# Volume label
		Label(
			volume_frame, 
			text="Volumen", 
			font=("Arial", 9)
		).pack(side="left")
		
		self.volume_scale = ttk.Scale(
			volume_frame, 
			from_=0, 
			to=100, 
			value=100, 
			orient="horizontal", 
			command=self.music_player.set_volume
		)
		
		self.volume_scale.pack(side="left", fill="x", expand=True, padx=5)

		# Texto "No music no life" debajo de todo
		self.footer_label = Label(
			self.root, 
			text="Arrastra y suelta tu música. No music No life.", 
			font=("Arial", 9, "italic"), 
			fg="gray"
		)
		
		self.footer_label.pack(pady=(5,10))

		self.root.drop_target_register(DND_FILES)
		self.root.dnd_bind('<<Drop>>', self.drop)

		# Control variables
		self.duration = 0
		self.updating_slider = False

		# update_time thread
		self.update_thread = threading.Thread(target=self.update_time)
		self.update_thread.daemon = True
		self.update_thread.start()
	
	def update_text_button(self, text):
		'''Update the play button text.
		
		Args:
			text (string): Text to display
		
		'''
		self.btn_play.config(text=text)

	def update_label_file(self, text):
		'''Update the label_file text.
		
		Args:
			text (string): Text to display
		
		'''
		self.label_file.config(text=text)

	def update_time(self):
		'''It is responsible for updating
		the scale
		'''
		while True:
			if self.music_player.get_playing() and not self.music_player.get_paused():
				length = self.music_player.get_player().get_length()
				if length > 0:
					self.duration = length / 1000
					current_time = self.music_player.get_player().get_time() / 1000
					pos = (current_time / self.duration) * 100 if self.duration > 0 else 0
					self.updating_slider = True
					try:
						# updating the scale
						self.time_scale.set(pos)
					except:
						pass
					self.updating_slider = False
					state = self.music_player.get_player().get_state()
					if state == vlc.State.Ended:
						self.music_player.next_song()
			time.sleep(0.3)

	def open_file(self):
		'''This method is responsible for opening
		the file manager.
		'''
		filenames = filedialog.askopenfilenames(
			title="Selecciona archivos de audio",
			filetypes=[("Archivos de audio", "*.mp3 *.ogg *.wav *.flac")]
		)
		if filenames:
			self.music_player.set_playlist(list(filenames)) 
			self.music_player.load_song(0)

	def on_seek(self, val):
		if self.duration > 0 and not self.updating_slider:
			seek_time = float(val) * self.duration / 100
			self.music_player.get_player().set_time(int(seek_time * 1000))

	def drop(self, event):
		'''Set the audio_files in the playlist.
		'''
		files = self.root.tk.splitlist(event.data)
		audio_files = [f for f in files if f.lower().endswith(('.mp3', '.ogg', '.wav', '.flac'))]
		if audio_files:
			self.music_player.set_playlist(audio_files)
			self.music_player.load_song(0)

	def show_about(self):
		'''About tab
		'''
		about_win = Toplevel(self.root)
		about_win.title("Acerca de")
		about_win.geometry("360x140")
		about_win.resizable(False, False)

		txt = Text(about_win, wrap="word", height=7, width=48, font=("Arial", 10))
		txt.pack(padx=10, pady=10)

		about_text = (
			'Este Reproductor de música "Pachis Music Player" fue creado por Israel G. Bistrain y Pachi.\n'
			"Puedes seguirnos en Mastodon: "
		)
		txt.insert("1.0", about_text)

		# Open the web browser
		def open_link(event):
			webbrowser.open_new("https://mastodon.social/@supersnufkin")

		start_index = txt.index("end-1c")
		txt.insert("end", "@supersnufkin@mastodon.social")
		end_index = txt.index("end-1c")

		txt.tag_add("link", start_index, end_index)
		txt.tag_config("link", foreground="blue", underline=1)
		txt.tag_bind("link", "<Button-1>", open_link)

		txt.config(state=DISABLED)

	def set_text_button(self, text):
		'''Update text button
		
		Args:
			text (string): text to display
		'''
		self.btn_play.config(text=text)












