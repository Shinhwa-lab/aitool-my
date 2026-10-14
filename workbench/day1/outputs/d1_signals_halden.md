# Halden Industrial Supplies Ltd. — 대금 지급 위험 신호 점검 (1일차 A-2)

- 원문: `data/day1/reports/halden_fictional_annual_report.md` (가상 연차보고서, FY2026 = 2025-07-01 ~ 2026-06-30)
- 관점: 수출기업 신용관리 분석가 · 이 바이어에게 60일 O/A(사후송금)로 수출하는 경우
- 위치 표기는 보고서 안의 `[H번호]`와 쪽 번호. 인용은 원문(영문) 그대로 옮겼다.
- 판단 · 결정은 사람이 한다. 이 문서는 근거 정리용 초안이다.

## 1. 위험 신호 표

### 체크리스트 8개 유형

| 신호 | 원문 인용 | 위치 | 심각도 |
|---|---|---|---|
| ① 계속기업 불확실성 — 감사인이 '중요한 불확실성'을 명시 | "these events or conditions, along with the other matters set out in note 2, indicate that a material uncertainty exists that may cast significant doubt on the Company's ability to continue as a going concern." | [H5] Independent Auditor's Report, p. 14 | 상 |
| ① 계속기업 불확실성 — 경영진도 같은 불확실성을 인정, 전제는 차입 연장 · EBITDA 약정 충족 · 공급사 결제조건 유지 | "The forecasts assume that the revolving credit facility, which expires on 31 March 2027, is renewed on similar terms, that the Company meets the minimum EBITDA covenant at 31 December 2026 and that current supplier payment terms are maintained." | [H8] Note 2, p. 21 | 상 |
| ② 유동성 부족 — 기본 시나리오에서도 2026년 11월 여유 한도가 £0.9m에 불과 | "In the base case the Company operates within its facilities, with minimum headroom of £0.9 million in November 2026." | [H8] Note 2, p. 21 | 상 |
| ② 유동성 부족 — 공급사 금융(supplier finance) 한도 £10.0m → £3.0m 축소. 기말 이용액 £7.6m보다 작다 (7.6 − 3.0 = £4.6m 초과) | "Following its annual review, the bank reduced the programme limit from £10.0 million to £3.0 million with effect from 1 August 2026." / "Trade payables include £7.6 million (2025: £3.9 million) of invoices confirmed under a supplier finance programme" | [H8] Note 16, p. 31 | 상 |
| ② 유동성 부족 — 현금 감소: £2,860k → £1,140k | "Cash and cash equivalents \| 1,140 \| 2,860" | [H7] Statement of Financial Position, p. 19 | 중 |
| ② 유동성 부족 — 영업현금흐름 £1.9m 중 £4.4m가 운전자본 조정에서 나옴 (1.9 − 4.4 = −£2.5m, 운전자본 효과를 빼면 마이너스) | "Net cash generated from operating activities was £1.9 million (2025: £4.6 million), of which working capital initiatives contributed £4.4 million." | [H3] Financial Review, p. 5 | 중 |
| ③ 차입 약정 위반 — 레버리지 약정 위반 후 은행 면제(waiver) | "The Company did not meet the leverage covenant (net debt to EBITDA of not more than 3.0 times) at the 31 March 2026 test date." | [H8] Note 15, p. 30 (같은 내용 [H3] p. 5) | 상 |
| ③ 차입 약정 위반 — 면제 조건이 무거움: 한도 £15.0m → £11.0m, 가산금리 2.25% → 3.75%, 최소 EBITDA £2.5m 약정 | "(i) the facility limit was reduced from £15.0 million to £11.0 million; (ii) the margin increased from 2.25% to 3.75% over SONIA; (iii) until the facility is refinanced, the leverage covenant is replaced by a minimum EBITDA covenant of £2.5 million for the twelve months to 31 December 2026" | [H8] Note 15, p. 30 | 상 |
| ③ 차입 약정 위반 — 매출이 기본 시나리오보다 5%만 낮아도 2026-12-31 약정 미달 → 추가 면제 필요. 참고로 FY2026 EBITDA는 £1.1m([H2])로 약정 £2.5m보다 낮다 (측정 기간이 달라 직접 비교는 '확인 필요') | "In a reasonably possible downside scenario, in which revenue is 5% below the base case, the Company would not meet the minimum EBITDA covenant at 31 December 2026 and would require a further waiver from the bank." | [H8] Note 2, p. 21 | 상 |
| ④ 차입 만기 — 회전신용한도 2027-03-31 만기, 연장 조건 미합의, 유동부채로 재분류 | "The facility expires on 31 March 2027. Discussions on a renewal have commenced, but no terms had been agreed at the date of approval of these financial statements. Accordingly, the amount drawn of £8.4 million is presented within current liabilities (2025: £9.0 million, within non-current liabilities)." | [H8] Note 15, p. 30 | 상 |
| ⑤ 매출 감소 · 영업손실 — 매출 −7.0%, 영업손실 전환 | "Revenue was £86.4 million (2025: £93.0 million), a decrease of 7.0%" / "we reported an operating loss of £0.9 million (2025: operating profit of £3.5 million)." | [H1] Chief Executive's Review, p. 3 | 중 |
| ⑤ 매출 감소 · 영업손실 — 당기순손실, 금융비용 증가 | "(Loss)/profit for the year \| (1,770) \| 1,890" / "Finance costs \| (1,240) \| (980)" | [H6] Statement of Profit or Loss, p. 18 | 중 |
| ⑤ 매출 감소 · 영업손실 — 매출총이익률 하락 (가격 경쟁 · 달러 매입 원가) | "Gross margin was 20.4% (2025: 23.0%), reflecting price competition and the higher cost of US dollar-denominated purchases." | [H1] Chief Executive's Review, p. 3 | 중 |
| ⑥ 자본잠식 | 명시되지 않음 (순자산 £21,110k > 자본금 £2,000k, 이익잉여금 £19,110k로 양수. 순자산 감소 22,880 − 21,110 = £1,770k는 당기순손실과 같은 금액) | [H7] p. 19 | — |
| ⑦ 결제조건 변경 — 아시아(한국 포함) 공급사 결제기간 60일 → 90일 연장, 신용장(L/C) → O/A 전환 | "we agreed revised terms with several of our principal suppliers in Korea, Japan and Taiwan, extending standard payment terms from 60 to 90 days from the bill of lading date and replacing documentary letters of credit with open account terms for suppliers representing approximately 35% of our purchases. Creditor days increased to 88 (2025: 62)." | [H3] Financial Review, p. 5 | 상 |
| ⑦ 결제조건 변경 — 일부 공급사의 기간 연장은 조기지급 프로그램을 전제로 했는데, 그 한도가 축소됨 | "Certain suppliers agreed to extended payment terms on the basis that early payment would be available under the programme." | [H8] Note 16, p. 31 | 상 |
| ⑦ 결제조건 변경 — 최대 고객에게는 90일 결제를 허용 → 매출채권 증가 · 회수 지연 | "mainly reflecting the move of our largest customer to 90-day payment terms from January 2026 and the timing of shipments in June. Debtor days were 79 (2025: 59)." | [H3] Financial Review, p. 5 | 중 |
| ⑧ 구조조정 | 명시되지 않음 (인원 감축 · 사업 철수 · 구조조정 비용에 대한 기술 없음. 관련 표현은 "We have taken decisive action on costs and working capital" [H1] p. 3 정도이며, 구조조정으로 볼 근거는 없음) | — | — |

### 체크리스트 밖의 추가 신호

| 신호 | 원문 인용 | 위치 | 심각도 |
|---|---|---|---|
| 담보 순위 — 은행이 전 자산에 고정 · 부동 담보 설정. 무담보 외상 채권자(우리)는 후순위 | "is secured by a fixed and floating charge over all of the Company's assets." | [H8] Note 15, p. 30 | 상 |
| 고객 집중 — 최대 고객 31%, 상위 3개 52% | "Our largest customer accounted for 31% of revenue (2025: 24%) and our three largest customers for 52% (2025: 44%)." | [H4] Principal Risks, p. 7 | 중 |
| 매출채권 연체 증가 — 60일 초과 연체 £0.9m → £2.6m | "Trade receivables more than 60 days past due were £2.6 million (2025: £0.9 million)." | [H8] Note 13, p. 28 | 중 |
| 회사 스스로 공급사 결제조건 · 신용 변화가 유동성 위험이라고 기재 | "Changes to the payment terms or to the availability of credit offered by our suppliers could affect our liquidity." | [H4] Principal Risks, p. 7 | 중 |
| 순차입금 증가 — £6.1m → £7.2m | "Net debt excluding lease liabilities was £7.2 million (2025: £6.1 million)." | [H3] Financial Review, p. 5 | 하 |

## 2. 안심 요소 표

| 안심 요소 | 원문 인용 | 위치 | 한계 |
|---|---|---|---|
| 모회사 증자 £4.0m (2026-09-05 현금 납입, 운전자본 용도) | "On 5 September 2026, Altmoor Holdings Ltd, the Company's parent company, subscribed £4.0 million in cash for 4,000,000 new ordinary shares of £1 each. The proceeds were received on that date and will be used for working capital." | [H8] Note 24, p. 34 | 증자를 반영하고도 감사인은 중요한 불확실성을 유지([H5]). 추가 지원 여부는 명시되지 않음 |
| 은행이 약정 위반을 면제했고 연장 협의 시작 | "On 12 May 2026 the bank waived the breach in respect of the 31 March and 30 June 2026 test dates." / "Discussions on a renewal have commenced" | [H8] Note 15, p. 30 | 면제 대가로 한도 축소 · 금리 인상. 연장 조건은 미합의 |
| 감사의견은 변형되지 않음 (적정) | "Our opinion is not modified in respect of this matter." | [H5] Independent Auditor's Report, p. 14 | 계속기업 불확실성 강조는 그대로 있음 |
| 순자산 양수, 자본잠식 없음 | "Net assets \| 21,110 \| 22,880" | [H7] Statement of Financial Position, p. 19 | 손실만큼 줄고 있음 |
| 매출채권의 91%가 신용보험으로 보호, 보험금 청구 · 대손 적음 | "At 30 June 2026, 91% of gross trade receivables (2025: 89%) were covered by trade credit insurance with Arcbridge Credit Insurance Ltd. No claims were made under the policy during the year, and impairment losses recognised on trade receivables were £0.1 million (2025: £0.1 million)." | [H8] Note 13, p. 28 | Halden이 '받을 돈'에 대한 보험이다. 우리가 Halden에게 받을 돈을 보호하지는 않음 |
| 영업현금흐름은 플러스 | "Net cash generated from operating activities was £1.9 million (2025: £4.6 million)" | [H3] Financial Review, p. 5 | £4.4m가 운전자본(공급사 결제 연장 등)에서 나온 것. 반복 가능성 낮음 |
| 경영진은 차입 연장을 합리적으로 기대 | "The directors nevertheless have a reasonable expectation that the facility will be renewed" | [H8] Note 2, p. 21 | 경영진의 기대일 뿐, 근거 합의는 없음 |
| 최대 고객 거래 20% 증가 | "whose purchases from us grew by 20% during the year." | [H1] Chief Executive's Review, p. 3 | 그 고객에게 90일 결제 허용 · 집중도 31%로 상승 |

## 3. 세 줄 요약

1. 감사인과 경영진 모두 계속기업 '중요한 불확실성'을 명시했다. 원인은 2027-03-31 만기인 차입(£8.4m)의 연장 미합의와 2026-12-31 최소 EBITDA £2.5m 약정이다(약정은 이미 한 번 위반 후 면제받음).
2. 공급사 쪽 결제조건을 60→90일, L/C→O/A로 바꿔 버티고 있으나(Creditor days 62→88), 이를 받쳐 주던 공급사 금융 한도가 £10.0m→£3.0m로 줄어 유동성이 빠듯하다(기본 시나리오 최저 여유 £0.9m, 2026년 11월). 우리 같은 한국 공급사의 60일 O/A 채권이 바로 이 압박을 받는 자리다.
3. 모회사 증자 £4.0m · 은행 면제 · 순자산 양수는 안심 요소지만 불확실성을 없애지 못했다. 자본잠식 · 구조조정은 명시되지 않음. 은행 담보가 전 자산에 걸려 있어 우리 외상 채권은 후순위다.
