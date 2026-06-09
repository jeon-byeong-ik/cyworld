# -*- coding: utf-8 -*-
"""AC-1: 미니홈피 프로필 조회·수정·에러."""
import pytest
from server.contexts.profile.profile import ProfileNotFoundError


def test_profile_get(profile_svc):
    p = profile_svc.get("jbi")
    assert p["nickname"] == "전병익"
    assert p["intro"] == "언제나 즐겁게 하루를 보내자~"
    assert p["skin"] == "블루스카이"


def test_profile_not_found(profile_svc):
    with pytest.raises(ProfileNotFoundError):
        profile_svc.get("unknown")


def test_profile_update(profile_svc):
    profile_svc.update("jbi", nickname="전병익(수정)", intro="수정됨", skin="retro")
    p = profile_svc.get("jbi")
    assert p["nickname"] == "전병익(수정)"
    assert p["intro"] == "수정됨"
    assert p["skin"] == "retro"
