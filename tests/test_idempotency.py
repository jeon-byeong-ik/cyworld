# -*- coding: utf-8 -*-
"""멱등 유틸 심화: key 안정성·순서 무관·replay 1회."""
from server.shared.idem import idempotency_key, IdempotencyStore


def test_key_stable_same_payload():
    payload = {"user_id": "u1", "amount": 100, "event": "charge"}
    assert idempotency_key(payload) == idempotency_key(payload)


def test_key_order_independent():
    p1 = {"a": 1, "b": 2}
    p2 = {"b": 2, "a": 1}
    assert idempotency_key(p1) == idempotency_key(p2)


def test_store_replay_once():
    store = IdempotencyStore()
    counter = {"n": 0}

    def fn():
        counter["n"] += 1
        return f"result_{counter['n']}"

    key = "test-key"
    r1, replay1 = store.issue_once(key, fn)
    r2, replay2 = store.issue_once(key, fn)
    assert r1 == r2          # 같은 결과
    assert replay1 is False
    assert replay2 is True
    assert counter["n"] == 1  # fn 은 1회만 실행


def test_guestbook_idem_end_to_end(guestbook_svc):
    payload = {"hompy_id": "h1", "author_id": "v1", "content": "hi"}
    eid1, r1 = guestbook_svc.write("h1", "v1", "hi", idem_payload=payload)
    eid2, r2 = guestbook_svc.write("h1", "v1", "hi", idem_payload=payload)
    assert eid1 == eid2 and r2 is True


def test_acorn_idem_end_to_end(acorn_svc):
    svc, _ = acorn_svc
    payload = {"user_id": "u1", "amount": 50, "ref": "order-1"}
    tx1, r1 = svc.charge("u1", 50, idem_payload=payload)
    tx2, r2 = svc.charge("u1", 50, idem_payload=payload)
    assert tx1 == tx2 and r2 is True
    assert svc.balance("u1") == 50  # 중복 충전 없음
