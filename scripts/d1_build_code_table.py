"""1일차: payment_terms_raw 표기 → 표준 코드 7종 매핑표 만들기 (원본은 읽기만 한다).

실행: uv run python scripts/d1_build_code_table.py
결과: workbench/day1/outputs/d1_code_table.csv (utf-8-sig)

규칙은 '표기에 들어 있는 단어'로만 판단한다. 단어로 코드가 하나로 정해지지 않으면 '검토 필요'.
마지막에 과정 코드표(data_dictionary.xlsx → payment_terms_map)와 대조해 다른 곳을 화면에 출력한다.
"""

import collections
import re

import openpyxl
import pandas as pd

SRC = "data/day1/d1_buyers_raw.xlsx"
DICT = "data/data_dictionary.xlsx"
OUT = "workbench/day1/outputs/d1_code_table.csv"
REVIEW = "검토 필요"


def word(pat):
    """앞뒤가 영문자가 아닐 때만 맞는 패턴 (예: DA가 DAYS 안에서 맞지 않게)."""
    return re.compile(rf"(?<![A-Z]){pat}(?![A-Z])")


TT = word(r"T/?T")
OA = word(r"O/?A")
DA = word(r"D/?A")
DP = word(r"D/?P")
LC = word(r"L/?C")
DAYS = re.compile(r"\d+\s*D(AYS?)?(?![A-Z])")  # 90 DAYS · 60DAYS · 90D
NET = re.compile(r"\bNET\s*\d+")
PCT = re.compile(r"(\d+)%")


def classify(raw):
    """표기 1개 → (표준 코드, 판단 근거, 확신). 위에서부터 처음 맞는 규칙을 쓴다."""
    s = raw.strip().upper()
    pcts = PCT.findall(s)

    # 1) 선수 + 잔금 분할
    if "30/70" in s or "30:70" in s or (pcts[:2] == ["30", "70"] and "ADVANCE" in s):
        return "TT_SPLIT_30_70", "'30/70'(또는 '30% advance + 70%') = 선수 30% + 잔금 70%", "높음"
    if pcts and pcts != ["100"]:
        return REVIEW, f"'{'%/'.join(pcts)}%' 분할 — 표준 코드의 분할 비율(30/70)과 다름. 7종 중 맞는 코드 없음", "낮음"

    # 2) 선수금
    if "IN ADVANCE" in s or "BEFORE SHIPMENT" in s:
        key = "in advance" if "IN ADVANCE" in s else "before shipment"
        return "TT_ADV", f"'{key}' = 선적 전 송금", "높음"

    # 3) 신용장
    if LC.search(s) or "신용장" in raw:
        key = LC.search(s).group() if LC.search(s) else "신용장"
        if "SIGHT" in s or "일람불" in raw:
            return "LC_SIGHT", f"'{key}' + '{'at sight' if 'SIGHT' in s else '일람불'}' = 일람불 신용장", "높음"
        if "USANCE" in s:
            return "LC_USANCE", f"'{key}' + 'usance' = 기한부 신용장", "높음"
        if DAYS.search(s):
            return "LC_USANCE", f"'{key}' + 일수('{DAYS.search(s).group()}') → 기한부로 판단. 'usance' 단어는 없음", "낮음"
        return REVIEW, f"'{key}'만 있고 일람불/기한부 구분 단어 없음", "낮음"

    # 4) 추심 (D/P · D/A)
    if DP.search(s) or "DOCUMENTS AGAINST PAYMENT" in s:
        return "DP", f"'{DP.search(s).group() if DP.search(s) else 'Documents against payment'}' = 지급인도조건", "높음"
    if DA.search(s) or "DOCUMENTS AGAINST ACCEPTANCE" in s:
        key = DA.search(s).group() if DA.search(s) else "Documents against acceptance"
        return "DA", f"'{key}' = 인수인도조건", "높음"

    # 5) 사후송금 (오픈어카운트)
    if OA.search(s):
        return "OA", f"'{OA.search(s).group()}' = Open account", "높음"
    if "OPEN ACCOUNT" in s or "OPEN ACCT" in s:
        return "OA", f"'{'open account' if 'OPEN ACCOUNT' in s else 'open acct'}' = Open account", "높음"
    if NET.search(s):
        return "OA", f"'{NET.search(s).group().title()}' = 송장 후 N일 송금(Net N) = 사후송금", "높음"
    if TT.search(s) and DAYS.search(s):
        return "OA", f"'{TT.search(s).group()}' + 일수('{DAYS.search(s).group()}') = 선적 후 송금 = 사후송금", "높음"

    # 6) 단어만으로 못 정함
    if TT.search(s):
        return REVIEW, f"'{TT.search(s).group()}'(T/T 송금)만 있음 — 선적 전(TT_ADV)인지 선적 후(OA)인지 나타내는 단어 없음", "낮음"
    return REVIEW, "규칙에 맞는 단어 없음", "낮음"


def main():
    ws = openpyxl.load_workbook(SRC, read_only=True)["buyers"]
    rows = list(ws.iter_rows(values_only=True))
    col = rows[0].index("payment_terms_raw")
    counts = collections.Counter(r[col] for r in rows[1:])

    table = pd.DataFrame(
        [(raw, *classify(raw)) for raw in counts],
        columns=["원래 표기", "표준 코드", "판단 근거(어느 단어로)", "확신(높음/낮음)"],
    )
    order = ["TT_ADV", "TT_SPLIT_30_70", "LC_SIGHT", "LC_USANCE", "DP", "DA", "OA", REVIEW]
    table["_o"] = table["표준 코드"].map(order.index)
    table["_k"] = table["원래 표기"].str.strip().str.upper()
    table = table.sort_values(["_o", "_k", "원래 표기"]).drop(columns=["_o", "_k"])
    table.to_csv(OUT, index=False, encoding="utf-8-sig")

    print(f"표기 {len(table)}종 (셀 {sum(counts.values())}개) → {OUT}")
    cell = table["원래 표기"].map(counts)
    print(pd.DataFrame({"표기 종류": table.groupby("표준 코드").size(),
                        "셀 수": cell.groupby(table["표준 코드"]).sum()}).reindex(order).fillna(0).astype(int))
    print("확신:", dict(collections.Counter(table["확신(높음/낮음)"])))

    # 과정 코드표와 대조 (TRIM·UPPER 키)
    pmap = pd.read_excel(DICT, "payment_terms_map", header=2)
    ref = dict(zip(pmap["raw_upper"], pmap["payment_method"]))
    print("\n과정 코드표와 다른 곳:")
    for _, r in table.iterrows():
        key = r["원래 표기"].strip().upper()
        if ref.get(key) != r["표준 코드"]:
            print(f"  {r['원래 표기']!r:45} 내 코드 {r['표준 코드']:15} 과정 코드표 {ref.get(key, '(없음)')}")


if __name__ == "__main__":
    main()
