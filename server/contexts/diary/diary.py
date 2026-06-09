# -*- coding: utf-8 -*-
class DiaryNotFoundError(Exception):
    pass


class DiaryAccessError(Exception):
    pass


class DiaryService:
    def __init__(self):
        self._diaries = {}
        self._counter = 0

    def write(self, owner_id: str, title: str, content: str,
              public: bool = True) -> str:
        self._counter += 1
        diary_id = f"d_{self._counter}"
        self._diaries[diary_id] = {
            "diary_id": diary_id,
            "owner_id": owner_id,
            "title": title,
            "content": content,
            "public": public,
            "comments": [],
        }
        return diary_id

    def read(self, diary_id: str, requester_id: str) -> dict:
        entry = self._diaries.get(diary_id)
        if entry is None:
            raise DiaryNotFoundError(diary_id)
        if not entry["public"] and requester_id != entry["owner_id"]:
            raise DiaryAccessError(diary_id)
        return {**entry, "comments": list(entry["comments"])}

    def update(self, diary_id: str, owner_id: str, **kwargs) -> dict:
        entry = self._diaries.get(diary_id)
        if entry is None:
            raise DiaryNotFoundError(diary_id)
        if entry["owner_id"] != owner_id:
            raise PermissionError(owner_id)
        for k in ("title", "content", "public"):
            if k in kwargs:
                entry[k] = kwargs[k]
        return {**entry, "comments": list(entry["comments"])}

    def delete(self, diary_id: str, owner_id: str) -> None:
        entry = self._diaries.get(diary_id)
        if entry is None:
            raise DiaryNotFoundError(diary_id)
        if entry["owner_id"] != owner_id:
            raise PermissionError(owner_id)
        del self._diaries[diary_id]

    def add_comment(self, diary_id: str, author_id: str, content: str) -> int:
        """댓글 추가. 댓글 인덱스 반환."""
        entry = self._diaries.get(diary_id)
        if entry is None:
            raise DiaryNotFoundError(diary_id)
        entry["comments"].append({"author_id": author_id, "content": content})
        return len(entry["comments"]) - 1
