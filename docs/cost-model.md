# Illustrative unit economics and capacity model

All values are **hypothetical assumptions**, not vendor quotes, measured savings or actual Azure pricing. Replace them with current contracted rates and measured token usage before any business case.

## Inputs
- Monthly inbound inquiries: 50,000
- FAQ eligible share: 55% → 27,500
- Successful automation within eligible share: 70% → 19,250 automated resolutions
- Baseline fully loaded manual handling cost: $4.00 / inquiry
- Assumed variable model + retrieval cost: $0.035 / attempted eligible inquiry
- Assumed fixed monthly infrastructure, observability and operations: $2,500
- Assumed monthly review/escalation overhead: $1,000

## Illustrative arithmetic
- Avoided manual handling value: 19,250 × $4.00 = **$77,000/month**
- Variable inference/retrieval: 27,500 × $0.035 = **$962.50/month**
- Total assumed monthly platform + review cost: $962.50 + $2,500 + $1,000 = **$4,462.50/month**
- Hypothetical gross benefit less these costs: **$72,537.50/month**

**This is not an ROI claim.** It omits implementation costs, change management, security, licenses, additional manual review, customer behavior, accuracy penalties and demand elasticity. Avoided handling value may not convert to realized savings unless staffing or capacity changes.

## Capacity assumptions
50,000/month ≈ 1,667/day averaged over 30 days. With 10× peak over the average 24-hour rate: ~0.19 requests/second. This is a simplistic planning figure; real peaks require measured arrival distributions, concurrency and service-time modeling.

## Sensitivity to containment
| Eligible share | Resolution success | Automated resolutions/month |
|---|---|---:|
| 40% | 50% | 10,000 |
| 55% | 70% | 19,250 |
| 65% | 80% | 26,000 |

## Metrics to collect
Prompt/completion tokens, per-deployment inference prices, retrieval calls, retries, human review minutes, end-to-end latency percentiles, accuracy and containment by intent, incident cost, infrastructure utilization.
