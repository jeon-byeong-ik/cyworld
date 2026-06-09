# 싸이월드 미니홈피 클론 · todos + 실행 계획

## Scope

미니홈피 프로필·방명록·다이어리·도토리·일촌·방문자 카운터를
순수 Python(in-memory)으로 구현·검증.
경계값(잔액 0·날짜 전환), 멱등성 유틸, contract.json 정합 포함.
사진첩(앨범·사진 CRUD)·동영상 게시판·프로필 수정 화면 추가.

---

## Acceptance Criteria

| AC | 내용 | 근거 | 상태 |
| --- | --- | --- | --- |
| AC-1 | 미니홈피 프로필 조회·수정. 없는 user_id → `ProfileNotFoundError` | `cyworld_feature_spec.md` | ⬜ |
| AC-2 | 방명록 작성·조회·삭제 + 비밀글 + 멱등성 | `cyworld_feature_spec.md` | ⬜ |
| AC-3 | 다이어리 CRUD + 댓글 + 공개 제어 | `cyworld_feature_spec.md` | ⬜ |
| AC-4 | 도토리 충전·사용·잔액 부족 거부 + 멱등성 | `cyworld_feature_spec.md` | ⬜ |
| AC-5 | 일촌 신청·수락·거절·목록 조회 | `cyworld_feature_spec.md` | ⬜ |
| AC-6 | 방문자 카운터 (중복 방지·날짜 전환 초기화) | `cyworld_feature_spec.md` | ⬜ |
| AC-7 | minihompy HTML 렌더 승인 스냅샷 일치 (UI parity) | `cyworld_feature_spec.md` | ⬜ |
| AC-8 | 사진첩 앨범 CRUD + 사진 추가·조회·삭제 | `cyworld_feature_spec.md` | ✅ |
| AC-9 | 동영상 게시판 추가·조회·삭제 | `cyworld_feature_spec.md` | ✅ |
| AC-10 | 프로필 수정 화면 + API | `cyworld_feature_spec.md` | ✅ |

완료 기준: `python3 proof/run_proof.py` → 전체 N/N PASS (목표 30개 이상)

---

## Execution Checklist

### Phase 1 — Core 구현

- [ ] T1 @backend-dev  공유 유틸 (`server/shared/idem.py`)
  - `auth/server/shared/idem.py` 참고 — SHA256 기반 `idempotency_key` + `IdempotencyStore`
  - `conftest.py` 기본 픽스처 뼈대 작성

- [ ] T2 @backend-dev  프로필 컨텍스트 (`server/contexts/profile/`)
  - `profile.py`: `ProfileService` — `get`, `update`, `register`
  - `screens.py`: `render_minihompy(profile, guestbook_preview, buddy_count, visitor_count) → str`
  - 에러: `ProfileNotFoundError`

- [ ] T3 @backend-dev  방명록 컨텍스트 (`server/contexts/guestbook/`)
  - `guestbook.py`: `GuestbookService` — `write`, `list_entries`, `delete`, `read_entry`
  - 비밀글: `secret=True` 시 `requester_id` 검증
  - 멱등: `IdempotencyStore` 적용 (write)
  - 에러: `SecretEntryError`, `EntryNotFoundError`

- [ ] T4 @backend-dev  다이어리 컨텍스트 (`server/contexts/diary/`)
  - `diary.py`: `DiaryService` — `write`, `read`, `update`, `delete`, `add_comment`
  - 비공개: `public=False` 시 소유자 외 `DiaryAccessError`
  - 에러: `DiaryNotFoundError`, `DiaryAccessError`

- [ ] T5 @backend-dev  도토리 컨텍스트 (`server/contexts/acorn/`)
  - `acorn.py`: `AcornService(clock)` — `charge`, `spend`, `balance`, `history`
  - 멱등: `IdempotencyStore` 적용 (charge)
  - 에러: `InsufficientAcornError`

- [ ] T6 @backend-dev  일촌 컨텍스트 (`server/contexts/buddy/`)
  - `buddy.py`: `BuddyService` — `request`, `accept`, `reject`, `list_buddies`
  - 상태: `PENDING` → `ACCEPTED` / `REJECTED`
  - 에러: `AlreadyBuddyError`, `BuddyRequestNotFoundError`

- [ ] T7 @backend-dev  방문자 카운터 컨텍스트 (`server/contexts/visitor/`)
  - `visitor.py`: `VisitorService(date_fn)` — `visit`, `stats`
  - 중복 방지: `(user_id, hompy_id, date)` 조합으로 당일 중복 제거
  - 날짜 전환: `date_fn()` 변경 시 today 카운터 자동 초기화

- [ ] T8 @test-dev  테스트 스위트 작성 (`tests/`)
  - `test_profile.py` — AC-1 (3개)
  - `test_guestbook.py` — AC-2 (4개)
  - `test_diary.py` — AC-3 (5개)
  - `test_acorn.py` — AC-4 (4개)
  - `test_buddy.py` — AC-5 (5개)
  - `test_visitor.py` — AC-6 (3개)
  - `test_screen_parity.py` — AC-7 (2개)

- [ ] T9 @test-dev  proof 게이트 + UI parity
  - `proof/run_proof.py` — `auth/proof/run_proof.py` 참고, `tmp/proof-results.json` 출력
  - `sdd/04_verify/10_test/ui_parity/minihompy.html` — 스냅샷 생성

### Phase 3 — 사진첩·동영상·프로필 수정 (신규)

- [x] T14 @backend-dev  사진첩 컨텍스트 (`server/contexts/photo/`)
  - `photo.py`: `PhotoService` — `create_album`, `list_albums`, `add_photo`, `list_photos`, `get_photo`, `delete_photo`
  - 에러: `AlbumNotFoundError`, `PhotoNotFoundError`

- [x] T15 @backend-dev  동영상 컨텍스트 (`server/contexts/video/`)
  - `video.py`: `VideoService` — `add_video`, `list_videos`, `get_video`, `delete_video`
  - 에러: `VideoNotFoundError`

- [x] T16 @backend-dev  app.py 확장
  - `render_photos_content(uid, album_id, photo_id)` — 앨범 사이드바 + 썸네일 그리드 + 상세뷰
  - `render_videos_content(uid)` — 동영상 카드 그리드
  - `render_profile_content(uid)` — 프로필 수정 폼
  - GET 라우트: `/hompy/{uid}/photos`, `/hompy/{uid}/photos/{album_id}`, `/hompy/{uid}/photos/view/{photo_id}`, `/hompy/{uid}/videos`, `/hompy/{uid}/profile`
  - POST API: `/api/hompy/{uid}/profile`, `/api/hompy/{uid}/photos`, `/api/hompy/{uid}/videos`

- [x] T17 @test-dev  테스트 스위트 확장
  - `tests/test_photo.py` — AC-8 (8개)
  - `tests/test_video.py` — AC-9 (8개)

### Phase 2 — 확장 테스트

- [ ] T10 @test-dev  도토리 경계값 (`tests/test_acorn_boundaries.py`)
  - `test_spend_exact_balance` — 잔액과 정확히 같은 금액 사용 (성공)
  - `test_spend_zero_balance` — 잔액 0에서 사용 시 즉시 거부
  - `test_charge_then_spend_sequence` — 충전→사용 순서 연속 검증

- [ ] T11 @test-dev  방문자 경계값 (`tests/test_visitor_boundaries.py`)
  - `test_same_visitor_no_duplicate_today` — 당일 재방문 today 불변
  - `test_date_change_resets_today` — 날짜 전환 후 today=0, total 누적
  - `test_different_visitors_count_separately` — 방문자 A·B 각각 카운트

- [ ] T12 @test-dev  멱등 유틸 심화 (`tests/test_idempotency.py`)
  - `idempotency_key` 동일 페이로드·키 순서 무관 동일 해시
  - `IdempotencyStore.issue_once` replay 1회 보장
  - 방명록·도토리 각 1개씩 end-to-end 멱등 검증

- [ ] T13 @test-dev  contract.json 스모크 (`tests/test_contract_smoke.py`)
  - `build`·`proof` 명령 선언 확인
  - SDD `01_planning`·`02_plan`·`04_verify` 경로 존재 확인

---

## 구현 가이드

### conftest.py 픽스처 패턴

```python
import pytest
from server.contexts.profile.profile import ProfileService
from server.contexts.acorn.acorn import AcornService
from server.contexts.visitor.visitor import VisitorService

@pytest.fixture
def profile_svc():
    svc = ProfileService()
    svc.register("u1", nickname="홍길동", intro="안녕하세요", skin="default")
    return svc

@pytest.fixture
def acorn_svc():
    clock = {"t": 1000.0}
    svc = AcornService(clock=lambda: clock["t"])
    return svc, clock

@pytest.fixture
def visitor_svc():
    clock = {"date": "2025-01-01"}
    svc = VisitorService(date_fn=lambda: clock["date"])
    return svc, clock
```

### 에러 클래스 위치

각 context 파일 내 상단에 정의:

```python
# profile.py
class ProfileNotFoundError(Exception): pass

# guestbook.py
class SecretEntryError(Exception): pass
class EntryNotFoundError(Exception): pass

# diary.py
class DiaryNotFoundError(Exception): pass
class DiaryAccessError(Exception): pass

# acorn.py
class InsufficientAcornError(Exception): pass

# buddy.py
class AlreadyBuddyError(Exception): pass
class BuddyRequestNotFoundError(Exception): pass
```

### screens.py 렌더 패턴

```python
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

def render_minihompy(profile, guestbook_preview, buddy_count, visitor_count):
    return MINIHOMPY_HTML.format(
        nickname=profile["nickname"],
        intro=profile["intro"],
        skin=profile["skin"],
        buddy_count=buddy_count,
        visitor_count=visitor_count,
        guestbook_preview=guestbook_preview,
    )
```

---

## Regression Scope

- direct: 미니홈피 전 흐름 (프로필·방명록·다이어리·도토리·일촌·방문자)
- shared: `server/shared/idem.py` (멱등 유틸)

---

## Validation

```bash
# Phase 1 게이트
cd c:\agentic-dev-demo\cy_live
python3 -m compileall -q server
python3 proof/run_proof.py

# Phase 2 게이트 (추가 경계값·유틸·contract)
pytest tests/test_acorn_boundaries.py \
       tests/test_visitor_boundaries.py \
       tests/test_idempotency.py \
       tests/test_contract_smoke.py -v
```
