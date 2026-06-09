# 싸이월드 미니홈피 클론 · Acceptance Criteria (EARS)

> 01_planning: 요구사항을 검증 가능한 EARS로 정제. 이 명세가 가드레일.

---

## AC-1 미니홈피 프로필

**AC-1a** When 사용자가 미니홈피를 조회하면, the system shall
닉네임·자기소개·스킨명·일촌 수·방문자 수를 반환한다.

**AC-1b** When 존재하지 않는 user_id로 조회하면, the system shall
`ProfileNotFoundError`를 발생시킨다.

**AC-1c** When 홈피 주인이 프로필을 수정하면, the system shall
닉네임·자기소개·스킨이 즉시 반영된다.

---

## AC-2 방명록 (Guestbook)

**AC-2a** When 방문자가 방명록에 글을 작성하면, the system shall
작성자·내용·타임스탬프를 저장하고 글 ID를 반환한다.

**AC-2b** When 비밀글로 작성하면, the system shall
홈피 주인과 작성자만 내용을 조회할 수 있고, 제3자에게는 `SecretEntryError`를 발생시킨다.

**AC-2c** When 동일 idempotency_key로 재작성 요청이 오면, the system shall
중복 저장 없이 기존 글 ID를 반환한다 (멱등성).

**AC-2d** When 홈피 주인이 글을 삭제하면, the system shall
해당 글을 목록에서 제거한다.

---

## AC-3 다이어리 (Diary)

**AC-3a** When 홈피 주인이 다이어리를 작성하면, the system shall
제목·내용·공개여부·타임스탬프를 저장한다.

**AC-3b** When 비공개 글을 제3자가 조회하면, the system shall
`DiaryAccessError`를 발생시킨다.

**AC-3c** When 홈피 주인이 다이어리를 수정하면, the system shall
내용·공개여부를 갱신한다.

**AC-3d** When 방문자가 댓글을 달면, the system shall
댓글 목록에 작성자·내용·타임스탬프를 추가한다.

**AC-3e** When 홈피 주인이 다이어리를 삭제하면, the system shall
댓글을 포함하여 모두 제거한다.

---

## AC-4 도토리 (Acorn)

**AC-4a** When 사용자가 도토리를 충전하면, the system shall
잔액이 증가하고 트랜잭션 ID·타임스탬프가 기록된다.

**AC-4b** When 사용자가 도토리를 사용하면, the system shall
잔액이 감소하고 트랜잭션 ID·타임스탬프가 기록된다.

**AC-4c** When 잔액이 부족한 상태에서 사용 요청이 오면, the system shall
`InsufficientAcornError`를 발생시키고 잔액은 변경하지 않는다.

**AC-4d** When 동일 idempotency_key로 충전 요청이 재발생하면, the system shall
중복 충전 없이 기존 트랜잭션 ID를 반환한다 (멱등성).

---

## AC-5 일촌 (Buddy)

**AC-5a** When 사용자가 일촌 신청을 하면, the system shall
관계 상태가 `PENDING`으로 저장된다.

**AC-5b** When 상대방이 일촌 신청을 수락하면, the system shall
양방향 관계가 `ACCEPTED`로 성립된다.

**AC-5c** When 상대방이 일촌 신청을 거절하면, the system shall
관계 상태가 `REJECTED`로 변경된다.

**AC-5d** When 이미 `ACCEPTED` 관계인 사용자에게 재신청하면, the system shall
`AlreadyBuddyError`를 발생시킨다.

**AC-5e** When 일촌 목록을 조회하면, the system shall
`ACCEPTED` 관계만 반환한다.

---

## AC-6 방문자 카운터 (Visitor)

**AC-6a** When 방문자가 미니홈피를 방문하면, the system shall
오늘 방문자 수와 전체 방문자 수를 각각 1 증가시킨다.

**AC-6b** When 같은 방문자가 당일 재방문하면, the system shall
오늘 방문자 수를 증가시키지 않는다 (중복 방지).

**AC-6c** When 날짜가 바뀌면, the system shall
오늘 방문자 수를 0으로 초기화하되 전체 방문자 수는 누적 유지한다.

---

## AC-7 화면 (Screen Parity)

**AC-7** The minihompy 화면은 shall 닉네임·자기소개·일촌 수·방문자 수·방명록
미리보기가 포함된 승인 스냅샷과 일치한다 (UI parity).

---

## AC-8 사진첩 (Photo Album)

**AC-8a** When 사용자가 앨범을 생성하면, the system shall
앨범 ID·이름·소유자를 저장하고 반환한다.

**AC-8b** When 사용자가 사진을 앨범에 추가하면, the system shall
제목·설명·이미지 URL·앨범 ID·소유자를 저장하고 photo_id를 반환한다.

**AC-8c** When 존재하지 않는 album_id로 사진을 추가하면, the system shall
`AlbumNotFoundError`를 발생시킨다.

**AC-8d** When 사용자가 전체 사진 목록을 조회하면, the system shall
해당 사용자의 모든 사진을 반환한다.

**AC-8e** When 앨범 ID를 지정하여 사진 목록을 조회하면, the system shall
해당 앨범의 사진만 반환한다.

**AC-8f** When 사진을 삭제하면, the system shall
해당 사진을 목록에서 제거한다.

**AC-8g** When 존재하지 않는 photo_id를 조회하면, the system shall
`PhotoNotFoundError`를 발생시킨다.

---

## AC-9 동영상 게시판 (Video Board)

**AC-9a** When 사용자가 동영상을 추가하면, the system shall
제목·설명·썸네일 URL·소유자를 저장하고 video_id를 반환한다.

**AC-9b** When 사용자가 동영상 목록을 조회하면, the system shall
해당 사용자의 동영상만 반환한다.

**AC-9c** When 동영상을 삭제하면, the system shall
해당 동영상을 목록에서 제거한다.

**AC-9d** When 존재하지 않는 video_id를 조회하거나 삭제하면, the system shall
`VideoNotFoundError`를 발생시킨다.

---

## AC-10 프로필 수정 화면 (Profile Edit)

**AC-10a** When 홈피 주인이 프로필 수정 화면을 요청하면, the system shall
닉네임·자기소개·스킨 편집 폼을 반환한다.

**AC-10b** When 홈피 주인이 프로필을 저장하면, the system shall
닉네임·자기소개·스킨이 즉시 반영되고 `{"ok": true}`를 반환한다.

**AC-10c** When 존재하지 않는 user_id로 프로필 저장을 요청하면, the system shall
`{"ok": false}`를 반환한다.

---

## 검증 매핑

| AC | 테스트 파일 |
| --- | --- |
| AC-1 | `tests/test_profile.py` |
| AC-2 | `tests/test_guestbook.py` |
| AC-3 | `tests/test_diary.py` |
| AC-4 | `tests/test_acorn.py` |
| AC-5 | `tests/test_buddy.py` |
| AC-6 | `tests/test_visitor.py` |
| AC-7 | `tests/test_screen_parity.py` + `sdd/99_toolchain/01_automation/run_ui_parity.py` |
| AC-8 | `tests/test_photo.py` |
| AC-9 | `tests/test_video.py` |
| AC-10 | `tests/test_profile.py` (AC-1c 커버) |
| 경계값 | `tests/test_acorn_boundaries.py`, `tests/test_visitor_boundaries.py` |
| 멱등 유틸 | `tests/test_idempotency.py` |
| contract | `tests/test_contract_smoke.py` |
