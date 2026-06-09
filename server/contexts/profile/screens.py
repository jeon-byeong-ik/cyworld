# -*- coding: utf-8 -*-
MINIHOMPY_HTML = """\
<!DOCTYPE html>
<html lang="ko">
<head><meta charset="utf-8"><title>{nickname}의 미니홈피</title></head>
<body>
  <header class="profile">
    <h1 class="nickname">{nickname}</h1>
    <p class="intro">{intro}</p>
    <span class="skin">{skin}</span>
  </header>
  <div class="stats">
    <span class="buddy-count">일촌 {buddy_count}명</span>
    <span class="visitor-count">방문자 {visitor_count}명</span>
  </div>
  <section class="guestbook-preview">{guestbook_preview}</section>
</body>
</html>
"""


def render_minihompy(profile: dict, guestbook_preview: str,
                     buddy_count: int, visitor_count: int) -> str:
    return MINIHOMPY_HTML.format(
        nickname=profile["nickname"],
        intro=profile["intro"],
        skin=profile["skin"],
        buddy_count=buddy_count,
        visitor_count=visitor_count,
        guestbook_preview=guestbook_preview,
    )
