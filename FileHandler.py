import json
import xml.etree.ElementTree as ET
from BaseClasses import User, Playlist, Track
from Exceptions import FileReadError, FileWriteError

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
