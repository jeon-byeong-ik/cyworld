# -*- coding: utf-8 -*-
class ProfileNotFoundError(Exception):
    pass


class ProfileService:
    def __init__(self):
        self._store = {}

    def register(self, user_id: str, nickname: str, intro: str = "", skin: str = "default") -> dict:
        profile = {
            "user_id": user_id,
            "nickname": nickname,
            "intro": intro,
            "skin": skin,
        }
        self._store[user_id] = profile
        return profile

    def get(self, user_id: str) -> dict:
        if user_id not in self._store:
            raise ProfileNotFoundError(user_id)
        return dict(self._store[user_id])

    def update(self, user_id: str, **kwargs) -> dict:
        if user_id not in self._store:
            raise ProfileNotFoundError(user_id)
        allowed = {"nickname", "intro", "skin"}
        for k, v in kwargs.items():
            if k in allowed:
                self._store[user_id][k] = v
        return dict(self._store[user_id])
