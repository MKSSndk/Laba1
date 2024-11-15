from typing import List
from Exceptions import PlaylistError

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.playlists: List['Playlist'] = []

    def create_playlist(self, name: str) -> 'Playlist':
        playlist = Playlist(
            playlist_id=len(self.playlists) + 1,
            name=name,
            owner=self
        )
        self.playlists.append(playlist)
        return playlist

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }

    @staticmethod
    def from_dict(data):
        user = User(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"]
        )
        user.playlists = [Playlist.from_dict(pl) for pl in data["playlists"]]
        return user


class Track:
    def __init__(self, track_id: int, title: str, duration: int):
        self.track_id = track_id
        self.title = title
        self.duration = duration

    def to_dict(self):
        return {
            "track_id": self.track_id,
            "title": self.title,
            "duration": self.duration
        }

    @staticmethod
    def from_dict(data):
        return Track(
            track_id=data["track_id"],
            title=data["title"],
            duration=data["duration"]
        )


class Playlist:
    def __init__(self, playlist_id: int, name: str, owner: User):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: List[Track] = []

    def add_track(self, track: Track):
        if track not in self.tracks:
            self.tracks.append(track)
        else:
            raise PlaylistError(f"Track '{track.title}' is already in the playlist.")

    def to_dict(self):
        return {
            "playlist_id": self.playlist_id,
            "name": self.name,
            "tracks": [track.to_dict() for track in self.tracks]
        }

    @staticmethod
    def from_dict(data):
        playlist = Playlist(
            playlist_id=data["playlist_id"],
            name=data["name"],
            owner=None
        )
        playlist.tracks = [Track.from_dict(t) for t in data["tracks"]]
        return playlist
