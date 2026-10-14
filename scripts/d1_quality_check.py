"""1일차: d1_buyers_raw.xlsx 품질 진단 (읽기 전용 — 원본을 고치지 않는다).

실행: uv run python scripts/d1_quality_check.py
결과는 화면에 출력만 한다. 보고서: workbench/day1/outputs/d1_quality_report.md
"""

import collections
import re

import openpyxl
import pandas as pd

SRC = "data/day1/d1_buyers_raw.xlsx"
DICT = "data/data_dictionary.xlsx"
BASE_DATE = pd.Timestamp("2026-09-30")  # readme 시트의 기준일

# 엑셀 셀 값을 변환 없이 그대로 읽는다 (pandas 자동 형변환을 피하려고 openpyxl 사용)
wb = openpyxl.load_workbook(SRC, read_only=True)
rows = list(wb["buyers"].iter_rows(values_only=True))
header, body = list(rows[0]), rows[1:]
df = pd.DataFrame(body, columns=header, dtype=object)
df.index = range(2, len(df) + 2)  # 인덱스 = 엑셀 행 번호(1행은 머리글)


def section(title):
    print(f"\n===== {title} =====")


def is_blank(v):
    return v is None or (isinstance(v, str) and v.strip() == "")


# 1) 열별 개요: 파이썬 셀 유형 분포 · 결측 · 고유값 수
section("열별 개요")
print(f"행 수 {len(df)} · 열 수 {len(df.columns)}")
for c in df.columns:
    types = collections.Counter(type(v).__name__ for v in df[c])
    blanks = sum(is_blank(v) for v in df[c])
    print(f"{c:24s} types={dict(types)} blank={blanks} unique={df[c].nunique(dropna=True)}")

# 2) 중복 행
section("중복: 전체 행 완전 일치")
key = df.astype(str)
full_dup = key[key.duplicated(keep=False)]
print(full_dup[["buyer_id", "buyer_name"]].to_string() if len(full_dup) else "없음")

section("중복: buyer_id")
dup_id = df[df["buyer_id"].duplicated(keep=False)].sort_values("buyer_id")
for bid, g in dup_id.groupby("buyer_id"):
    diff_cols = [c for c in df.columns if g[c].astype(str).nunique() > 1]
    print(bid, "엑셀 행", list(g.index), "다른 열:", diff_cols or "없음(완전 중복)")
    for c in diff_cols:
        print("   ", c, list(g[c]))

section("중복: buyer_name (공백·대소문자 정리 후)")
norm_name = df["buyer_name"].str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
g = df[norm_name.duplicated(keep=False)]
print(g[["buyer_id", "buyer_name"]].sort_values("buyer_name").to_string() if len(g) else "없음")

section("앞뒤 공백이 있는 글자 셀")
for c in df.columns:
    hits = [(i, v) for i, v in df[c].items() if isinstance(v, str) and v != v.strip()]
    if hits:
        print(c, len(hits), hits[:5])

# 3) 범주형 열 값 분포
for c in ["country", "country_code", "region", "industry", "segment", "buyer_type",
          "ar_currency", "ksure_insured", "oecd_crc"]:
    section(f"값 분포: {c}")
    print(dict(collections.Counter(map(repr, df[c]))))

section("country ↔ country_code 대응 (코드별 국가 표기)")
for code, g in df.groupby("country_code"):
    vals = collections.Counter(g["country"])
    if len(vals) > 1:
        print(code, dict(vals))

section("country_code ↔ region / oecd_crc 일관성 (코드별 값이 둘 이상이면 출력)")
for col in ["region", "oecd_crc"]:
    for code, g in df.groupby("country_code"):
        vals = collections.Counter(map(repr, g[col]))
        if len(vals) > 1:
            print(col, code, dict(vals))
print("oecd_crc 국가별 값:", {k: sorted(set(map(repr, g["oecd_crc"]))) for k, g in df.groupby("country_code")})

section("segment ↔ buyer_type ↔ industry")
print(pd.crosstab(df["segment"], df["buyer_type"]))
print(pd.crosstab(df["segment"], df["industry"].fillna("(빈칸)")))
print("industry 빈칸 행:", df[df["industry"].isna()][["buyer_id", "buyer_name", "segment"]].to_dict("records"))

# 4) 결제조건: 코드표(payment_terms_map) 매칭
section("payment_terms_raw 값 분포")
print(dict(collections.Counter(map(repr, df["payment_terms_raw"]))))
pmap = pd.read_excel(DICT, "payment_terms_map", header=2)
lookup = dict(zip(pmap["raw_upper"], pmap["payment_method"]))
upper = df["payment_terms_raw"].str.strip().str.upper()
miss = df.loc[~upper.isin(lookup), "payment_terms_raw"]
print("raw 그대로 일치:", df["payment_terms_raw"].isin(pmap["raw_variant"]).sum())
print("TRIM·UPPER 후 일치:", upper.isin(lookup).sum(), "/ 미일치:", len(miss))
print("미일치 표기:", dict(collections.Counter(map(repr, miss))), "행:", list(miss.index))
print("표준 코드 분포(일치분):", dict(collections.Counter(upper.map(lookup).dropna())))

# 5) 숫자 열에 들어간 글자
NUM_COLS = ["ar_balance", "max_dpd_days", "overdue_amount", "pay_score", "oecd_crc",
            "revenue_usd_fy2025", "current_ratio_fy2025", "debt_to_equity_fy2025",
            "dso_fy2025", "op_margin_fy2025"]
section("숫자 열의 글자 셀")
for c in NUM_COLS:
    hits = [(i, df.at[i, "buyer_id"], v) for i, v in df[c].items() if isinstance(v, str)]
    print(c, len(hits), hits)

section("숫자 열의 소수점 셀 (정수여야 하는 금액·일수·점수)")
for c in ["ar_balance", "max_dpd_days", "overdue_amount", "pay_score", "revenue_usd_fy2025"]:
    hits = [(i, df.at[i, "buyer_id"], v) for i, v in df[c].items() if isinstance(v, float)]
    print(c, hits)


def to_num(v):
    """진단용 숫자 읽기: 숫자 셀만 숫자로, 글자는 None (변환·정제하지 않음)."""
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


num = pd.DataFrame({c: df[c].map(to_num) for c in NUM_COLS}, dtype=float)

section("숫자 열 범위 (숫자 셀만)")
print(num.describe().T.to_string())

section("논리 점검")
ar, od, dpd = num["ar_balance"], num["overdue_amount"], num["max_dpd_days"]
print("음수 금액/일수:", {c: list(num.index[num[c] < 0]) for c in ["ar_balance", "overdue_amount", "max_dpd_days"]})
print("overdue > ar_balance:", df.loc[od > ar, ["buyer_id", "ar_balance", "overdue_amount"]].to_dict("records"))
print("dpd>0 인데 overdue=0:", df.loc[(dpd > 0) & (od == 0), ["buyer_id", "max_dpd_days", "overdue_amount"]].to_dict("records"))
print("dpd=0 인데 overdue>0:", df.loc[(dpd == 0) & (od > 0), ["buyer_id", "max_dpd_days", "overdue_amount"]].to_dict("records"))
print("ar_balance=0 인데 overdue>0:", df.loc[(ar == 0) & (od > 0), ["buyer_id"]].to_dict("records"))
print("pay_score 1~100 밖:", list(num.index[(num["pay_score"] < 1) | (num["pay_score"] > 100)]))
print("current_ratio <= 0:", list(num.index[num["current_ratio_fy2025"] <= 0]))
print("debt_to_equity < 0 (자본잠식):", df.loc[num["debt_to_equity_fy2025"] < 0, ["buyer_id"]].to_dict("records"))
print("op_margin |x|>1 (퍼센트로 입력 의심):", list(num.index[num["op_margin_fy2025"].abs() > 1]))
print("dso 정수 셀:", [(i, v) for i, v in df["dso_fy2025"].items() if isinstance(v, int)])

section("재무 열 결측 패턴")
fin = ["revenue_usd_fy2025", "current_ratio_fy2025", "debt_to_equity_fy2025", "dso_fy2025", "op_margin_fy2025"]
print(collections.Counter(tuple(int(df.at[i, c] is None) for c in fin) for i in df.index))
not_recv = df["fin_summary_text"].str.contains("not received", case=False)
print("'not received' 문구 행:", list(df.index[not_recv]))
print("  그중 revenue 빈칸:", int(num.loc[not_recv, "revenue_usd_fy2025"].isna().sum()))
print("revenue 빈칸인데 'not received' 아님:", list(df.index[num["revenue_usd_fy2025"].isna() & ~not_recv]))

section("fin_summary_text ↔ revenue_usd_fy2025 (문장 속 USD xM 과 비교, 차이 > 0.05M)")
for i, t in df["fin_summary_text"].items():
    m = re.search(r"USD ([\d.]+)M", t or "")
    r = num.at[i, "revenue_usd_fy2025"]
    if m and pd.notna(r) and abs(float(m.group(1)) - r / 1e6) > 0.05:
        print(i, df.at[i, "buyer_id"], m.group(1), r)
    if m and pd.isna(r):
        print(i, df.at[i, "buyer_id"], "문장에 매출 있음, 열은 빈칸", m.group(1))

# 6) 날짜 형식
section("since_date 형식")
PATTERNS = {
    "YYYY-MM-DD": r"^\d{4}-\d{2}-\d{2}$",
    "YYYY.M.D": r"^\d{4}\.\d{1,2}\.\d{1,2}$",
    "DD/MM/YYYY (또는 MM/DD)": r"^\d{2}/\d{2}/\d{4}$",
    "Mon D YYYY": r"^[A-Z][a-z]{2} \d{1,2} \d{4}$",
}
fmt = {}
for i, v in df["since_date"].items():
    s = str(v).strip()
    fmt[i] = next((k for k, p in PATTERNS.items() if re.match(p, s)), "기타")
cnt = collections.Counter(fmt.values())
for k in list(PATTERNS) + ["기타"]:
    ex = [df.at[i, "since_date"] for i in df.index if fmt[i] == k][:3]
    print(k, cnt.get(k, 0), ex)

slash = [df.at[i, "since_date"] for i in df.index if fmt[i].startswith("DD/MM")]
a = [tuple(map(int, s.split("/")[:2])) for s in slash]
print("슬래시형: 앞자리>12(일/월 확정)", sum(x > 12 for x, _ in a),
      "· 뒷자리>12(월/일 확정)", sum(y > 12 for _, y in a),
      "· 둘 다 ≤12(모호)", sum(x <= 12 and y <= 12 for x, y in a))
print("모호 예:", [s for s, (x, y) in zip(slash, a) if x <= 12 and y <= 12][:10])


def parse(s):
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%Y.%m.%d", "%d/%m/%Y", "%b %d %Y"):
        try:
            return pd.to_datetime(s, format=f)
        except ValueError:
            pass
    return pd.NaT


d = df["since_date"].map(parse)
print("해석 실패:", list(d.index[d.isna()]))
print("범위:", d.min().date(), "~", d.max().date())
print("기준일(2026-09-30) 이후:", df.loc[d > BASE_DATE, ["buyer_id", "since_date"]].to_dict("records"))
