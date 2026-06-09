# -*- coding: utf-8 -*-
from server.shared.idem import IdempotencyStore, idempotency_key


class SecretEntryError(Exception):
    pass


class EntryNotFoundError(Exception):
    pass


class GuestbookService:
    def __init__(self):
        self._entries = {}      # entry_id → entry dict
        self._counter = 0
        self._idem = IdempotencyStore()

    def write(self, hompy_id: str, author_id: str, content: str,
              secret: bool = False, idem_payload: dict = None) -> tuple[str, bool]:
        """글 작성. (entry_id, is_replay) 반환."""
        key = idempotency_key(idem_payload) if idem_payload else None

        def _create():
            self._counter += 1
            entry_id = f"gb_{self._counter}"
            self._entries[entry_id] = {
                "entry_id": entry_id,
                "hompy_id": hompy_id,
                "author_id": author_id,
                "content": content,
                "secret": secret,
            }
            return entry_id

        if key:
            return self._idem.issue_once(key, _create)
        return _create(), False

    def read_entry(self, entry_id: str, requester_id: str) -> dict:
        entry = self._entries.get(entry_id)
        if entry is None:
            raise EntryNotFoundError(entry_id)
        if entry["secret"] and requester_id not in (entry["author_id"], entry["hompy_id"]):
            raise SecretEntryError(entry_id)
        return dict(entry)

    def list_entries(self, hompy_id: str, requester_id: str = None) -> list[dict]:
        result = []
        for e in self._entries.values():
            if e["hompy_id"] != hompy_id:
                continue
            if e["secret"] and requester_id not in (e["author_id"], hompy_id):
                result.append({**e, "content": "비밀글입니다."})
            else:
                result.append(dict(e))
        return result

    def delete(self, entry_id: str, requester_id: str) -> None:
        """홈피 주인(requester = hompy_id)만 삭제 가능."""
        entry = self._entries.get(entry_id)
        if entry is None:
            raise EntryNotFoundError(entry_id)
        if requester_id != entry["hompy_id"]:
            raise PermissionError(f"{requester_id} cannot delete {entry_id}")
        del self._entries[entry_id]
