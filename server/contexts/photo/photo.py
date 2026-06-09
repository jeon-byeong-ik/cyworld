# -*- coding: utf-8 -*-
class AlbumNotFoundError(Exception):
    pass


class PhotoNotFoundError(Exception):
    pass


class PhotoService:
    def __init__(self):
        self._albums = {}
        self._photos = {}
        self._album_counter = 0
        self._photo_counter = 0

    def create_album(self, user_id: str, name: str) -> dict:
        self._album_counter += 1
        album_id = f"alb_{self._album_counter}"
        self._albums[album_id] = {
            "album_id": album_id,
            "owner_id": user_id,
            "name": name,
        }
        return dict(self._albums[album_id])

    def list_albums(self, user_id: str) -> list:
        albums = [
            {**a, "photo_count": sum(
                1 for p in self._photos.values()
                if p["owner_id"] == user_id and p["album_id"] == a["album_id"]
            )}
            for a in self._albums.values()
            if a["owner_id"] == user_id
        ]
        return albums

    def add_photo(self, user_id: str, album_id: str,
                  title: str, description: str = "",
                  img_url: str = "/static/images/profile.jpg") -> dict:
        if album_id not in self._albums:
            raise AlbumNotFoundError(album_id)
        self._photo_counter += 1
        photo_id = f"ph_{self._photo_counter}"
        self._photos[photo_id] = {
            "photo_id": photo_id,
            "owner_id": user_id,
            "album_id": album_id,
            "title": title,
            "description": description,
            "img_url": img_url,
        }
        return dict(self._photos[photo_id])

    def list_photos(self, user_id: str, album_id: str = None) -> list:
        return [
            dict(p) for p in self._photos.values()
            if p["owner_id"] == user_id
            and (album_id is None or p["album_id"] == album_id)
        ]

    def get_photo(self, photo_id: str) -> dict:
        if photo_id not in self._photos:
            raise PhotoNotFoundError(photo_id)
        return dict(self._photos[photo_id])

    def delete_photo(self, user_id: str, photo_id: str) -> None:
        p = self._photos.get(photo_id)
        if p is None:
            raise PhotoNotFoundError(photo_id)
        if p["owner_id"] != user_id:
            raise PermissionError(user_id)
        del self._photos[photo_id]
