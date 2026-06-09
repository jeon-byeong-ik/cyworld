# -*- coding: utf-8 -*-
"""AC-9: 동영상 게시판 테스트"""
import pytest
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from server.contexts.video.video import VideoService, VideoNotFoundError


@pytest.fixture
def svc():
    return VideoService()


# AC-9a: 동영상 추가 + 목록 조회
def test_add_video_and_list(svc):
    svc.add_video("u1", "여행 브이로그", "즐거운 여행 영상")
    svc.add_video("u1", "일상 영상", "평범한 하루")
    videos = svc.list_videos("u1")
    assert len(videos) == 2
    assert any(v["title"] == "여행 브이로그" for v in videos)


# AC-9b: 동영상 단건 조회
def test_get_video(svc):
    vid = svc.add_video("u1", "테스트 영상")
    result = svc.get_video(vid["video_id"])
    assert result["title"] == "테스트 영상"
    assert result["owner_id"] == "u1"


# AC-9c: 동영상 삭제
def test_delete_video(svc):
    vid = svc.add_video("u1", "삭제 영상")
    svc.delete_video("u1", vid["video_id"])
    assert len(svc.list_videos("u1")) == 0


# AC-9d: 없는 동영상 조회 시 VideoNotFoundError
def test_get_video_not_found(svc):
    with pytest.raises(VideoNotFoundError):
        svc.get_video("nonexist")


# AC-9e: 없는 동영상 삭제 시 VideoNotFoundError
def test_delete_video_not_found(svc):
    with pytest.raises(VideoNotFoundError):
        svc.delete_video("u1", "nonexist")


# AC-9f: 타 사용자 동영상은 조회 안 됨
def test_videos_isolated_by_user(svc):
    svc.add_video("u1", "u1 영상")
    svc.add_video("u2", "u2 영상")
    assert len(svc.list_videos("u1")) == 1
    assert len(svc.list_videos("u2")) == 1


# AC-9g: 썸네일 URL 기본값 적용
def test_video_default_thumbnail(svc):
    vid = svc.add_video("u1", "썸네일 없는 영상")
    assert vid["thumbnail_url"] == "/static/images/profile.jpg"


# AC-9h: 설명 없이 추가 가능
def test_video_empty_description(svc):
    vid = svc.add_video("u1", "설명 없는 영상")
    assert vid["description"] == ""
