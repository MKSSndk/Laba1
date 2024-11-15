from typing import List
from BaseClasses import User, Track
from Exceptions import UserNotFoundError, TrackNotFoundError

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
