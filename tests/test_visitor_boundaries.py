# -*- coding: utf-8 -*-
"""방문자 카운터 경계값: 당일 중복·날짜 전환·복수 방문자."""


def test_same_visitor_no_duplicate_today(visitor_svc):
    svc, _ = visitor_svc
    for _ in range(5):
        svc.visit("hompy1", "v1")
    s = svc.stats("hompy1")
    assert s["today"] == 1    # today 중복 차단
    assert s["total"] == 5    # total 은 매 호출마다 증가


def test_date_change_resets_today(visitor_svc):
    svc, clock = visitor_svc
    svc.visit("hompy1", "v1")
    svc.visit("hompy1", "v2")
    assert svc.stats("hompy1")["today"] == 2
    clock["date"] = "2025-01-02"
    s = svc.stats("hompy1")
    assert s["today"] == 0     # 날짜 바뀌면 today 초기화
    assert s["total"] == 2     # total 누적 유지


def test_different_visitors_count_separately(visitor_svc):
    svc, _ = visitor_svc
    svc.visit("hompy1", "v1")
    svc.visit("hompy1", "v2")
    svc.visit("hompy1", "v3")
    s = svc.stats("hompy1")
    assert s["today"] == 3
    assert s["total"] == 3
