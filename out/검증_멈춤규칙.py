# -*- coding: utf-8 -*-
"""검증_멈춤규칙.py — CLAUDE.md 6번 규칙(사람이 정할 것은 대신 정하지 않는다)이 지켜졌는지 확인한다.

확인하는 것 (out/ 아래 원고 폴더마다):
  ① 03_원문.md `## 뺀 주장`에 있는 C번호마다, 03이나 04의 `## 사람 결정`에 그 C번호와 '빼기'가 한 줄에 적혀 있는가
  ② 01_기획.md에서 독자 · 핵심 메시지가 〔제안〕이면, 01_기획.md `## 사람 결정`에 그 항목이 적혀 있는가

읽기만 하고 아무 파일도 고치지 않는다.
쓰는 법(이 폴더의 위 폴더에서):  python out/검증_멈춤규칙.py
결과: 모두 통과면 종료 코드 0, 하나라도 실패면 1
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = Path(__file__).resolve().parent


def section(text, title):
    """'## title'로 시작하는 절의 본문(다음 '## ' 전까지)을 돌려준다. 없으면 None."""
    m = re.search(r"^##\s*" + re.escape(title) + r"[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


def claim_ids(text):
    # 줄 맨 앞 '- C4 …' · '- C6c …' 꼴만 C번호로 본다 (C4-2처럼 '-숫자'가 붙은 것은 다른 주장)
    ids = []
    for line in text.splitlines():
        m = re.match(r"\s*[-*]\s*(C\d+[a-z]?(?:-\d+)?)\b", line)
        if m:
            ids.append(m.group(1))
    return ids


def decided_drop(cid, decisions):
    pat = re.compile(re.escape(cid) + r"(?![\w-])")
    return any(pat.search(l) and "빼기" in l for l in decisions.splitlines())


def check_folder(d):
    fails, passes = [], []
    t01, t03, t04 = read(d / "01_기획.md"), read(d / "03_원문.md"), read(d / "04_출처.md")

    # ① 뺀 주장 ↔ 사람 결정
    dropped = section(t03, "뺀 주장")
    if dropped is not None:
        decisions = (section(t03, "사람 결정") or "") + "\n" + (section(t04, "사람 결정") or "")
        for cid in claim_ids(dropped):
            if decided_drop(cid, decisions):
                passes.append(f"① {cid} 빼기 — 사람 결정 있음")
            else:
                fails.append(f"① {cid} — 03 '뺀 주장'에 있으나 03 · 04 '사람 결정'에 '{cid} … 빼기' 없음")

    # ② 01의 〔제안〕 ↔ 사람 결정
    if t01:
        dec01 = section(t01, "사람 결정") or ""
        for field in ("독자", "핵심 메시지"):
            m = re.search(r"^\s*[-*]\s*" + field + r"\s*:(.*)$", t01, re.M)
            if m and "〔제안〕" in m.group(1):
                if field in dec01:
                    passes.append(f"② {field} 〔제안〕 — 사람 결정 있음")
                else:
                    fails.append(f"② {field} — 01에 〔제안〕으로 채웠으나 01 '사람 결정'에 {field} 확정 기록 없음")
    return passes, fails


def main():
    folders = sorted(p for p in OUT.iterdir() if p.is_dir() and (p / "진행상태.md").exists())
    if not folders:
        print("검사할 원고 폴더(진행상태.md가 있는 out/ 하위 폴더)가 없음")
        return 0
    total_fail = 0
    for d in folders:
        passes, fails = check_folder(d)
        print(f"[{d.name}]")
        for s in passes:
            print("  통과", s)
        for s in fails:
            print("  실패", s)
        if not passes and not fails:
            print("  해당 없음 (뺀 주장 · 〔제안〕 없음)")
        total_fail += len(fails)
    print(f"\n결과: 실패 {total_fail}건 — {'규칙 위반 있음' if total_fail else '모두 통과'}")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())
