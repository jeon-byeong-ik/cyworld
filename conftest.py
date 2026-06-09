# -*- coding: utf-8 -*-
"""pytest 픽스처: clock·id_gen 주입으로 결정적 테스트."""
import pytest

from server.contexts.profile.profile import ProfileService
from server.contexts.guestbook.guestbook import GuestbookService
from server.contexts.diary.diary import DiaryService
from server.contexts.acorn.acorn import AcornService
from server.contexts.buddy.buddy import BuddyService
from server.contexts.visitor.visitor import VisitorService


@pytest.fixture
def profile_svc():
    svc = ProfileService()
    svc.register("jbi", nickname="전병익", intro="언제나 즐겁게 하루를 보내자~", skin="블루스카이")
    svc.register("u2", nickname="김영희", intro="반갑습니다", skin="blue")
    return svc


@pytest.fixture
def guestbook_svc():
    return GuestbookService()


@pytest.fixture
def diary_svc():
    return DiaryService()


@pytest.fixture
def acorn_svc():
    clock = {"t": 1000.0}
    svc = AcornService(clock=lambda: clock["t"])
    return svc, clock


@pytest.fixture
def buddy_svc():
    return BuddyService()


@pytest.fixture
def visitor_svc():
    clock = {"date": "2025-01-01"}
    svc = VisitorService(date_fn=lambda: clock["date"])
    return svc, clock
