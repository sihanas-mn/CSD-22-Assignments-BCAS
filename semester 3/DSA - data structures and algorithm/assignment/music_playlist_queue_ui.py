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

def run_ui():
    print("🎵 Welcome to Music Playlist Manager 🎵")
    name = input("Enter the name of your playlist: ")
    playlist = PlaylistQueue(name)

    while True:
        print("\nOptions:")
        print("1. Add Song")
        print("2. Remove Song")
        print("3. Display Playlist")
        print("4. Play Sequentially")
        print("5. Play Shuffled")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            title = input("Enter song title: ")
            artist = input("Enter artist name: ")
            playlist.add_song(Song(title, artist))

        elif choice == '2':
            playlist.remove_song()

        elif choice == '3':
            playlist.display_playlist()

        elif choice == '4':
            playlist.play_sequential()

        elif choice == '5':
            playlist.play_shuffled()

        elif choice == '6':
            print("Thank you for using Music Playlist Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

# Run the interface
if __name__ == "__main__":
    run_ui()