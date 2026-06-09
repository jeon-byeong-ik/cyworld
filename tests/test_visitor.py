# -*- coding: utf-8 -*-
"""AC-6: 방문자 카운터·중복 방지·날짜 초기화."""


def test_visitor_count_increases(visitor_svc):
    svc, _ = visitor_svc
    svc.visit("hompy1", "v1")
    svc.visit("hompy1", "v2")
    s = svc.stats("hompy1")
    assert s["total"] == 2
    assert s["today"] == 2


def test_visitor_no_duplicate_today(visitor_svc):
    svc, _ = visitor_svc
    svc.visit("hompy1", "v1")
    svc.visit("hompy1", "v1")  # 당일 재방문
    s = svc.stats("hompy1")
    assert s["total"] == 2   # total 은 매 방문마다 증가
    assert s["today"] == 1   # today 는 중복 방지


def test_visitor_date_change_resets_today(visitor_svc):
    svc, clock = visitor_svc
    svc.visit("hompy1", "v1")
    assert svc.stats("hompy1")["today"] == 1
    clock["date"] = "2025-01-02"
    svc.visit("hompy1", "v1")
    s = svc.stats("hompy1")
    assert s["today"] == 1   # 새날 첫 방문
    assert s["total"] == 2   # 전체 누적
