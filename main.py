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
