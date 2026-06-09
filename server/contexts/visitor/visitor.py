# -*- coding: utf-8 -*-
class VisitorService:
    def __init__(self, date_fn=None):
        self._date_fn = date_fn or (lambda: "1970-01-01")
        # hompy_id → {"total": int, "today_date": str, "today": int, "visited": set}
        self._stats = {}

    def _ensure(self, hompy_id: str) -> None:
        self._stats.setdefault(hompy_id, {
            "total": 0,
            "today_date": self._date_fn(),
            "today": 0,
            "visited": set(),
        })

    def _refresh_date(self, hompy_id: str) -> None:
        """날짜가 바뀌면 today 초기화."""
        s = self._stats[hompy_id]
        current = self._date_fn()
        if s["today_date"] != current:
            s["today_date"] = current
            s["today"] = 0
            s["visited"] = set()

    def visit(self, hompy_id: str, visitor_id: str) -> None:
        self._ensure(hompy_id)
        self._refresh_date(hompy_id)
        s = self._stats[hompy_id]
        s["total"] += 1
        if visitor_id not in s["visited"]:
            s["today"] += 1
            s["visited"].add(visitor_id)

    def stats(self, hompy_id: str) -> dict:
        self._ensure(hompy_id)
        self._refresh_date(hompy_id)
        s = self._stats[hompy_id]
        return {"total": s["total"], "today": s["today"]}
