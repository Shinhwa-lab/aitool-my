"""1일차: 바이어 원본 + 내 코드표 → EDA용 분석 표 (메모리에서만 만든다. 원본은 읽기만 한다).

사용: from scripts.d1_clean_buyers import build_analysis_table
      df = build_analysis_table()
점검: uv run python scripts/d1_clean_buyers.py   (행 수 · 규칙별 결과를 화면에 출력)

정리 규칙 (근거: workbench/day1/outputs/d1_quality_report.md)
  R1 중복 제거   buyer_id 기준 첫 행만 남긴다 (153 → 150). 보고서 2절: 중복 3건은 이름 표기 외 값이 같다.
  R2 결제방식    payment_terms_raw를 코드표 '원래 표기'와 글자 그대로(공백 포함) 맞춰 pay_code · pay_code_conf를 붙인다.
                 맞지 않는 표기가 있으면 멈춘다 (추측으로 채우지 않는다).
  R3 연체일      '90일' · '381 days'처럼 숫자 + 단위인 글자는 숫자만 남긴다.
                 '-' · '확인중'은 0으로 채우지 않고 빈칸(NaN) + dpd_status='확인필요'. 보고서 3-1절.
  R4 연체 여부   is_overdue = max_dpd_days > 0. 연체일이 확인필요면 빈칸(pd.NA) — 비율의 분모에서 뺀다.
"""

import re

import pandas as pd

SRC = "data/day1/d1_buyers_raw.xlsx"
CODE_TABLE = "workbench/day1/outputs/d1_code_table.csv"
DPD_UNKNOWN = "확인필요"

NUM_WITH_UNIT = re.compile(r"^\s*(\d+)\s*(일|days?)?\s*$", re.IGNORECASE)


def parse_dpd(v):
    """max_dpd_days 셀 1개 → 숫자(int) 또는 None(확인필요)."""
    if isinstance(v, (int, float)) and not pd.isna(v):
        return int(v)
    m = NUM_WITH_UNIT.match(str(v))
    return int(m.group(1)) if m else None


def build_analysis_table(src=SRC, code_table=CODE_TABLE):
    raw = pd.read_excel(src, sheet_name="buyers")
    codes = pd.read_csv(code_table, encoding="utf-8-sig")

    # R1 중복 제거
    df = raw.drop_duplicates(subset="buyer_id", keep="first").reset_index(drop=True)

    # R2 결제방식 → 표준 코드 (글자 그대로 조회)
    code_map = codes.set_index("원래 표기")
    missing = sorted(set(df["payment_terms_raw"]) - set(code_map.index))
    if missing:
        raise ValueError(f"코드표에 없는 결제조건 표기: {missing}")
    df["pay_code"] = df["payment_terms_raw"].map(code_map["표준 코드"])
    df["pay_code_conf"] = df["payment_terms_raw"].map(code_map["확신(높음/낮음)"])

    # R3 연체일 숫자화
    df["max_dpd_days_raw"] = df["max_dpd_days"].astype(str)
    df["max_dpd_days"] = pd.array([parse_dpd(v) for v in df["max_dpd_days"]], dtype="Int64")
    df["dpd_status"] = df["max_dpd_days"].isna().map({True: DPD_UNKNOWN, False: "숫자"})

    # R4 연체 여부 (확인필요는 NA)
    df["is_overdue"] = (df["max_dpd_days"] > 0).astype("boolean")
    return df


if __name__ == "__main__":
    df = build_analysis_table()
    print("행 수:", len(df), "/ buyer_id 고유:", df["buyer_id"].nunique())
    print("표준 코드:", df["pay_code"].value_counts().to_dict())
    print("연체일 확인필요:", df.loc[df["dpd_status"] == DPD_UNKNOWN, ["buyer_id", "max_dpd_days_raw"]].to_dict("records"))
    print("연체 바이어:", int(df["is_overdue"].sum()), "/ 판정 가능", int(df["is_overdue"].notna().sum()))
