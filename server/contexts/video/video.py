# -*- coding: utf-8 -*-
class VideoNotFoundError(Exception):
    pass


class VideoService:
    def __init__(self):
        self._videos = {}
        self._counter = 0

    def add_video(self, user_id: str, title: str,
                  description: str = "",
                  thumbnail_url: str = "/static/images/profile.jpg") -> dict:
        self._counter += 1
        video_id = f"vid_{self._counter}"
        self._videos[video_id] = {
            "video_id": video_id,
            "owner_id": user_id,
            "title": title,
            "description": description,
            "thumbnail_url": thumbnail_url,
        }
        return dict(self._videos[video_id])

    def list_videos(self, user_id: str) -> list:
        return [
            dict(v) for v in self._videos.values()
            if v["owner_id"] == user_id
        ]

    def get_video(self, video_id: str) -> dict:
        if video_id not in self._videos:
            raise VideoNotFoundError(video_id)
        return dict(self._videos[video_id])

    def delete_video(self, user_id: str, video_id: str) -> None:
        v = self._videos.get(video_id)
        if v is None:
            raise VideoNotFoundError(video_id)
        if v["owner_id"] != user_id:
            raise PermissionError(user_id)
        del self._videos[video_id]
