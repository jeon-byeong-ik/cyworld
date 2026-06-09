# -*- coding: utf-8 -*-
"""AC-2: 방명록 작성·조회·비밀글·멱등·삭제."""
import pytest
from server.contexts.guestbook.guestbook import SecretEntryError, EntryNotFoundError


def test_guestbook_write_and_list(guestbook_svc):
    eid, replay = guestbook_svc.write("hompy1", "visitor1", "안녕하세요!")
    assert eid.startswith("gb_")
    assert replay is False
    entries = guestbook_svc.list_entries("hompy1", requester_id="hompy1")
    assert len(entries) == 1
    assert entries[0]["content"] == "안녕하세요!"


def test_guestbook_secret_entry(guestbook_svc):
    eid, _ = guestbook_svc.write("hompy1", "visitor1", "비밀글", secret=True)
    # 홈피 주인 조회 — OK
    entry = guestbook_svc.read_entry(eid, requester_id="hompy1")
    assert entry["content"] == "비밀글"
    # 제3자 조회 — SecretEntryError
    with pytest.raises(SecretEntryError):
        guestbook_svc.read_entry(eid, requester_id="stranger")


def test_guestbook_idempotent(guestbook_svc):
    payload = {"hompy_id": "hompy1", "author_id": "v1", "content": "hello"}
    eid1, r1 = guestbook_svc.write("hompy1", "v1", "hello", idem_payload=payload)
    eid2, r2 = guestbook_svc.write("hompy1", "v1", "hello", idem_payload=payload)
    assert eid1 == eid2
    assert r1 is False
    assert r2 is True


def test_guestbook_delete(guestbook_svc):
    eid, _ = guestbook_svc.write("hompy1", "visitor1", "삭제될 글")
    guestbook_svc.delete(eid, requester_id="hompy1")
    with pytest.raises(EntryNotFoundError):
        guestbook_svc.read_entry(eid, requester_id="hompy1")
