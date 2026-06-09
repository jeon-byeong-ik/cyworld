# -*- coding: utf-8 -*-
"""AC-3: 다이어리 CRUD·공개제어·댓글·삭제."""
import pytest
from server.contexts.diary.diary import DiaryNotFoundError, DiaryAccessError


def test_diary_write_and_read(diary_svc):
    did = diary_svc.write("u1", "오늘의 일기", "날씨가 맑다")
    entry = diary_svc.read(did, requester_id="u1")
    assert entry["title"] == "오늘의 일기"
    assert entry["public"] is True


def test_diary_private_access(diary_svc):
    did = diary_svc.write("u1", "비공개", "내용", public=False)
    # 소유자 조회 — OK
    diary_svc.read(did, requester_id="u1")
    # 제3자 조회 — DiaryAccessError
    with pytest.raises(DiaryAccessError):
        diary_svc.read(did, requester_id="u2")


def test_diary_update(diary_svc):
    did = diary_svc.write("u1", "제목", "원본")
    diary_svc.update(did, "u1", content="수정된 내용", public=False)
    entry = diary_svc.read(did, requester_id="u1")
    assert entry["content"] == "수정된 내용"
    assert entry["public"] is False


def test_diary_comment(diary_svc):
    did = diary_svc.write("u1", "댓글 테스트", "본문")
    diary_svc.add_comment(did, "u2", "좋은 글이에요")
    entry = diary_svc.read(did, requester_id="u1")
    assert len(entry["comments"]) == 1
    assert entry["comments"][0]["content"] == "좋은 글이에요"


def test_diary_delete_removes_comments(diary_svc):
    did = diary_svc.write("u1", "삭제 테스트", "본문")
    diary_svc.add_comment(did, "u2", "댓글")
    diary_svc.delete(did, "u1")
    with pytest.raises(DiaryNotFoundError):
        diary_svc.read(did, requester_id="u1")
