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
        print(f"Added: {song}")

    def remove_song(self):
        if self.is_empty():
            print("Playlist is empty!")
            return None
        removed = self.queue.pop(0)
        print(f"Removed: {removed}")
        return removed

    def is_empty(self):
        return len(self.queue) == 0

    def display_playlist(self):
        if self.is_empty():
            print("Playlist is empty.")
        else:
            print(f"\nPlaylist '{self.name}':")
            for i, song in enumerate(self.queue, start=1):
                print(f"{i}. {song}")

    def play_sequential(self):
        print("\nPlaying playlist sequentially:")
        for song in self.queue:
            print(f"Now Playing: {song}")

    def play_shuffled(self):
        print("\nPlaying playlist in shuffled order:")
        shuffled = self.queue.copy()
        random.shuffle(shuffled)
        for song in shuffled:
            print(f"Now Playing: {song}")

# ----------- TEST CASES / DEMO -----------
def test_playlist_queue():
    print("Creating Playlist...\n")
    playlist = PlaylistQueue("My Favorite Songs")

    # Adding songs
    s1 = Song("Shape of You", "Ed Sheeran")
    s2 = Song("Blinding Lights", "The Weeknd")
    s3 = Song("Someone Like You", "Adele")
    s4 = Song("Levitating", "Dua Lipa")
    
    playlist.add_song(s1)
    playlist.add_song(s2)
    playlist.add_song(s3)
    playlist.add_song(s4)

    # Display playlist
    playlist.display_playlist()

    # Remove a song
    playlist.remove_song()
    playlist.display_playlist()

    # Play in order
    playlist.play_sequential()

    # Play shuffled
    playlist.play_shuffled()

# Run test
if __name__ == "__main__":
    test_playlist_queue()
