# -*- coding: utf-8 -*-
"""contract.json 정합: 명령 선언·SDD 경로 존재."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".agentic-dev" / "contract.json"


def test_contract_required_commands():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    cmds = data.get("commands", {})
    assert "build" in cmds, "build 명령 없음"
    assert "proof" in cmds, "proof 명령 없음"


def test_contract_sdd_paths_exist():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    sdd = data.get("integrations", {}).get("sdd", {})
    for key in ("plan_dir", "verify_dir"):
        path = ROOT / sdd[key]
        assert path.exists(), f"SDD 경로 없음: {sdd[key]}"
