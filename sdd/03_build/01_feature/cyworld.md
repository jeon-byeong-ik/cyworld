# 싸이월드 미니홈피 클론 · Build 현황

## 모듈 구성 및 AC 매핑

| 모듈 | 파일 | 역할 | AC |
| --- | --- | --- | --- |
| shared | `server/shared/idem.py` | SHA256 멱등 키·IdempotencyStore | AC-2·4 |
| profile | `server/contexts/profile/profile.py` | 프로필 등록·조회·수정 | AC-1 |
| profile | `server/contexts/profile/screens.py` | 미니홈피 HTML 렌더 | AC-7 |
| guestbook | `server/contexts/guestbook/guestbook.py` | 방명록 CRUD·비밀글·멱등 | AC-2 |
| diary | `server/contexts/diary/diary.py` | 다이어리 CRUD·공개제어·댓글 | AC-3 |
| acorn | `server/contexts/acorn/acorn.py` | 도토리 충전·사용·잔액·멱등 | AC-4 |
| buddy | `server/contexts/buddy/buddy.py` | 일촌 신청·수락·거절·목록 | AC-5 |
| visitor | `server/contexts/visitor/visitor.py` | 방문자 카운터·중복방지·날짜 초기화 | AC-6 |

## 테스트 커버리지

| 파일 | 테스트 수 | 대상 AC |
| --- | --- | --- |
| `test_profile.py` | 3 | AC-1 |
| `test_guestbook.py` | 4 | AC-2 |
| `test_diary.py` | 5 | AC-3 |
| `test_acorn.py` | 4 | AC-4 |
| `test_buddy.py` | 5 | AC-5 |
| `test_visitor.py` | 3 | AC-6 |
| `test_screen_parity.py` | 2 | AC-7 |
| `test_acorn_boundaries.py` | 3 | AC-4 경계값 |
| `test_visitor_boundaries.py` | 3 | AC-6 경계값 |
| `test_idempotency.py` | 5 | 멱등 유틸 |
| `test_contract_smoke.py` | 2 | contract 정합 |
| **합계** | **39** | **AC-1~7 전체** |

## 샘플 사용자

| user_id | 닉네임 | 역할 |
| --- | --- | --- |
| `jbi` | 전병익 | 메인 홈피 주인 (프로필 이미지: `static/images/profile.jpg`) |
| `u2` | 김영희 | 일촌·방명록 작성자 |
| `u3` | 이민준 | 일촌 |

## 정적 파일

| 경로 | 원본 | 설명 |
| --- | --- | --- |
| `static/images/profile.jpg` | `sdd-contrast/image/spec/싸이월드 사진.jpg` | 전병익 프로필 사진 |

## UI 재현 스펙 (실제 싸이월드 기준)

| 요소 | 구현 값 |
| --- | --- |
| 전체 너비 | 780px (콘텐츠) + body 격자 배경 |
| body 배경 | `#9ab0c8` + 18px 격자 (`linear-gradient` 구현) |
| 좌측 사이드바 | 174px, 배경 `#c4d8ed`→`#b4cce0` |
| 방문자 바 | `#606878` 다크, 흰 텍스트 TODAY/TOTAL |
| TODAY IS 박스 | `#fffde8`→`#fffacc` 크림, border `#d4c040` |
| 스파이럴 바인더 링 | 18px 흰 원 × 6개, 좌·중 패널 경계 절대 위치 |
| 중앙 패널 | `#fff`, border-left 4px `#88aac8`, max-height 520px scroll |
| 타이틀 바 | `#d8eef8`→`#c4e0f0` 그라디언트, 굵은 파란 타이틀 |
| 미니룸 섹션 | 프로필 사진 + 말풍선 씬 (Flash 대체) |
| 우측 사이드바 | 112px, `#3c3c44` 다크 |
| 네비 버튼 | `#2e6878`→`#1e5060` 청록 그라디언트, active `#183c50` |
| 액티브/페이머스/팬들리 | `#fff8e0` 크림 배경, 오렌지 게이지 바 |
| 음악 플레이어 | `#2e2e38` 다크, 파란 컨트롤 |

## 설계 결정

- **결정적 테스트**: clock·date_fn 주입으로 시간·날짜 비의존
- **멱등성**: SHA256 해시 기반 `idempotency_key` — 방명록 write·도토리 charge 적용
- **visitor total**: 중복 방문도 total 증가 (today 만 중복 차단) — AC-6a 명세 준수
- **frozenset key**: buddy 관계를 방향 무관 `frozenset({a, b})`로 저장
- **UI 디자인**: 실제 싸이월드(`sdd-contrast/image/spec/싸이월드.jpg`) 참고 — 격자 배경·좌우 사이드바·파란 버튼 네비 재현
