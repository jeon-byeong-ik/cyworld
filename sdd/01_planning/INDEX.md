# cy_live · Planning Index

> 01_planning 폴더의 명세 목록. 각 명세는 검증 가능한 EARS 형식으로 작성.

| 명세 | 파일 | 상태 | AC 수 |
| --- | --- | --- | --- |
| 싸이월드 미니홈피 클론 | `01_feature/cyworld_feature_spec.md` | 🟡 진행중 | AC-1~7 |

---

## 도메인 구성

| context | 역할 | AC |
| --- | --- | --- |
| `profile` | 미니홈피 프로필 조회·수정 | AC-1 |
| `guestbook` | 방명록 CRUD + 멱등 + 비밀글 | AC-2 |
| `diary` | 다이어리 CRUD + 댓글 + 공개 제어 | AC-3 |
| `acorn` | 도토리 충전·사용·잔액 + 멱등 | AC-4 |
| `buddy` | 일촌 신청·수락·거절·목록 | AC-5 |
| `visitor` | 방문자 카운터 (중복 방지·일별 초기화) | AC-6 |
| `screens` | 미니홈피 HTML 렌더 (UI parity 게이트) | AC-7 |
