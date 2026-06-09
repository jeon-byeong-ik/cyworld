# -*- coding: utf-8 -*-
"""AC-7: 미니홈피 HTML 렌더 스냅샷 parity."""
import pathlib
from server.contexts.profile.screens import render_minihompy

SNAPSHOT = pathlib.Path(__file__).resolve().parents[1] / \
    "sdd/04_verify/10_test/ui_parity/minihompy.html"


def test_screen_renders_required_elements(profile_svc):
    profile = profile_svc.get("jbi")
    html = render_minihompy(profile, guestbook_preview="방명록 미리보기",
                            buddy_count=2, visitor_count=7344)
    assert "전병익" in html
    assert "class=\"nickname\"" in html
    assert "class=\"intro\"" in html
    assert "class=\"buddy-count\"" in html
    assert "class=\"visitor-count\"" in html
    assert "class=\"guestbook-preview\"" in html


def test_screen_matches_snapshot(profile_svc):
    profile = profile_svc.get("jbi")
    html = render_minihompy(profile, guestbook_preview="방명록 미리보기",
                            buddy_count=2, visitor_count=7344)
    if not SNAPSHOT.exists():
        SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT.write_text(html, encoding="utf-8")
    snapshot = SNAPSHOT.read_text(encoding="utf-8")
    assert html == snapshot
