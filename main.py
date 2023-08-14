import tkinter as tk
from tkinter import filedialog
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.current_song_index = 0
        self.init_ui()
        self.init_audio()

    def init_ui(self):
        self.root.configure(bg="light blue")

        # Create top navigation bar
        top_nav_frame = tk.Frame(self.root, bg="light blue")

        # Create top navigation bar
        self.add_button = tk.Button(top_nav_frame, text="Add Song", command=self.add_song , bg="midnight blue" ,fg="white")
        self.delete_button = tk.Button(top_nav_frame, text="Delete Song", command=self.delete_song , bg="midnight blue" ,fg="white")
        self.add_button.pack(side=tk.LEFT)
        self.delete_button.pack(side=tk.LEFT)
        top_nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.playlist = tk.Listbox(self.root, bg="light blue")
        self.playlist.pack(fill=tk.BOTH, expand=True)

        # Create bottom navigation bar
        bottom_nav_frame = tk.Frame(self.root, bg="light blue")
        self.play_button = tk.Button(bottom_nav_frame, text="Play", command=self.play , bg="midnight blue" ,fg="white")
        self.pause_button = tk.Button(bottom_nav_frame, text="Pause", command=self.pause , bg="midnight blue" ,fg="white")
        self.resume_button = tk.Button(bottom_nav_frame, text="Resume", command=self.resume , bg="midnight blue" ,fg="white")
        self.next_button = tk.Button(bottom_nav_frame, text="Next", command=self.next_song , bg="midnight blue" ,fg="white")
        self.prev_button = tk.Button(bottom_nav_frame, text="Previous", command=self.prev_song , bg="midnight blue" ,fg="white")
        self.restart_button = tk.Button(bottom_nav_frame, text="Restart", command=self.restart_song , bg="midnight blue" ,fg="white")
        self.play_button.pack(side=tk.LEFT)
        self.pause_button.pack(side=tk.LEFT)
        self.resume_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.prev_button.pack(side=tk.LEFT)
        self.restart_button.pack(side=tk.LEFT)
        bottom_nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        buttons = [self.add_button, self.delete_button, self.play_button,
                   self.pause_button, self.resume_button, self.next_button, self.prev_button, self.restart_button]

        for button in buttons:
            button.bind("<Enter>", lambda event, button=button: self.on_hover_enter(event, button))
            button.bind("<Leave>", lambda event, button=button: self.on_hover_leave(event, button))

    def on_hover_enter(self, event, button):
        button.config(bg="orange", fg="black")

    def on_hover_leave(self, event, button):
        button.config(bg="midnight blue", fg="white")


    def init_audio(self):
        pygame.mixer.init()
        self.playing = False
        self.paused = False
        self.playlist_data = []

    #method for adding song files
    def add_song(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3")])
        if file_paths:
            self.playlist_data.extend(file_paths)
            self.update_playlist_display()

    #method when delete or add is pressed, files are shown
    def update_playlist_display(self):
        self.playlist.delete(0, tk.END)
        for song_path in self.playlist_data:
            song_filename = os.path.basename(song_path)
            self.playlist.insert(tk.END, song_filename)

   #method of deleting files
    def delete_song(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            index_to_delete = selected_index[0]
            del self.playlist_data[index_to_delete]
            self.update_playlist_display()

    #method of playing songs
    def play(self):
        selected_index = self.playlist.curselection()
        if not self.playing and self.playlist_data:
            if selected_index:
                index_to_play = selected_index[0]
            else:
                index_to_play = 0

            song_to_play = self.playlist_data[index_to_play]
            pygame.mixer.music.load(song_to_play)
            pygame.mixer.music.play()
            self.playing = True
            self.playlist.itemconfig(index_to_play, {'bg': 'orange', 'fg': 'black'})
            self.currently_playing_index = index_to_play

   #pausing songs
    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    #resuming songs
    def resume(self):
        if self.playing and self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    #methods for next and previous buttons
    def next_song(self):
        if self.playing:
            pygame.mixer.music.stop()
            if hasattr(self, 'currently_playing_index'):
                self.playlist.itemconfig(self.currently_playing_index, {'bg': 'white', 'fg': 'black'})
        if self.playlist_data:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist_data)
            song_to_play = self.playlist_data[self.current_song_index]
            pygame.mixer.music.load(song_to_play)
            pygame.mixer.music.play()
            self.playing = True
            self.currently_playing_index = self.current_song_index
            self.playlist.itemconfig(self.currently_playing_index, {'bg': 'orange', 'fg': 'black'})

    def prev_song(self):
        if self.playing:
            pygame.mixer.music.stop()
            if hasattr(self, 'currently_playing_index'):
                self.playlist.itemconfig(self.currently_playing_index, {'bg': 'white', 'fg': 'black'})
                self.current_song_index = (self.current_song_index - 1) % len(self.playlist_data)
                self.currently_playing_index = self.current_song_index
                song_to_play = self.playlist_data[self.current_song_index]
                pygame.mixer.music.load(song_to_play)
                pygame.mixer.music.play()
                self.playlist.itemconfig(self.currently_playing_index, {'bg': 'orange', 'fg': 'black'})

    def restart_song(self):
        if self.playing:
            pygame.mixer.music.rewind()


def main():
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.geometry("310x400")
    root.mainloop()

if __name__ == "__main__":
    main()
