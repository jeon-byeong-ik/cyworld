# -*- coding: utf-8 -*-
from server.shared.idem import IdempotencyStore, idempotency_key


class InsufficientAcornError(Exception):
    pass


class AcornService:
    def __init__(self, clock=None):
        self._balances = {}     # user_id → int
        self._history = {}      # user_id → list[dict]
        self._counter = 0
        self._idem = IdempotencyStore()
        self._clock = clock or (lambda: 0.0)

    def _ensure(self, user_id: str) -> None:
        self._balances.setdefault(user_id, 0)
        self._history.setdefault(user_id, [])

    def charge(self, user_id: str, amount: int,
               idem_payload: dict = None) -> tuple[str, bool]:
        """충전. (tx_id, is_replay) 반환."""
        self._ensure(user_id)
        key = idempotency_key(idem_payload) if idem_payload else None

        def _do():
            self._counter += 1
            tx_id = f"tx_{self._counter}"
            self._balances[user_id] += amount
            self._history[user_id].append({
                "tx_id": tx_id, "type": "charge",
                "amount": amount, "ts": self._clock(),
            })
            return tx_id

        if key:
            return self._idem.issue_once(key, _do)
        return _do(), False

    def spend(self, user_id: str, amount: int) -> str:
        """사용. tx_id 반환. 잔액 부족 시 InsufficientAcornError."""
        self._ensure(user_id)
        if self._balances[user_id] < amount:
            raise InsufficientAcornError(
                f"{user_id}: balance={self._balances[user_id]} < {amount}"
            )
        self._counter += 1
        tx_id = f"tx_{self._counter}"
        self._balances[user_id] -= amount
        self._history[user_id].append({
            "tx_id": tx_id, "type": "spend",
            "amount": amount, "ts": self._clock(),
        })
        return tx_id

    def balance(self, user_id: str) -> int:
        self._ensure(user_id)
        return self._balances[user_id]

    def history(self, user_id: str) -> list:
        self._ensure(user_id)
        return list(self._history[user_id])
