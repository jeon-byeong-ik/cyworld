# -*- coding: utf-8 -*-
"""AC-4: 도토리 충전·사용·잔액 부족·멱등."""
import pytest
from server.contexts.acorn.acorn import InsufficientAcornError


def test_acorn_charge_and_balance(acorn_svc):
    svc, _ = acorn_svc
    svc.charge("u1", 100)
    assert svc.balance("u1") == 100


def test_acorn_spend(acorn_svc):
    svc, _ = acorn_svc
    svc.charge("u1", 100)
    svc.spend("u1", 30)
    assert svc.balance("u1") == 70


def test_acorn_insufficient(acorn_svc):
    svc, _ = acorn_svc
    svc.charge("u1", 10)
    with pytest.raises(InsufficientAcornError):
        svc.spend("u1", 50)
    assert svc.balance("u1") == 10  # 잔액 불변


def test_acorn_charge_idempotent(acorn_svc):
    svc, _ = acorn_svc
    payload = {"user_id": "u1", "amount": 100, "event": "purchase"}
    tx1, r1 = svc.charge("u1", 100, idem_payload=payload)
    tx2, r2 = svc.charge("u1", 100, idem_payload=payload)
    assert tx1 == tx2
    assert r1 is False
    assert r2 is True
    assert svc.balance("u1") == 100  # 중복 충전 없음
