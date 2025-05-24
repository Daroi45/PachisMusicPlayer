import os
import threading
import time
import webbrowser
import vlc
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk, Label, Button, Frame, filedialog, Toplevel, Text, DISABLED, CENTER

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pachis Music Player")
        self.root.geometry("380x140")  # Un poco más alto para el texto
        self.root.resizable(False, False)

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

        self.current_file = None
        self.playing = False
        self.paused = False

        self.playlist = []
        self.current_index = -1

        self.label_file = Label(root, text="Sin archivo cargado", anchor="w", font=("Arial", 10))
        self.label_file.pack(fill="x", padx=10, pady=5)

        self.time_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=self.on_seek)
        self.time_scale.pack(fill="x", padx=10)

        control_frame = Frame(root)
        control_frame.pack(pady=5)

        btn_width = 5  # más pequeño

        self.btn_prev = Button(control_frame, text="Anterior", width=btn_width, font=("Arial", 9), command=self.prev_song)
        self.btn_prev.grid(row=0, column=0, padx=2)

        self.btn_play = Button(control_frame, text="Play", width=btn_width, font=("Arial", 9), command=self.play_pause)
        self.btn_play.grid(row=0, column=1, padx=2)

        self.btn_next = Button(control_frame, text="Siguiente", width=btn_width, font=("Arial", 9), command=self.next_song)
        self.btn_next.grid(row=0, column=2, padx=2)

        self.btn_open = Button(control_frame, text="Abrir", width=btn_width, font=("Arial", 9), command=self.open_file)
        self.btn_open.grid(row=0, column=3, padx=2)

        self.btn_about = Button(control_frame, text="Acerca", width=btn_width, font=("Arial", 9), command=self.show_about)
        self.btn_about.grid(row=0, column=4, padx=2)

        volume_frame = Frame(root)
        volume_frame.pack(pady=5, fill="x", padx=10)

        Label(volume_frame, text="Volumen", font=("Arial", 9)).pack(side="left")
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, value=100, orient="horizontal", command=self.set_volume)
        self.volume_scale.pack(side="left", fill="x", expand=True, padx=5)

        # Texto "No music no life" debajo de todo
        self.footer_label = Label(root, text="Arrastra y suelta tu música. No music No life.", font=("Arial", 9, "italic"), fg="gray")
        self.footer_label.pack(pady=(5,10))
        

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        self.duration = 0
        self.updating_slider = False

        self.update_thread = threading.Thread(target=self.update_time)
        self.update_thread.daemon = True
        self.update_thread.start()

    def load_song(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            self.current_file = self.playlist[index]
            media = self.instance.media_new(self.current_file)
            self.player.set_media(media)
            self.player.play()

            tries = 0
            self.duration = 0
            while self.duration == 0 and tries < 30:
                self.duration = self.player.get_length() / 1000
                time.sleep(0.1)
                tries += 1

            self.playing = True
            self.paused = False
            self.btn_play.config(text="Pausa")
            self.label_file.config(text=os.path.basename(self.current_file))
            self.updating_slider = True
            self.time_scale.set(0)
            self.updating_slider = False

    def play_pause(self):
        if not self.playing:
            if self.current_file:
                self.player.play()
                self.playing = True
                self.paused = False
                self.btn_play.config(text="Pausa")
            elif self.playlist:
                self.load_song(0)
        elif self.paused:
            self.player.play()
            self.paused = False
            self.btn_play.config(text="Pausa")
        else:
            self.player.pause()
            self.paused = True
            self.btn_play.config(text="Play")

    def next_song(self):
        if self.playlist:
            next_index = (self.current_index + 1) % len(self.playlist)
            self.load_song(next_index)

    def prev_song(self):
        if self.playlist:
            prev_index = (self.current_index - 1) % len(self.playlist)
            self.load_song(prev_index)

    def open_file(self):
        filenames = filedialog.askopenfilenames(title="Selecciona archivos de audio",
                                                filetypes=[("Archivos de audio", "*.mp3 *.ogg *.wav *.flac")])
        if filenames:
            self.playlist = list(filenames)
            self.load_song(0)

    def set_volume(self, val):
        volume = int(float(val))
        self.player.audio_set_volume(volume)

    def on_seek(self, val):
        if self.duration > 0 and not self.updating_slider:
            seek_time = float(val) * self.duration / 100
            self.player.set_time(int(seek_time * 1000))

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
                        self.time_scale.set(pos)
                    except:
                        pass
                    self.updating_slider = False
                    state = self.player.get_state()
                    if state == vlc.State.Ended:
                        self.next_song()
            time.sleep(0.3)

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        audio_files = [f for f in files if f.lower().endswith(('.mp3', '.ogg', '.wav', '.flac'))]
        if audio_files:
            self.playlist = audio_files
            self.load_song(0)

    def show_about(self):
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

        def open_link(event):
            webbrowser.open_new("https://mastodon.social/@supersnufkin")

        start_index = txt.index("end-1c")
        txt.insert("end", "@supersnufkin@mastodon.social")
        end_index = txt.index("end-1c")

        txt.tag_add("link", start_index, end_index)
        txt.tag_config("link", foreground="blue", underline=1)
        txt.tag_bind("link", "<Button-1>", open_link)

        txt.config(state=DISABLED)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = MusicPlayer(root)
    root.mainloop()

