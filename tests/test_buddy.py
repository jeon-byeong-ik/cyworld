# -*- coding: utf-8 -*-
"""AC-5: 일촌 신청·수락·거절·목록."""
import pytest
from server.contexts.buddy.buddy import AlreadyBuddyError, BuddyRequestNotFoundError


def test_buddy_request_and_accept(buddy_svc):
    buddy_svc.request("u1", "u2")
    buddy_svc.accept("u1", "u2")
    assert "u2" in buddy_svc.list_buddies("u1")
    assert "u1" in buddy_svc.list_buddies("u2")


def test_buddy_reject(buddy_svc):
    buddy_svc.request("u1", "u2")
    buddy_svc.reject("u1", "u2")
    assert buddy_svc.list_buddies("u1") == []


def test_buddy_already_buddy(buddy_svc):
    buddy_svc.request("u1", "u2")
    buddy_svc.accept("u1", "u2")
    with pytest.raises(AlreadyBuddyError):
        buddy_svc.request("u1", "u2")


def test_buddy_accept_nonexistent(buddy_svc):
    with pytest.raises(BuddyRequestNotFoundError):
        buddy_svc.accept("u1", "u99")


def test_buddy_list_only_accepted(buddy_svc):
    buddy_svc.request("u1", "u2")
    buddy_svc.accept("u1", "u2")
    buddy_svc.request("u1", "u3")  # PENDING 상태
    assert buddy_svc.list_buddies("u1") == ["u2"]
