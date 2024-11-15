from CRUD import MusicServiceCRUD
from BaseClasses import User
from FileHandler import JSONFileHandler, XMLFileHandler
from Exceptions import MusicServiceError, TrackNotFoundError, PlaylistError, UserNotFoundError, FileReadError

if __name__ == "__main__":
    crud = MusicServiceCRUD()

    try:
        # Пример создания пользователя
        user = crud.create_user(1, "Alice", "alice@example.com")
        print("Пользователь создан:", user.to_dict())

        # Пример создания трека
        track1 = crud.create_track(1, "Song One", 300)
        track2 = crud.create_track(2, "Song Two", 250)
        print("Треки созданы:", [track1.to_dict(), track2.to_dict()])

        # Пример добавления трека в плейлист
        playlist = user.create_playlist("My Playlist")
        playlist.add_track(track1)
        playlist.add_track(track2)
        print("Плейлист создан:", playlist.to_dict())

        # Пример сохранения данных в JSON
        JSONFileHandler.save_to_file("user_data.json", user.to_dict())
        print("Данные сохранены в файл user_data.json")

        # Пример загрузки данных из JSON
        loaded_data = JSONFileHandler.load_from_file("user_data.json")
        loaded_user = User.from_dict(loaded_data)
        print("Данные загружены из файла JSON:", loaded_user.to_dict())

        # Пример сохранения данных в XML
        XMLFileHandler.save_to_file("user_data.xml", user)
        print("Данные сохранены в файл user_data.xml")

        # Пример загрузки данных из XML
        loaded_user_xml = XMLFileHandler.load_from_file("user_data.xml")
        print("Данные загружены из файла XML:", loaded_user_xml.to_dict())

        # Пример попытки загрузить несуществующий трек
        try:
            non_existent_track = crud.get_track(999)
        except TrackNotFoundError as e:
            print(f"Исключение обработано: {e}")

        # Пример попытки добавить трек, который уже существует в плейлисте
        try:
            playlist.add_track(track1)
        except PlaylistError as e:
            print(f"Исключение обработано: {e}")

        # Пример попытки удалить несуществующего пользователя
        try:
            crud.delete_user(999)
        except UserNotFoundError as e:
            print(f"Исключение обработано: {e}")

        # Пример попытки загрузить данные из несуществующего файла
        try:
            JSONFileHandler.load_from_file("nonexistent.json")
        except FileReadError as e:
            print(f"Исключение обработано: {e}")

    except MusicServiceError as e:
        print(f"Общая ошибка музыкального сервиса: {e}")

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
