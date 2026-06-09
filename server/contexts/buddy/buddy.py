# -*- coding: utf-8 -*-
class AlreadyBuddyError(Exception):
    pass


class BuddyRequestNotFoundError(Exception):
    pass


class BuddyService:
    def __init__(self):
        # key: frozenset({a, b}) → {"from_id": str, "to_id": str, "status": str}
        self._relations = {}

    def _key(self, a: str, b: str) -> frozenset:
        return frozenset({a, b})

    def request(self, from_id: str, to_id: str) -> None:
        k = self._key(from_id, to_id)
        if k in self._relations and self._relations[k]["status"] == "ACCEPTED":
            raise AlreadyBuddyError(f"{from_id} ↔ {to_id}")
        self._relations[k] = {"from_id": from_id, "to_id": to_id, "status": "PENDING"}

    def accept(self, from_id: str, to_id: str) -> None:
        k = self._key(from_id, to_id)
        if k not in self._relations:
            raise BuddyRequestNotFoundError(f"{from_id} ↔ {to_id}")
        self._relations[k]["status"] = "ACCEPTED"

    def reject(self, from_id: str, to_id: str) -> None:
        k = self._key(from_id, to_id)
        if k not in self._relations:
            raise BuddyRequestNotFoundError(f"{from_id} ↔ {to_id}")
        self._relations[k]["status"] = "REJECTED"

    def list_buddies(self, user_id: str) -> list[str]:
        result = []
        for k, rel in self._relations.items():
            if user_id in k and rel["status"] == "ACCEPTED":
                other = next(iter(k - {user_id}))
                result.append(other)
        return result
