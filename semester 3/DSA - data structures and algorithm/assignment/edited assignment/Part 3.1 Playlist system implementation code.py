import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Queue ADT Implementation
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[0] if not self.is_empty() else None

    def get_all_songs(self):
        return self.items.copy()

    def shuffle(self):
        random.shuffle(self.items)

# GUI using Tkinter
class PlaylistApp:
    def __init__(self, master):
        self.master = master
        master.title("Music Playlist Management System")
        master.geometry("500x400")
        master.config(bg="#ececec")

        self.playlist = Queue()

        self.label = tk.Label(master, text="Music Playlist", font=("Arial", 16), bg="#ececec")
        self.label.pack(pady=10)

        self.song_listbox = tk.Listbox(master, width=50, height=10)
        self.song_listbox.pack(pady=10)

        self.add_button = tk.Button(master, text="Add Song", command=self.add_song)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(master, text="Remove Song", command=self.remove_song)
        self.remove_button.pack(pady=5)

        self.play_button = tk.Button(master, text="Play Playlist (Sequential)", command=self.play_playlist)
        self.play_button.pack(pady=5)

        self.shuffle_button = tk.Button(master, text="Shuffle Playlist", command=self.shuffle_playlist)
        self.shuffle_button.pack(pady=5)

        self.refresh_button = tk.Button(master, text="Refresh Playlist View", command=self.refresh_listbox)
        self.refresh_button.pack(pady=5)

    def add_song(self):
        song = simpledialog.askstring("Add Song", "Enter song name:")
        if song:
            self.playlist.enqueue(song)
            self.refresh_listbox()

    def remove_song(self):
        if not self.playlist.is_empty():
            removed = self.playlist.dequeue()
            messagebox.showinfo("Removed Song", f"Removed: {removed}")
            self.refresh_listbox()
        else:
            messagebox.showwarning("Warning", "The playlist is empty!")

    def play_playlist(self):
        if self.playlist.is_empty():
            messagebox.showwarning("Warning", "No songs to play!")
        else:
            songs = self.playlist.get_all_songs()
            messagebox.showinfo("Playing Playlist", "\n".join(songs))

    def shuffle_playlist(self):
        self.playlist.shuffle()
        self.refresh_listbox()

    def refresh_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for song in self.playlist.get_all_songs():
            self.song_listbox.insert(tk.END, song)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()
