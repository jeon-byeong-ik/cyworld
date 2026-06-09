# -*- coding: utf-8 -*-
"""AC-8: 사진첩 테스트"""
import pytest
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from server.contexts.photo.photo import (
    PhotoService, AlbumNotFoundError, PhotoNotFoundError,
)


@pytest.fixture
def svc():
    s = PhotoService()
    s.register_if_needed = lambda: None
    return s


@pytest.fixture
def svc_with_album(svc):
    alb = svc.create_album("u1", "가족 story")
    return svc, alb["album_id"]


# AC-8a: 앨범 생성 + 목록 조회
def test_create_album_and_list(svc):
    svc.create_album("u1", "가족 story")
    svc.create_album("u1", "친구 story")
    albums = svc.list_albums("u1")
    assert len(albums) == 2
    assert any(a["name"] == "가족 story" for a in albums)


# AC-8b: 사진 추가 + 전체 조회
def test_add_photo_and_list_all(svc_with_album):
    svc, alb_id = svc_with_album
    svc.add_photo("u1", alb_id, "여행 사진", "즐거운 여행")
    svc.add_photo("u1", alb_id, "가족 사진", "행복한 하루")
    photos = svc.list_photos("u1")
    assert len(photos) == 2


# AC-8c: 앨범별 사진 조회
def test_list_photos_by_album(svc):
    alb1 = svc.create_album("u1", "앨범1")["album_id"]
    alb2 = svc.create_album("u1", "앨범2")["album_id"]
    svc.add_photo("u1", alb1, "사진A")
    svc.add_photo("u1", alb2, "사진B")
    assert len(svc.list_photos("u1", alb1)) == 1
    assert len(svc.list_photos("u1", alb2)) == 1


# AC-8d: 없는 앨범에 사진 추가 시 AlbumNotFoundError
def test_add_photo_invalid_album(svc):
    with pytest.raises(AlbumNotFoundError):
        svc.add_photo("u1", "nonexist", "실패 사진")


# AC-8e: 사진 삭제
def test_delete_photo(svc_with_album):
    svc, alb_id = svc_with_album
    ph = svc.add_photo("u1", alb_id, "삭제할 사진")
    svc.delete_photo("u1", ph["photo_id"])
    assert len(svc.list_photos("u1")) == 0


# AC-8f: 없는 사진 조회 시 PhotoNotFoundError
def test_get_photo_not_found(svc):
    with pytest.raises(PhotoNotFoundError):
        svc.get_photo("nonexist")


# AC-8g: 앨범 photo_count 반영
def test_album_photo_count(svc):
    alb = svc.create_album("u1", "테스트 앨범")["album_id"]
    svc.add_photo("u1", alb, "사진1")
    svc.add_photo("u1", alb, "사진2")
    albums = svc.list_albums("u1")
    assert albums[0]["photo_count"] == 2


# AC-8h: 타 사용자 사진은 조회 안 됨
def test_photos_isolated_by_user(svc):
    alb1 = svc.create_album("u1", "u1 앨범")["album_id"]
    alb2 = svc.create_album("u2", "u2 앨범")["album_id"]
    svc.add_photo("u1", alb1, "u1 사진")
    svc.add_photo("u2", alb2, "u2 사진")
    assert len(svc.list_photos("u1")) == 1
    assert len(svc.list_photos("u2")) == 1
