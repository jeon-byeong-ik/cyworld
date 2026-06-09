# cy_live 서비스 · 운영 런북

## DEV 배포 절차

1. `python3 -m compileall -q server` — 컴파일 에러 없음 확인
2. `python3 proof/run_proof.py` — 39/39 PASS 확인
3. `git add` → `git commit` → `git push`

## 임계치·롤백

| 조건 | 조치 |
| --- | --- |
| proof FAIL 1개 이상 | 커밋 중단, 원인 분석 후 재수정 |
| proof 실행 불가 | `pip install -r requirements.txt` 후 재시도 |

## 감사 항목

- 도토리 충전·사용: `acorn.history(user_id)` — tx_id·타임스탬프 기록
- 방명록 멱등 replay: `(entry_id, is_replay=True)` 반환값으로 추적
- 일촌 상태 전이: PENDING → ACCEPTED / REJECTED 순서 검증

## 빌드·검증 명령 (contract.json)

```bash
python3 -m compileall -q server   # build
python3 proof/run_proof.py        # proof
```
