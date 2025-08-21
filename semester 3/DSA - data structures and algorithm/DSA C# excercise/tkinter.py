# Python code with a simple GUI using Tkinter for the Music Playlist Management System

import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"{self.title} by {self.artist}"

class PlaylistQueue:
    def __init__(self, name):
        self.name = name
        self.queue = []

    def add_song(self, song):
        self.queue.append(song)

    def remove_song(self):
        if not self.queue:
            return None
        return self.queue.pop(0)

    def get_playlist(self):
        return [str(song) for song in self.queue]

    def get_shuffled_playlist(self):
        shuffled = self.queue.copy()
        random.shuffle(shuffled)
        return [str(song) for song in shuffled]

class PlaylistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Playlist Manager")

        self.playlist = PlaylistQueue("My Playlist")

        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(root, text="Song Title:").grid(row=0, column=0)

        self.artist_entry = tk.Entry(root, width=30)
        self.artist_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(root, text="Artist Name:").grid(row=1, column=0)

        tk.Button(root, text="Add Song", command=self.add_song).grid(row=2, column=0, pady=5)
        tk.Button(root, text="Remove Song", command=self.remove_song).grid(row=2, column=1, pady=5)
        tk.Button(root, text="Play Sequential", command=self.play_sequential).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Play Shuffled", command=self.play_shuffled).grid(row=3, column=1, pady=5)

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_song(self):
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        if title and artist:
            song = Song(title, artist)
            self.playlist.add_song(song)
            self.update_playlist()
            self.title_entry.delete(0, tk.END)
            self.artist_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both title and artist.")

    def remove_song(self):
        removed = self.playlist.remove_song()
        if removed:
            messagebox.showinfo("Removed", f"Removed: {removed}")
            self.update_playlist()
        else:
            messagebox.showwarning("Remove Error", "Playlist is empty!")

    def play_sequential(self):
        self.listbox.delete(0, tk.END)
        for song in self.playlist.get_playlist():
            self.listbox.insert(tk.END, f"Now Playing: {song}")

    def play_shuffled(self):
        self.listbox.delete(0, tk.END)
        for song in self.playlist.get_shuffled_playlist():
            self.listbox.insert(tk.END, f"Now Playing: {song}")

    def update_playlist(self):
        self.listbox.delete(0, tk.END)
        for song in self.playlist.get_playlist():
            self.listbox.insert(tk.END, song)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()



