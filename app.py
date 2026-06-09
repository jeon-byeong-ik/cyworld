# -*- coding: utf-8 -*-
"""싸이월드 미니홈피 클론 — 로컬 데모 서버 (표준 라이브러리만 사용)."""
import json
import mimetypes
import pathlib
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from server.contexts.profile.profile import ProfileService, ProfileNotFoundError
from server.contexts.guestbook.guestbook import GuestbookService
from server.contexts.diary.diary import DiaryService
from server.contexts.acorn.acorn import AcornService
from server.contexts.buddy.buddy import BuddyService
from server.contexts.visitor.visitor import VisitorService
from server.contexts.photo.photo import PhotoService, AlbumNotFoundError
from server.contexts.video.video import VideoService

STATIC = pathlib.Path(__file__).parent / "static"

# ── 샘플 데이터 ──────────────────────────────────────────────────────────────
profile_svc = ProfileService()
guestbook_svc = GuestbookService()
diary_svc = DiaryService()
acorn_svc = AcornService()
buddy_svc = BuddyService()
visitor_svc = VisitorService(date_fn=__import__("datetime").date.today)
photo_svc = PhotoService()
video_svc = VideoService()

profile_svc.register("jbi", nickname="전병익", intro="언제나 즐겁게 하루를 보내자~",
                     skin="블루스카이")
profile_svc.register("u2", nickname="김영희", intro="자주 놀러오세요 ✨", skin="핑크")
profile_svc.register("u3", nickname="이민준", intro="오늘도 화이팅!", skin="그린")

acorn_svc.charge("jbi", 1200)
acorn_svc.charge("u2", 300)

buddy_svc.request("jbi", "u2"); buddy_svc.accept("jbi", "u2")
buddy_svc.request("jbi", "u3"); buddy_svc.accept("jbi", "u3")

guestbook_svc.write("jbi", "u2",    "병익아~ 잘 지내지? 오랜만이다!")
guestbook_svc.write("jbi", "u3",    "미니홈피 자주 놀러올게요 ㅎㅎ")
guestbook_svc.write("jbi", "u2",    "다음에 같이 밥 먹자~ 연락해!", secret=True)
guestbook_svc.write("jbi", "visitor1", "좋은 하루 보내세요~")

diary_svc.write("jbi", "도쿄 디즈니랜드 다녀왔어요! 🏰",
                "오늘 아이들이랑 도쿄 디즈니랜드에 다녀왔다. "
                "신나서 손뼉 치는 모습이 너무 귀여웠다. 언제 또 가고 싶다.")
diary_svc.write("jbi", "주말 가족 나들이",
                "날씨가 너무 좋아서 가족들이랑 공원에 다녀왔어요. "
                "아이들이 많이 컸구나 싶었던 하루.")

# 사진첩 샘플 데이터
_alb_fam   = photo_svc.create_album("jbi", "가족 story")["album_id"]
_alb_fri   = photo_svc.create_album("jbi", "친구 story")["album_id"]
_alb_trip  = photo_svc.create_album("jbi", "여행 story")["album_id"]
_alb_work  = photo_svc.create_album("jbi", "work story")["album_id"]
_alb_tokyo = photo_svc.create_album("jbi", "도쿄·USJ 여행")["album_id"]

photo_svc.add_photo("jbi", _alb_fam,  "주말 가족 나들이",
                    "봄날 공원에서 산책 🌸",
                    "/static/images/profile.jpg")
photo_svc.add_photo("jbi", _alb_fri,  "친구들이랑 모임",
                    "오랜만에 다같이 모였어요 😄",
                    "/static/images/profile.jpg")
photo_svc.add_photo("jbi", _alb_trip, "서울 야경",
                    "한강에서 바라본 서울 야경 🌃",
                    "/static/images/profile.jpg")
photo_svc.add_photo("jbi", _alb_work, "팀 회식",
                    "팀원들이랑 맛있는 저녁 🍻",
                    "/static/images/profile.jpg")

# 도쿄·USJ 여행 실사진 8장
photo_svc.add_photo("jbi", _alb_tokyo, "신데렐라 성 앞에서",
                    "도쿄 디즈니랜드 입구! 성 앞에서 포즈 📸",
                    "/static/images/tokyo_disney_01.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "신데렐라 성 야경 🌙",
                    "밤에 파란 조명으로 빛나는 아름다운 성",
                    "/static/images/tokyo_disney_02.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "형제 함께 성 앞에서",
                    "둘이서 사이좋게 🏰",
                    "/static/images/tokyo_disney_03.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "회전목마 야경 🎠",
                    "저녁 황금빛 조명이 너무 예뻤어요",
                    "/static/images/tokyo_disney_04.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "게임존에서 신나게 🎮",
                    "실내 게임기 앞에서 환호하는 아이들",
                    "/static/images/tokyo_disney_05.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "나리타 공항 출발층 ✈️",
                    "드디어 일본 도착! 설레는 공항 풍경",
                    "/static/images/tokyo_airport_01.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "활주로 비행기",
                    "탑승 전 활주로에 서 있는 비행기",
                    "/static/images/tokyo_airport_02.jpg")
photo_svc.add_photo("jbi", _alb_tokyo, "USJ 유니버설 스튜디오 🎬",
                    "유니버설 스튜디오 재팬 지구본 앞!",
                    "/static/images/usj_01.jpg")

# 동영상 샘플 데이터
video_svc.add_video("jbi", "도쿄 여행 브이로그 🎥",
                    "아이들이랑 즐거운 디즈니랜드 여행 영상",
                    "/static/images/profile.jpg")
video_svc.add_video("jbi", "주말 나들이 일상",
                    "봄날 공원 산책 영상 🌸",
                    "/static/images/profile.jpg")
video_svc.add_video("jbi", "생일파티 현장",
                    "친구 생일파티에서 찍은 영상 🎂",
                    "/static/images/profile.jpg")


# ── CSS: 실제 싸이월드 스타일 재현 ────────────────────────────────────────────
CYWORLD_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "돋움", "굴림", Dotum, Gulim, sans-serif;
  font-size: 12px;
  color: #333;
  background-color: #9ab0c8;
  background-image:
    linear-gradient(rgba(0,0,0,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.08) 1px, transparent 1px);
  background-size: 18px 18px;
  min-height: 100vh;
}
a { color: #336699; text-decoration: none; }
a:hover { text-decoration: underline; color: #003399; }

/* ─── 전역 네비바 ─── */
#gnav {
  width: 100%;
  background: linear-gradient(to bottom, #e4e4e4, #d0d0d0);
  border-bottom: 1px solid #b4b4b4;
  display: flex; align-items: center;
  padding: 3px 10px; height: 26px; font-size: 11px; gap: 6px;
}
.gnav-left { display: flex; align-items: center; gap: 3px; }
.gnav-left input[type=text] {
  height: 18px; width: 110px; border: 1px solid #ff6666;
  padding: 0 5px; font-size: 11px; font-family: inherit; color: #666;
}
.gnav-left button {
  height: 18px; padding: 0 6px;
  background: linear-gradient(to bottom, #eee, #d8d8d8);
  border: 1px solid #aaa; font-size: 10px; font-family: inherit; cursor: pointer;
}
.gnav-ad { font-size: 10px; color: #777; margin-left: 6px; }
.gnav-right { margin-left: auto; display: flex; align-items: center; }
.gnav-right a { font-size: 11px; color: #333; padding: 0 5px; }
.gnav-right a:hover { color: #003399; text-decoration: none; }
.gnav-sep { color: #bbb; }

/* ─── 메인 3컬럼 ─── */
#cy-wrap {
  width: 780px; margin: 8px auto 0;
  display: flex; align-items: flex-start; position: relative;
}

/* ─── 좌측 사이드바 ─── */
#cy-left { width: 174px; flex-shrink: 0; position: relative; z-index: 5; }

.cy-visitor-bar {
  background: linear-gradient(to bottom, #606878, #505868);
  color: #d8dde8; font-size: 10px; text-align: center;
  padding: 3px 0; letter-spacing: 0.3px;
  border: 1px solid #404858; border-bottom: none;
}
.cy-visitor-bar strong { color: #fff; }

.cy-left-panel {
  background: linear-gradient(to bottom, #c4d8ed, #b4cce0);
  border: 1px solid #7a9ab8; overflow: hidden;
}

.cy-today-box {
  background: linear-gradient(to bottom, #fffde8, #fffacc);
  border-bottom: 1px solid #d4c040;
  padding: 3px 6px; font-size: 11px; color: #554400;
  display: flex; align-items: center; justify-content: space-between; min-height: 22px;
}
.cy-today-label { font-size: 10px; color: #777; }
.cy-today-heart { color: #cc3344; font-weight: bold; }
.cy-today-mood  { color: #554400; font-weight: bold; margin-left: 2px; }
.cy-today-arrow { color: #aaa; font-size: 9px; }

.cy-photo-area {
  padding: 8px 8px 4px;
  background: linear-gradient(to bottom, #c8dcf0, #c0d8ec); text-align: center;
}
.cy-photo {
  width: 140px; height: 140px; object-fit: cover;
  border: 2px solid #7a9ab8; display: block; margin: 0 auto;
  box-shadow: 0 2px 6px rgba(0,50,120,0.2);
}

.cy-intro-text {
  padding: 6px 8px 8px; font-size: 11px; color: #334466; line-height: 1.6;
  background: linear-gradient(to bottom, #c0d8ec, #b8d0e8); min-height: 36px;
}

.cy-edit-bar {
  background: linear-gradient(to bottom, #b8d0e8, #a8c4dc);
  border-top: 1px solid #7a9ab8; border-bottom: 1px solid #7a9ab8;
  padding: 3px 7px; display: flex; justify-content: space-between;
  align-items: center; font-size: 10px;
}
.cy-edit-bar a { color: #2255aa; }
.cy-edit-bar .sep { color: #88aacc; }
.cy-edit-bar .arr { color: #99aacc; font-size: 9px; }

.cy-user-info {
  background: linear-gradient(to bottom, #c8dcf0, #bcd0e8); padding: 5px 8px 7px;
}
.cy-user-info .uname   { font-weight: bold; font-size: 12px; color: #336699; }
.cy-user-info .udetail { font-size: 10px; color: #557799; margin-top: 2px; line-height: 1.5; }

.spiral-rings {
  position: absolute; right: -10px; top: 44px;
  z-index: 30; display: flex; flex-direction: column; gap: 30px;
}
.ring {
  width: 18px; height: 18px; border-radius: 50%;
  background: radial-gradient(circle at 38% 35%, #ffffff 30%, #ddeeff 100%);
  border: 2px solid #7a9ab8;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3), inset 0 1px 2px rgba(255,255,255,0.9);
}

/* ─── 중앙 메인 패널 ─── */
#cy-center {
  flex: 1; background: #fff; border: 1px solid #7a9ab8;
  border-left: 4px solid #88aac8;
  overflow-y: scroll; max-height: 520px; position: relative;
}

.cy-title-bar {
  background: linear-gradient(to bottom, #d8eef8, #c4e0f0);
  border-bottom: 2px solid #88aac8; padding: 7px 10px 7px 14px;
  display: flex; align-items: center; gap: 6px;
  position: sticky; top: 0; z-index: 10; min-height: 36px;
}
.cy-title-text {
  font-size: 16px; font-weight: bold; color: #3355aa; flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  font-family: "돋움", "굴림", Dotum, Gulim, sans-serif;
}
.cy-title-badge {
  background: linear-gradient(to bottom, #aad860, #88c040);
  border: 1px solid #66a020; border-radius: 3px; color: #224400;
  font-size: 10px; padding: 1px 5px; white-space: nowrap; flex-shrink: 0;
}
.cy-homesetting { font-size: 10px; color: #888; white-space: nowrap; flex-shrink: 0; }
.cy-homesetting a { color: #888; }
.cy-url-text { font-size: 10px; color: #99aacc; white-space: nowrap; flex-shrink: 0; }

.cy-section { padding: 8px 12px 8px 14px; border-bottom: 1px solid #d8eaf6; }
.cy-section-head {
  font-size: 12px; font-weight: bold; color: #224466;
  margin-bottom: 6px; padding-bottom: 4px; border-bottom: 1px solid #c8ddf0;
}
.cy-section-head a { font-size: 10px; font-weight: normal; color: #6688bb; margin-left: 8px; }

.cy-post-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 3px 16px; margin-bottom: 7px;
}
.cy-post-item { font-size: 11px; color: #334; padding: 1px 0; }
.cy-post-item a { color: #336699; }
.cy-post-cnt { color: #cc2200; font-weight: bold; }
.cy-post-hint {
  font-size: 10px; color: #888; line-height: 1.7;
  background: #f4f9fe; border: 1px dashed #b8d0e8; padding: 5px 8px;
}

.cy-miniroom-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 5px 10px 5px 14px;
  background: linear-gradient(to bottom, #eef6fc, #e4f0f8);
  border-top: 1px solid #c8ddf0; border-bottom: 1px solid #c8ddf0; font-size: 11px;
}
.cy-miniroom-head .mh-title { color: #224466; font-weight: bold; }
.cy-miniroom-head .mh-title a { color: #336699; font-weight: normal; }
.cy-miniroom-head .mh-loving { font-style: italic; color: #88aacc; font-size: 10px; }

.cy-miniroom-body {
  min-height: 210px;
  background:
    radial-gradient(ellipse at 20% 80%, rgba(80,150,220,0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(160,210,255,0.2) 0%, transparent 60%),
    linear-gradient(160deg, #d4eef8 0%, #e8f6ff 40%, #c8e8f8 100%);
  display: flex; align-items: center; justify-content: center;
  padding: 20px 16px; position: relative; overflow: hidden;
}
.cy-miniroom-body::before {
  content: ''; position: absolute; width: 200px; height: 200px;
  border-radius: 50%; background: rgba(255,255,255,0.12);
  top: -60px; right: -60px; pointer-events: none;
}
.cy-miniroom-body::after {
  content: ''; position: absolute; width: 140px; height: 140px;
  border-radius: 50%; background: rgba(100,160,220,0.08);
  bottom: -40px; left: -40px; pointer-events: none;
}
.miniroom-scene { display: flex; align-items: flex-end; gap: 20px; z-index: 2; position: relative; }
.miniroom-avatar { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.miniroom-photo-frame {
  width: 96px; height: 96px; border-radius: 50%; overflow: hidden;
  border: 3px solid rgba(255,255,255,0.85); box-shadow: 0 4px 14px rgba(0,60,140,0.22);
}
.miniroom-photo-frame img { width: 100%; height: 100%; object-fit: cover; }
.miniroom-name {
  font-size: 11px; font-weight: bold; color: #336;
  background: rgba(255,255,255,0.75); border-radius: 10px; padding: 2px 8px;
}
.miniroom-chat { flex: 1; display: flex; flex-direction: column; gap: 8px; padding-bottom: 10px; }
.speech-bubble {
  background: rgba(255,255,255,0.92); border: 1px solid #88aacc;
  border-radius: 10px; padding: 7px 10px; font-size: 11px; color: #334;
  position: relative; line-height: 1.5; max-width: 200px;
}
.speech-bubble::before {
  content: ''; position: absolute; left: -9px; top: 14px;
  border: 6px solid transparent; border-right-color: #88aacc;
}
.speech-bubble::after {
  content: ''; position: absolute; left: -7px; top: 15px;
  border: 5px solid transparent; border-right-color: rgba(255,255,255,0.92);
}
.bubble-author { font-size: 10px; color: #669; margin-top: 3px; }

.cy-miniroom-foot {
  background: linear-gradient(to bottom, #e4f0f8, #dceaf4);
  border-top: 1px solid #b8d0e8; padding: 3px 10px 3px 14px;
  font-size: 10px; display: flex; justify-content: space-between; align-items: center;
}
.cy-miniroom-foot a { color: #336699; margin-right: 5px; }

.cy-ilchon { padding: 6px 12px 8px 14px; border-bottom: 1px solid #d8eaf6; }
.cy-ilchon-head { font-size: 11px; font-weight: bold; color: #336699; margin-bottom: 5px; }
.cy-ilchon-head a { color: #336699; }
.ilchon-item { font-size: 11px; color: #555; padding: 3px 0; border-bottom: 1px dotted #d4e8f4; }
.ilchon-item:last-child { border-bottom: none; }
.ilchon-item .ia { color: #336699; font-weight: bold; }

.gb-entry {
  background: #fafcff; border: 1px solid #c4d8ec;
  padding: 5px 8px; margin-bottom: 3px; font-size: 11px; line-height: 1.5;
}
.gb-entry.secret { background: #fffbe6; border-color: #d4c040; }
.gb-author { font-weight: bold; color: #336699; margin-bottom: 1px; }
.gb-content { color: #444; }
.gb-meta { font-size: 10px; color: #aaa; margin-top: 2px; }
.cy-no-post {
  font-size: 11px; color: #999; background: #f4f8fc;
  border: 1px dashed #b4cce0; padding: 8px; text-align: center;
}

.gb-form { margin-top: 8px; }
.gb-form-label {
  font-size: 11px; font-weight: bold; color: #224466;
  margin-bottom: 5px; padding-bottom: 3px; border-bottom: 1px solid #c8ddf0;
}
.gb-form-row { display: flex; gap: 4px; align-items: center; margin-bottom: 4px; }
.gb-form input[type=text] {
  flex: 1; border: 1px solid #a8c4dc; padding: 3px 6px;
  font-size: 11px; font-family: inherit; background: #fff; height: 22px;
}
.gb-form textarea {
  width: 100%; border: 1px solid #a8c4dc; padding: 4px 6px;
  font-size: 11px; font-family: inherit; background: #fff;
  min-height: 54px; resize: vertical; margin-bottom: 4px;
}
.cy-btn {
  background: linear-gradient(to bottom, #5a88bb, #3a6899);
  color: #fff; border: 1px solid #2255aa; padding: 3px 10px;
  font-size: 11px; font-family: inherit; cursor: pointer;
  border-radius: 2px; white-space: nowrap; height: 22px;
}
.cy-btn:hover { background: linear-gradient(to bottom, #6a99cc, #4a77bb); }
.gb-form-submit { text-align: right; }

.diary-entry {
  border-left: 3px solid #88aac8; padding: 6px 10px; margin-bottom: 6px; background: #f4f9fe;
}
.diary-entry .diary-title { font-weight: bold; color: #224466; font-size: 12px; margin-bottom: 3px; }
.diary-entry .diary-body { font-size: 11px; color: #445566; line-height: 1.6; }
.diary-entry .diary-meta { font-size: 10px; color: #aaa; margin-top: 4px; }

.buddy-card {
  background: #fafcff; border: 1px solid #c4d8ec; padding: 6px 9px; margin-bottom: 4px; font-size: 11px;
}
.buddy-card .bn { font-weight: bold; color: #336699; }
.buddy-card .bi { color: #556677; margin-top: 2px; font-size: 10px; }

/* ─── 우측 사이드바 ─── */
#cy-right {
  width: 112px; flex-shrink: 0; background: #3c3c44;
  border: 1px solid #222228; border-left: none;
  display: flex; flex-direction: column; min-height: 520px;
}

.cy-right-stats { background: #454550; border-bottom: 1px solid #222230; padding: 6px 8px; }
.cy-right-stats p { font-size: 10px; color: #b8b8cc; line-height: 1.75; }
.cy-right-stats .rv { color: #ff9966; font-weight: bold; }

.cy-activity {
  background: linear-gradient(to bottom, #fff8e0, #fff0c8);
  border-bottom: 1px solid #d8c040; padding: 5px 7px;
}
.act-row {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 3px; font-size: 9px; color: #664400;
}
.act-row:last-child { margin-bottom: 0; }
.act-gauge { width: 38px; height: 4px; background: #e0d090; border-radius: 2px; overflow: hidden; }
.act-gauge-fill { height: 100%; background: linear-gradient(to right, #ff9944, #ffcc44); border-radius: 2px; }

.cy-music {
  background: #2e2e38; border-bottom: 1px solid #1a1a22;
  padding: 5px 8px; font-size: 9px; color: #8899bb; line-height: 1.8;
}
.cy-music a { color: #6688aa; }
.cy-music .ctrl { font-size: 11px; color: #6688aa; letter-spacing: 3px; }

.cy-nav-btn {
  display: block;
  background: linear-gradient(to bottom, #2e6878, #1e5060);
  color: #fff; font-size: 13px; font-weight: bold; text-align: center;
  padding: 7px 0; border-bottom: 1px solid #1a4050;
  text-decoration: none; font-family: "돋움", "굴림", Dotum, Gulim, sans-serif;
}
.cy-nav-btn:hover {
  background: linear-gradient(to bottom, #3a7888, #2a6070); color: #fff; text-decoration: none;
}
.cy-nav-btn.active {
  background: linear-gradient(to bottom, #183c50, #0e2c3c); color: #88ddff; border-left: 3px solid #66ccee;
}

.cy-right-bottom {
  background: #2a2a34; border-top: 1px solid #111118;
  padding: 7px 7px; margin-top: auto; text-align: center;
}
.cy-right-bottom img {
  width: 60px; height: 60px; object-fit: cover;
  border-radius: 50%; border: 2px solid #445566; opacity: 0.85;
}
.cy-right-bottom p { font-size: 9px; color: #7788aa; margin-top: 4px; line-height: 1.5; }

/* ═══════════════════════════════════════
   사진첩 (PHOTO ALBUM)
═══════════════════════════════════════ */
.photo-layout {
  display: flex; min-height: 460px;
}

/* 사진첩 좌측 앨범 트리 */
.photo-sidebar {
  width: 130px; flex-shrink: 0;
  background: linear-gradient(to bottom, #e8f2fc, #dceaf6);
  border-right: 1px solid #b8d0e8;
  padding: 6px 0;
}
.photo-sidebar-title {
  background: linear-gradient(to bottom, #5588bb, #3a6a9a);
  color: #fff; font-size: 11px; font-weight: bold;
  padding: 4px 8px; margin-bottom: 4px; letter-spacing: 0.5px;
  display: flex; justify-content: space-between; align-items: center;
}
.photo-sidebar-title span { font-size: 9px; color: #b8d8ff; }

.album-link {
  display: flex; align-items: center; gap: 4px;
  padding: 3px 8px; font-size: 11px; color: #335577;
  border-bottom: 1px dotted #c0d8ee; cursor: pointer;
  text-decoration: none;
}
.album-link:hover { background: #d0e8f8; text-decoration: none; }
.album-link.active { background: #b8d8f0; font-weight: bold; color: #224466; }
.album-link .alb-icon { font-size: 12px; }
.album-link .alb-cnt { margin-left: auto; color: #cc3300; font-size: 10px; }

/* 사진 그리드 영역 */
.photo-main { flex: 1; padding: 8px 10px; }

.photo-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 6px;
}
.photo-thumb {
  border: 1px solid #b8d0e8; background: #f4f9fe;
  overflow: hidden; cursor: pointer;
}
.photo-thumb:hover { border-color: #5588bb; box-shadow: 0 2px 6px rgba(0,80,160,0.18); }
.photo-thumb img {
  width: 100%; height: 70px; object-fit: cover; display: block;
}
.photo-thumb .pt-title {
  padding: 3px 5px; font-size: 10px; color: #335577;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  background: linear-gradient(to bottom, #eef5fc, #e4eef8);
  border-top: 1px solid #c8ddf0;
}

.photo-upload-form {
  margin-top: 10px; padding: 8px; background: #f4f9fe;
  border: 1px dashed #a8c4dc;
}
.photo-upload-form .puf-title {
  font-size: 11px; font-weight: bold; color: #224466; margin-bottom: 6px;
}
.photo-upload-form input[type=text],
.photo-upload-form select {
  width: 100%; height: 22px; border: 1px solid #a8c4dc;
  padding: 2px 6px; font-size: 11px; font-family: inherit;
  background: #fff; margin-bottom: 4px;
}
.photo-upload-form textarea {
  width: 100%; height: 36px; border: 1px solid #a8c4dc;
  padding: 3px 6px; font-size: 11px; font-family: inherit;
  background: #fff; resize: vertical; margin-bottom: 4px;
}

/* 사진 상세 */
.photo-detail { padding: 10px 14px; }
.photo-detail img {
  max-width: 100%; max-height: 300px; object-fit: contain;
  border: 1px solid #b8d0e8; display: block; margin: 0 auto 8px;
}
.photo-detail .pd-title { font-size: 14px; font-weight: bold; color: #224466; margin-bottom: 4px; }
.photo-detail .pd-desc  { font-size: 11px; color: #556677; line-height: 1.6; }
.photo-detail .pd-back  { margin-top: 8px; }

/* ═══════════════════════════════════════
   동영상 게시판
═══════════════════════════════════════ */
.video-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;
  padding: 8px 12px;
}
.video-card {
  border: 1px solid #b8d0e8; background: #fafcff; overflow: hidden;
}
.video-card:hover { border-color: #5588bb; box-shadow: 0 2px 6px rgba(0,80,160,0.15); }
.video-thumb {
  position: relative; background: #1a1a2a; overflow: hidden; height: 80px;
}
.video-thumb img { width: 100%; height: 100%; object-fit: cover; opacity: 0.75; display: block; }
.video-play-btn {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
  width: 30px; height: 30px; border-radius: 50%;
  background: rgba(255,255,255,0.85); border: 2px solid rgba(255,255,255,0.9);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #335577; pointer-events: none;
}
.video-info { padding: 5px 7px; }
.video-info .vt { font-size: 11px; font-weight: bold; color: #224466; margin-bottom: 2px; }
.video-info .vd { font-size: 10px; color: #667788; line-height: 1.4; }

.video-upload-form {
  margin: 0 12px 10px; padding: 8px; background: #f4f9fe;
  border: 1px dashed #a8c4dc;
}
.video-upload-form .vuf-title {
  font-size: 11px; font-weight: bold; color: #224466; margin-bottom: 6px;
}
.video-upload-form input[type=text] {
  width: 100%; height: 22px; border: 1px solid #a8c4dc;
  padding: 2px 6px; font-size: 11px; font-family: inherit;
  background: #fff; margin-bottom: 4px;
}
.video-upload-form textarea {
  width: 100%; height: 36px; border: 1px solid #a8c4dc;
  padding: 3px 6px; font-size: 11px; font-family: inherit;
  background: #fff; resize: vertical; margin-bottom: 4px;
}

/* ═══════════════════════════════════════
   프로필 수정
═══════════════════════════════════════ */
.profile-edit-wrap { padding: 12px 16px; }

.profile-edit-photo {
  text-align: center; margin-bottom: 14px;
}
.profile-edit-photo img {
  width: 100px; height: 100px; object-fit: cover;
  border-radius: 50%; border: 3px solid #88aac8;
  box-shadow: 0 3px 10px rgba(0,60,140,0.2);
  display: block; margin: 0 auto 6px;
}
.profile-edit-photo .pep-change {
  font-size: 10px; color: #6688bb; cursor: pointer;
}
.profile-edit-photo .pep-change:hover { text-decoration: underline; }

.profile-edit-form table {
  width: 100%; border-collapse: collapse; margin-bottom: 10px;
}
.profile-edit-form td { padding: 5px 6px; font-size: 11px; vertical-align: middle; }
.profile-edit-form .pef-label {
  width: 70px; color: #335577; font-weight: bold;
  background: linear-gradient(to right, #e4eff8, #dce8f4);
  border: 1px solid #c0d4e8; white-space: nowrap;
}
.profile-edit-form .pef-input { border: 1px solid #c0d4e8; background: #fff; }
.profile-edit-form input[type=text],
.profile-edit-form select,
.profile-edit-form textarea {
  width: 100%; border: 1px solid #a8c4dc;
  padding: 3px 6px; font-size: 11px; font-family: inherit;
  background: #fff;
}
.profile-edit-form textarea { height: 52px; resize: vertical; }
.profile-edit-form select { height: 24px; }

.profile-edit-actions {
  text-align: center; padding: 8px 0 4px;
  border-top: 1px solid #c8ddf0; display: flex; gap: 6px; justify-content: center;
}
.cy-btn-cancel {
  background: linear-gradient(to bottom, #cccccc, #b0b0b0);
  color: #333; border: 1px solid #999; padding: 3px 14px;
  font-size: 11px; font-family: inherit; cursor: pointer;
  border-radius: 2px; height: 22px;
}
.cy-btn-cancel:hover { background: linear-gradient(to bottom, #dddddd, #c0c0c0); }

.profile-save-ok {
  background: #eeffee; border: 1px solid #88cc88;
  color: #226622; font-size: 11px; padding: 6px 10px;
  margin-bottom: 8px; border-radius: 3px; text-align: center; display: none;
}
"""


# ── 페이지 셸 ─────────────────────────────────────────────────────────────────
def page_shell(user_id, profile, vstats, buddy_count, acorn, active_tab, content_html):
    nav_items = [
        ("홈",      f"/hompy/{user_id}",           "home"),
        ("프로필",  f"/hompy/{user_id}/profile",   "profile"),
        ("다이어리",f"/hompy/{user_id}/diary",     "diary"),
        ("사진첩",  f"/hompy/{user_id}/photos",    "photos"),
        ("동영상",  f"/hompy/{user_id}/videos",    "videos"),
        ("방명록",  f"/hompy/{user_id}/guestbook", "guestbook"),
        ("관리",    f"/hompy/{user_id}/manage",    "manage"),
    ]
    nav_html = "".join(
        f'<a href="{url}" class="cy-nav-btn{"  active" if tab == active_tab else ""}">'
        f'{label}</a>'
        for label, url, tab in nav_items
    )
    rings_html = "<div class='ring'></div>" * 6

    gb_count  = len([e for e in guestbook_svc._entries.values()
                     if e["hompy_id"] == user_id])
    d_count   = len([d for d in diary_svc._diaries.values()
                     if d["owner_id"] == user_id])
    ph_count  = len(photo_svc.list_photos(user_id))
    vid_count = len(video_svc.list_videos(user_id))

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>{profile['nickname']}의 미니홈피 :: 싸이월드</title>
  <style>{CYWORLD_CSS}</style>
</head>
<body>

<!-- ① 전역 네비바 -->
<div id="gnav">
  <div class="gnav-left">
    <input type="text" value="{profile['nickname']} 미니홈피">
    <button>검색</button>
    <span class="gnav-ad">싸이월드 클론 데모</span>
  </div>
  <div class="gnav-right">
    <a href="#">메인</a><span class="gnav-sep">|</span>
    <a href="#">선물가게</a><span class="gnav-sep">|</span>
    <a href="/hompy/{user_id}">내 미니홈피</a><span class="gnav-sep">|</span>
    <a href="#">방문한 히스토리가 남아요</a><span class="gnav-sep">|</span>
    <a href="#">바로가기&#9660;</a><span class="gnav-sep">|</span>
    <a href="#">랜덤</a><span class="gnav-sep">|</span>
    <a href="#">로그아웃</a>
  </div>
</div>

<!-- ② 메인 3컬럼 -->
<div id="cy-wrap">

  <!-- 좌측 사이드바 -->
  <div id="cy-left">
    <div class="cy-visitor-bar">
      TODAY <strong>{vstats["today"]}</strong> &nbsp;|&nbsp; TOTAL <strong>{vstats["total"]}</strong>
    </div>
    <div class="cy-left-panel">
      <div class="cy-today-box">
        <span>
          <span class="cy-today-label">TODAY IS... </span>
          <span class="cy-today-heart">&#9829;</span>
          <span class="cy-today-mood">{profile['intro'][:6]}</span>
        </span>
        <span class="cy-today-arrow">&#9660;</span>
      </div>
      <div class="cy-photo-area">
        <img class="cy-photo" src="/static/images/profile.jpg" alt="프로필 사진">
      </div>
      <div class="cy-intro-text">{profile['intro']}</div>
      <div class="cy-edit-bar">
        <span>&#9658; <a href="/hompy/{user_id}/profile">EDIT</a> <span class="arr">&#9660;</span></span>
        <span class="sep">|</span>
        <span><a href="#">HISTORY</a> <span class="arr">&#9660;</span></span>
      </div>
      <div class="cy-user-info">
        <div class="uname">{profile['nickname']}</div>
        <div class="udetail">&#127808; {profile['skin']}</div>
        <div class="udetail">&#127823; 도토리 {acorn}개</div>
      </div>
    </div>
    <!-- 스파이럴 바인더 링 -->
    <div class="spiral-rings">{rings_html}</div>
  </div>

  <!-- 중앙 메인 -->
  <div id="cy-center">
    <div class="cy-title-bar">
      <span class="cy-title-text">&#128151; {profile['nickname']}의 미니홈피</span>
      <span class="cy-title-badge">&#9733; 즐겨찾기</span>
      <span class="cy-homesetting">&#10023; <a href="#">홈설정</a></span>
      <span class="cy-url-text">cyworld.local/{user_id}</span>
    </div>
    {content_html}
  </div>

  <!-- 우측 사이드바 -->
  <div id="cy-right">
    <div class="cy-right-stats">
      <p>댓글 | 스크랩 <span class="rv">{gb_count}</span></p>
      <p>즐겨찾기 <span class="rv">{buddy_count}</span></p>
      <p>일촌 <span class="rv">{buddy_count}</span>명</p>
      <p style="margin-top:2px;padding-top:2px;border-top:1px solid #333">
        사용중아이템<br>
        <span style="color:#ffcc66">&#10022; 소망상자</span>
      </p>
    </div>
    <div class="cy-activity">
      <div class="act-row">액티브
        <div class="act-gauge"><div class="act-gauge-fill" style="width:72%"></div></div>
      </div>
      <div class="act-row">페이머스
        <div class="act-gauge"><div class="act-gauge-fill" style="width:48%"></div></div>
      </div>
      <div class="act-row">팬들리
        <div class="act-gauge"><div class="act-gauge-fill" style="width:30%"></div></div>
      </div>
    </div>
    <div class="cy-music">
      &#9654; 음악 재생을 위해서 <a href="#">[설정]</a><br>
      <span class="ctrl">&#9664;&#9664; &#9654; &#9654;&#9654;</span>
    </div>
    {nav_html}
    <div class="cy-right-bottom">
      <img src="/static/images/profile.jpg" alt="avatar">
      <p>{profile['nickname']}<br>의 미니홈피</p>
    </div>
  </div>

</div>
</body>
</html>"""


# ── 홈 컨텐츠 ─────────────────────────────────────────────────────────────────
def render_home_content(user_id):
    diaries    = [d for d in diary_svc._diaries.values()  if d["owner_id"] == user_id]
    gb_entries = [e for e in guestbook_svc._entries.values() if e["hompy_id"] == user_id]
    d_cnt  = len(diaries)
    gb_cnt = len(gb_entries)
    ph_cnt = len(photo_svc.list_photos(user_id))
    vid_cnt = len(video_svc.list_videos(user_id))

    if not gb_entries and not d_cnt:
        hint = "최근 4주간 게시물이 없습니다.<br>소식이 뜸한 친구에게 마음의 한마디를 남기세요."
    else:
        hint = (f"다이어리 <strong>{d_cnt}</strong>개 · "
                f"사진첩 <strong>{ph_cnt}</strong>개 · "
                f"방명록 <strong>{gb_cnt}</strong>개의 게시물이 있습니다.")

    bubbles_html = ""
    for e in gb_entries[-2:]:
        author  = e["author_id"]
        content = "🔒 비밀글입니다." if e["secret"] else e["content"][:28]
        bubbles_html += f"""
        <div class="speech-bubble">
          {content}
          <div class="bubble-author">— {author}</div>
        </div>"""
    if not bubbles_html:
        bubbles_html = '<div class="speech-bubble">안녕하세요~ 놀러오세요! 👋</div>'

    ilchon_html = ""
    for e in gb_entries[:2]:
        if not e["secret"]:
            ilchon_html += (
                f'<div class="ilchon-item">'
                f'<span class="ia">{e["author_id"]}</span>: {e["content"][:22]}…'
                f'</div>'
            )
    if not ilchon_html:
        ilchon_html = '<div style="font-size:10px;color:#999">일촌평이 없습니다.</div>'

    return f"""
<div class="cy-section">
  <div class="cy-section-head">최근 게시물</div>
  <div class="cy-post-grid">
    <div class="cy-post-item">
      <a href="/hompy/{user_id}/diary">다이어리</a>
      <span class="cy-post-cnt"> {d_cnt}</span>/73
    </div>
    <div class="cy-post-item">
      <a href="/hompy/{user_id}/photos">사진첩</a>
      <span class="cy-post-cnt"> {ph_cnt}</span>/521
    </div>
    <div class="cy-post-item">
      <a href="/hompy/{user_id}/videos">동영상</a>
      <span class="cy-post-cnt"> {vid_cnt}</span>/2
    </div>
    <div class="cy-post-item">
      <a href="/hompy/{user_id}/guestbook">방명록</a>
      <span class="cy-post-cnt"> {gb_cnt}</span>/883
    </div>
  </div>
  <div class="cy-post-hint">{hint}</div>
</div>

<div class="cy-miniroom-head">
  <span class="mh-title">미니라이프 | <a href="#">미니룸</a></span>
  <span class="mh-loving">Loving you..</span>
</div>
<div class="cy-miniroom-body">
  <div class="miniroom-scene">
    <div class="miniroom-avatar">
      <div class="miniroom-photo-frame">
        <img src="/static/images/profile.jpg" alt="미니룸">
      </div>
      <div class="miniroom-name">전병익</div>
    </div>
    <div class="miniroom-chat">
      {bubbles_html}
    </div>
  </div>
</div>
<div class="cy-miniroom-foot">
  <div>
    <a href="#">&#9658;내 미니룸</a>
    <a href="#">&#9658;미니미설정</a>
    <a href="#">&#9658;미니룸설정</a>
  </div>
  <div><a href="#">답글쓰기[메인설정]</a></div>
</div>

<div class="cy-ilchon">
  <div class="cy-ilchon-head"><a href="/hompy/{user_id}/guestbook">일촌평</a></div>
  {ilchon_html}
</div>
"""


# ── 사진첩 컨텐츠 ─────────────────────────────────────────────────────────────
def render_photos_content(user_id, album_id=None, photo_id=None):
    albums = photo_svc.list_albums(user_id)

    # 앨범 사이드바 HTML
    all_count = len(photo_svc.list_photos(user_id))
    sidebar_items = (
        f'<a href="/hompy/{user_id}/photos" '
        f'class="album-link{"  active" if album_id is None and photo_id is None else ""}">'
        f'<span class="alb-icon">&#128444;</span> 전체보기'
        f'<span class="alb-cnt">{all_count}</span></a>'
    )
    for alb in albums:
        active = "  active" if alb["album_id"] == album_id else ""
        sidebar_items += (
            f'<a href="/hompy/{user_id}/photos/{alb["album_id"]}" class="album-link{active}">'
            f'<span class="alb-icon">&#128193;</span> {alb["name"]}'
            f'<span class="alb-cnt">{alb["photo_count"]}</span></a>'
        )

    # 사진 상세 뷰
    if photo_id:
        try:
            ph = photo_svc.get_photo(photo_id)
            back_url = (f"/hompy/{user_id}/photos/{ph['album_id']}"
                        if ph["album_id"] else f"/hompy/{user_id}/photos")
            main_html = f"""
<div class="photo-detail">
  <img src="{ph['img_url']}" alt="{ph['title']}">
  <div class="pd-title">&#128444; {ph['title']}</div>
  <div class="pd-desc">{ph['description']}</div>
  <div class="pd-back"><a href="{back_url}">&#9664; 앨범으로 돌아가기</a></div>
</div>"""
        except Exception:
            main_html = '<div class="cy-no-post">사진을 찾을 수 없습니다.</div>'
    else:
        # 썸네일 그리드
        photos = photo_svc.list_photos(user_id, album_id)
        if photos:
            thumbs = "".join(
                f'<a href="/hompy/{user_id}/photos/view/{p["photo_id"]}" class="photo-thumb">'
                f'<img src="{p["img_url"]}" alt="{p["title"]}">'
                f'<div class="pt-title">{p["title"]}</div></a>'
                for p in photos
            )
            grid_html = f'<div class="photo-grid">{thumbs}</div>'
        else:
            grid_html = '<div class="cy-no-post" style="margin-top:10px">사진이 없습니다.</div>'

        # 업로드 폼용 앨범 선택 옵션
        alb_options = "".join(
            f'<option value="{a["album_id"]}"'
            f'{"  selected" if a["album_id"] == album_id else ""}>{a["name"]}</option>'
            for a in albums
        )
        cur_album = album_id or (albums[0]["album_id"] if albums else "")

        main_html = f"""
{grid_html}
<div class="photo-upload-form">
  <div class="puf-title">&#128247; 사진 추가</div>
  <select id="ph-album">{alb_options}</select>
  <input type="text" id="ph-title" placeholder="사진 제목">
  <textarea id="ph-desc" placeholder="설명 (선택)"></textarea>
  <div style="text-align:right">
    <button class="cy-btn" onclick="uploadPhoto('{user_id}')">올리기</button>
  </div>
</div>
<script>
function uploadPhoto(uid) {{
  const album = document.getElementById('ph-album').value;
  const title = document.getElementById('ph-title').value;
  const desc  = document.getElementById('ph-desc').value;
  if (!title.trim()) {{ alert('제목을 입력하세요'); return; }}
  fetch('/api/hompy/' + uid + '/photos', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{album_id: album, title: title, description: desc}})
  }}).then(r => r.json()).then(() => location.reload());
}}
</script>"""

    label = "전체 사진"
    if album_id:
        for a in albums:
            if a["album_id"] == album_id:
                label = a["name"]
                break

    return f"""
<div class="photo-layout">
  <div class="photo-sidebar">
    <div class="photo-sidebar-title">
      PHOTO ALBUM <span>&#128444;</span>
    </div>
    {sidebar_items}
  </div>
  <div class="photo-main">
    <div class="cy-section-head" style="margin-bottom:0;padding:6px 0 4px">
      &#128444; {label}
    </div>
    {main_html}
  </div>
</div>"""


# ── 동영상 컨텐츠 ─────────────────────────────────────────────────────────────
def render_videos_content(user_id):
    videos = video_svc.list_videos(user_id)

    if videos:
        cards = "".join(
            f'<div class="video-card">'
            f'<div class="video-thumb">'
            f'<img src="{v["thumbnail_url"]}" alt="{v["title"]}">'
            f'<div class="video-play-btn">&#9654;</div>'
            f'</div>'
            f'<div class="video-info">'
            f'<div class="vt">{v["title"]}</div>'
            f'<div class="vd">{v["description"]}</div>'
            f'</div></div>'
            for v in videos
        )
        grid_html = f'<div class="video-grid">{cards}</div>'
    else:
        grid_html = '<div class="cy-no-post" style="margin:10px 12px">동영상이 없습니다.</div>'

    return f"""
<div class="cy-section">
  <div class="cy-section-head">&#127916; 동영상 ({len(videos)}개)</div>
</div>
{grid_html}
<div class="video-upload-form">
  <div class="vuf-title">&#127909; 동영상 추가</div>
  <input type="text" id="vid-title" placeholder="동영상 제목">
  <textarea id="vid-desc" placeholder="설명 (선택)"></textarea>
  <div style="text-align:right">
    <button class="cy-btn" onclick="uploadVideo('{user_id}')">올리기</button>
  </div>
</div>
<script>
function uploadVideo(uid) {{
  const title = document.getElementById('vid-title').value;
  const desc  = document.getElementById('vid-desc').value;
  if (!title.trim()) {{ alert('제목을 입력하세요'); return; }}
  fetch('/api/hompy/' + uid + '/videos', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{title: title, description: desc}})
  }}).then(r => r.json()).then(() => location.reload());
}}
</script>"""


# ── 프로필 수정 컨텐츠 ────────────────────────────────────────────────────────
def render_profile_content(user_id):
    try:
        profile = profile_svc.get(user_id)
    except ProfileNotFoundError:
        return '<div class="cy-no-post">프로필을 찾을 수 없습니다.</div>'

    skin_options = ["블루스카이", "핑크", "그린", "퍼플", "오렌지", "레드", "화이트"]
    skin_html = "".join(
        f'<option value="{s}"{"  selected" if s == profile["skin"] else ""}>{s}</option>'
        for s in skin_options
    )

    return f"""
<div class="cy-section">
  <div class="cy-section-head">&#128100; 프로필 수정</div>
</div>
<div class="profile-edit-wrap">
  <div id="save-ok" class="profile-save-ok">✅ 프로필이 저장되었습니다!</div>

  <div class="profile-edit-photo">
    <img src="/static/images/profile.jpg" alt="프로필 사진">
    <div class="pep-change">&#128247; 사진 변경</div>
  </div>

  <div class="profile-edit-form">
    <table>
      <tr>
        <td class="pef-label">닉네임</td>
        <td class="pef-input">
          <input type="text" id="pef-nickname" value="{profile['nickname']}">
        </td>
      </tr>
      <tr>
        <td class="pef-label">자기소개</td>
        <td class="pef-input">
          <textarea id="pef-intro">{profile['intro']}</textarea>
        </td>
      </tr>
      <tr>
        <td class="pef-label">스킨</td>
        <td class="pef-input">
          <select id="pef-skin">{skin_html}</select>
        </td>
      </tr>
    </table>
  </div>

  <div class="profile-edit-actions">
    <button class="cy-btn" onclick="saveProfile('{user_id}')">저장하기</button>
    <button class="cy-btn-cancel" onclick="history.back()">취소</button>
  </div>
</div>
<script>
function saveProfile(uid) {{
  const nickname = document.getElementById('pef-nickname').value.trim();
  const intro    = document.getElementById('pef-intro').value.trim();
  const skin     = document.getElementById('pef-skin').value;
  if (!nickname) {{ alert('닉네임을 입력하세요'); return; }}
  fetch('/api/hompy/' + uid + '/profile', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{nickname: nickname, intro: intro, skin: skin}})
  }}).then(r => r.json()).then(data => {{
    if (data.ok) {{
      const ok = document.getElementById('save-ok');
      ok.style.display = 'block';
      setTimeout(() => location.reload(), 1000);
    }}
  }});
}}
</script>"""


# ── 방명록 컨텐츠 ─────────────────────────────────────────────────────────────
def render_guestbook_content(user_id):
    entries = guestbook_svc.list_entries(user_id, requester_id=user_id)
    rows_html = "".join(
        f'<div class="gb-entry{"  secret" if e["secret"] else ""}">'
        f'<div class="gb-author">{e["author_id"]}</div>'
        f'<div class="gb-content">{"&#128274; 비밀글입니다." if e["secret"] else e["content"]}</div>'
        f'<div class="gb-meta">#{e["entry_id"]}</div>'
        f'</div>'
        for e in entries
    ) or '<div class="cy-no-post">아직 방명록이 없습니다.</div>'

    return f"""
<div class="cy-section">
  <div class="cy-section-head">&#128221; 방명록 ({len(entries)}개)</div>
  {rows_html}
  <div class="gb-form" style="margin-top:10px">
    <div class="gb-form-label">방명록 남기기</div>
    <div class="gb-form-row">
      <input type="text" id="gb-author" placeholder="작성자 ID">
      <label style="font-size:11px;white-space:nowrap">
        <input type="checkbox" id="gb-secret"> 비밀글
      </label>
    </div>
    <textarea id="gb-content" placeholder="내용을 입력하세요"></textarea>
    <div class="gb-form-submit">
      <button class="cy-btn" onclick="postGB('{user_id}')">남기기</button>
    </div>
  </div>
</div>
<script>
function postGB(uid) {{
  const a = document.getElementById('gb-author').value || 'guest';
  const c = document.getElementById('gb-content').value;
  const s = document.getElementById('gb-secret').checked;
  if (!c.trim()) {{ alert('내용을 입력하세요'); return; }}
  fetch('/api/hompy/' + uid + '/guestbook', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{author_id: a, content: c, secret: s}})
  }}).then(r => r.json()).then(() => location.reload());
}}
</script>"""


# ── 다이어리 컨텐츠 ───────────────────────────────────────────────────────────
def render_diary_content(user_id):
    diaries = [d for d in diary_svc._diaries.values() if d["owner_id"] == user_id]
    rows_html = "".join(
        f'<div class="diary-entry">'
        f'<div class="diary-title">{"&#128274; " if not d["public"] else "&#128212; "}{d["title"]}</div>'
        f'<div class="diary-body">{d["content"]}</div>'
        f'<div class="diary-meta">댓글 {len(d["comments"])}개</div>'
        f'</div>'
        for d in diaries
    ) or '<div class="cy-no-post">아직 다이어리가 없습니다.</div>'

    return f"""
<div class="cy-section">
  <div class="cy-section-head">&#128212; 다이어리 ({len(diaries)}개)</div>
  {rows_html}
</div>"""


# ── 일촌 컨텐츠 ───────────────────────────────────────────────────────────────
def render_buddy_content(user_id):
    buddies = buddy_svc.list_buddies(user_id)
    rows_html = ""
    for bid in buddies:
        try:
            bp = profile_svc.get(bid)
            rows_html += (
                f'<div class="buddy-card">'
                f'<div class="bn"><a href="/hompy/{bid}">&#128100; {bp["nickname"]}</a></div>'
                f'<div class="bi">{bp["intro"][:30]}</div>'
                f'</div>'
            )
        except ProfileNotFoundError:
            rows_html += f'<div class="buddy-card"><div class="bn">{bid}</div></div>'
    if not rows_html:
        rows_html = '<div class="cy-no-post">일촌이 없습니다.</div>'

    return f"""
<div class="cy-section">
  <div class="cy-section-head">&#128101; 일촌 목록 ({len(buddies)}명)</div>
  {rows_html}
</div>"""


# ── HTTP 핸들러 ───────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")

    def _send(self, code, body, ct="text/html; charset=utf-8"):
        enc = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(enc)))
        self.end_headers()
        self.wfile.write(enc)

    def _json(self, code, data):
        self._send(code, json.dumps(data, ensure_ascii=False), "application/json")

    def _read_body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n)) if n else {}

    def _full_page(self, user_id, content_html, active_tab="home"):
        try:
            profile = profile_svc.get(user_id)
        except ProfileNotFoundError:
            return None
        visitor_svc.visit(user_id, self.client_address[0])
        vstats  = visitor_svc.stats(user_id)
        buddies = buddy_svc.list_buddies(user_id)
        acorn   = acorn_svc.balance(user_id)
        return page_shell(user_id, profile, vstats, len(buddies), acorn,
                          active_tab, content_html)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"

        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/hompy/jbi")
            self.end_headers()
            return

        if path.startswith("/static/"):
            fpath = STATIC / path[len("/static/"):]
            if fpath.exists() and fpath.is_file():
                ct, _ = mimetypes.guess_type(str(fpath))
                self._send(200, fpath.read_bytes(), ct or "application/octet-stream")
            else:
                self._send(404, b"Not Found")
            return

        parts = [p for p in path.split("/") if p]

        # /hompy/{uid}
        if len(parts) == 2 and parts[0] == "hompy":
            uid  = parts[1]
            html = self._full_page(uid, render_home_content(uid), "home")
            self._send(200 if html else 404,
                       html or f"<h1>홈피를 찾을 수 없습니다: {uid}</h1>")
            return

        # /hompy/{uid}/{tab}
        if len(parts) == 3 and parts[0] == "hompy":
            uid, tab = parts[1], parts[2]
            dispatch = {
                "guestbook": (render_guestbook_content, "guestbook"),
                "diary":     (render_diary_content,     "diary"),
                "buddy":     (render_buddy_content,     "buddy"),
                "photos":    (lambda u: render_photos_content(u), "photos"),
                "videos":    (render_videos_content,    "videos"),
                "profile":   (render_profile_content,   "profile"),
            }
            if tab in dispatch:
                fn, active = dispatch[tab]
                html = self._full_page(uid, fn(uid), active)
                self._send(200 if html else 404, html or "<h1>404</h1>")
            else:
                self._send(404, "<h1>404 Not Found</h1>")
            return

        # /hompy/{uid}/photos/{album_id}
        if len(parts) == 4 and parts[0] == "hompy" and parts[2] == "photos":
            uid, album_id = parts[1], parts[3]
            html = self._full_page(
                uid, render_photos_content(uid, album_id=album_id), "photos")
            self._send(200 if html else 404, html or "<h1>404</h1>")
            return

        # /hompy/{uid}/photos/view/{photo_id}
        if len(parts) == 5 and parts[0] == "hompy" and parts[2] == "photos" and parts[3] == "view":
            uid, photo_id = parts[1], parts[4]
            html = self._full_page(
                uid, render_photos_content(uid, photo_id=photo_id), "photos")
            self._send(200 if html else 404, html or "<h1>404</h1>")
            return

        # GET /api/hompy/{uid}/guestbook
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "guestbook":
            uid = parts[2]
            self._json(200, guestbook_svc.list_entries(uid, requester_id=uid))
            return

        self._send(404, "<h1>404 Not Found</h1>")

    def do_POST(self):
        parts = [p for p in self.path.rstrip("/").split("/") if p]

        # POST /api/hompy/{uid}/guestbook
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "guestbook":
            uid  = parts[2]
            body = self._read_body()
            eid, replay = guestbook_svc.write(
                uid,
                body.get("author_id", "guest"),
                body.get("content", ""),
                secret=body.get("secret", False),
            )
            self._json(201, {"entry_id": eid, "replay": replay})
            return

        # POST /api/hompy/{uid}/profile
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "profile":
            uid  = parts[2]
            body = self._read_body()
            try:
                updated = profile_svc.update(
                    uid,
                    nickname=body.get("nickname", ""),
                    intro=body.get("intro", ""),
                    skin=body.get("skin", "블루스카이"),
                )
                self._json(200, {"ok": True, "profile": updated})
            except ProfileNotFoundError:
                self._json(404, {"ok": False, "error": "not found"})
            return

        # POST /api/hompy/{uid}/photos
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "photos":
            uid  = parts[2]
            body = self._read_body()
            try:
                photo = photo_svc.add_photo(
                    uid,
                    body.get("album_id", ""),
                    body.get("title", ""),
                    body.get("description", ""),
                )
                self._json(201, {"ok": True, "photo": photo})
            except AlbumNotFoundError:
                self._json(404, {"ok": False, "error": "album not found"})
            return

        # POST /api/hompy/{uid}/videos
        if len(parts) == 4 and parts[0] == "api" and parts[3] == "videos":
            uid  = parts[2]
            body = self._read_body()
            video = video_svc.add_video(
                uid,
                body.get("title", ""),
                body.get("description", ""),
            )
            self._json(201, {"ok": True, "video": video})
            return

        self._json(404, {"error": "not found"})


# ── 진입점 ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"[cy_live] http://localhost:{port}  (Ctrl+C 로 종료)")
    print(f"          전병익 홈피 → http://localhost:{port}/hompy/jbi")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[cy_live] 서버 종료")
