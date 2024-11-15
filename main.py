from typing import List
import json
import xml.etree.ElementTree as ET

class MusicServiceError(Exception):
    pass

class UserNotFoundError(MusicServiceError):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found.")


class TrackNotFoundError(MusicServiceError):
    def __init__(self, track_id: int):
        super().__init__(f"Track with ID {track_id} not found.")


class PlaylistError(MusicServiceError):
    def __init__(self, message: str):
        super().__init__(message)


class FileReadError(MusicServiceError):
    def __init__(self, filename: str):
        super().__init__(f"Error reading from file '{filename}'.")


class FileWriteError(MusicServiceError):
    def __init__(self, filename: str):
        super().__init__(f"Error writing to file '{filename}'.")

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

class MusicServiceCRUD:
    def __init__(self):
        self.users: List[User] = []
        self.tracks: List[Track] = []

    def create_user(self, user_id: int, name: str, email: str) -> User:
        user = User(user_id=user_id, name=name, email=email)
        self.users.append(user)
        return user

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise UserNotFoundError(user_id)

    def create_track(self, track_id: int, title: str, duration: int) -> Track:
        track = Track(track_id=track_id, title=title, duration=duration)
        self.tracks.append(track)
        return track

    def get_track(self, track_id: int) -> Track:
        for track in self.tracks:
            if track.track_id == track_id:
                return track
        raise TrackNotFoundError(track_id)

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        self.users.remove(user)
        print(f"Пользователь с ID {user_id} удалён.")

class JSONFileHandler:
    @staticmethod
    def save_to_file(filename: str, data: dict):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise FileWriteError(filename) from e

    @staticmethod
    def load_from_file(filename: str) -> dict:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise FileReadError(filename) from e


class XMLFileHandler:
    @staticmethod
    def save_to_file(filename: str, user: User):
        try:
            root = ET.Element("User", attrib={
                "id": str(user.user_id),
                "name": user.name,
                "email": user.email
            })
            for playlist in user.playlists:
                playlist_elem = ET.SubElement(
                    root, "Playlist",
                    attrib={"id": str(playlist.playlist_id), "name": playlist.name}
                )
                for track in playlist.tracks:
                    ET.SubElement(
                        playlist_elem, "Track",
                        attrib={
                            "id": str(track.track_id),
                            "title": track.title,
                            "duration": str(track.duration)
                        }
                    )
            tree = ET.ElementTree(root)
            tree.write(filename, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            raise FileWriteError(filename) from e

    @staticmethod
    def load_from_file(filename: str) -> User:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            user = User(
                user_id=int(root.attrib["id"]),
                name=root.attrib["name"],
                email=root.attrib["email"]
            )
            for playlist_elem in root.findall("Playlist"):
                playlist = Playlist(
                    playlist_id=int(playlist_elem.attrib["id"]),
                    name=playlist_elem.attrib["name"],
                    owner=user
                )
                for track_elem in playlist_elem.findall("Track"):
                    track = Track(
                        track_id=int(track_elem.attrib["id"]),
                        title=track_elem.attrib["title"],
                        duration=int(track_elem.attrib["duration"])
                    )
                    playlist.add_track(track)
                user.playlists.append(playlist)
            return user
        except Exception as e:
            raise FileReadError(filename) from e
