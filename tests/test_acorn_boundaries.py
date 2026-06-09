# -*- coding: utf-8 -*-
"""도토리 경계값: 잔액 0·정확히 소진·충전→사용 순서."""
import pytest
from server.contexts.acorn.acorn import InsufficientAcornError


def test_spend_exact_balance(acorn_svc):
    svc, _ = acorn_svc
    svc.charge("u1", 50)
    svc.spend("u1", 50)  # 잔액과 정확히 같은 금액 — 성공해야 함
    assert svc.balance("u1") == 0


def test_spend_zero_balance(acorn_svc):
    svc, _ = acorn_svc
    with pytest.raises(InsufficientAcornError):
        svc.spend("u1", 1)  # 초기 잔액 0에서 즉시 거부


def test_charge_then_spend_sequence(acorn_svc):
    svc, clock = acorn_svc
    svc.charge("u1", 200)
    clock["t"] = 2000.0
    svc.spend("u1", 80)
    clock["t"] = 3000.0
    svc.spend("u1", 120)
    assert svc.balance("u1") == 0
    h = svc.history("u1")
    assert len(h) == 3
    assert h[0]["type"] == "charge"
    assert h[1]["type"] == "spend"
    assert h[2]["type"] == "spend"
