# Design acceptance pilot | AI with Zaian
Date: 9 November 2026
Content ID: AZ 2026 1109 02
Decision: **HOLD — recurring content production DISABLED**

## Scope tested
Five actual Instagram carousel PNGs rendered 1080 × 1350, with a 360-pixel contact sheet and bilingual brand review. Pilot theme: AI agent delegation, evidence and approval. No people, humanoid figures or RTA logo. Uses the locked navy, teal, lime, gold and white palette. Subject-led editorial diagrams replace generic AI imagery.

## Executed tests and results
| Test | Result | Evidence |
| --- | --- | --- |
| Exported image dimensions | PASS | Five PNGs generated at 1080 × 1350 |
| 360-pixel preview created | PASS | Mobile Contact Sheet.png |
| Text bounding check | PASS | Automated Checks.json reports zero out-of-bounds boxes |
| Contrast | PASS (tested combinations) | White/navy 19.24:1, teal/navy 9.20:1, lime/navy 15.55:1, muted/navy 11.62:1 |
| Arabic layout | PARTIAL | RAQM enabled; actual export was inspected and a broken mixed-script heading repaired |
| Official Dubai Font | **FAIL/BLOCKED** | Not installed in runtime; pilot used Noto Sans Arabic and DejaVu Sans, clearly marked fallback |
| Independent reviewer | NOT TESTED | Only producing assistant reviewed; cannot count as independent QA |
| Physical-device and Instagram in-app safe area | NOT TESTED | No actual app preview recorded |
| Platform audience performance | NOT TESTED | No publication or analytics |
| User approval to publish | NOT GIVEN | Content is test-only |

## Defect register
- D-001 (Major): mixed Arabic/English heading showed missing glyph squares. Fixed by rewriting headings in Arabic and rerendering.
- D-002 (Major, OPEN): official Dubai Font not installed or verified on actual output. Blocks brand acceptance.
- D-003 (Major, OPEN): independent linguistic and visual reviewer has not inspected rendered files.
- D-004 (Major, OPEN): in-app Instagram layout test on a real device not completed.
- D-005 (Critical release prerequisite, OPEN): explicit final owner approval not yet granted.

## Gate state
- Gate A Editorial: PARTIAL (factual claims reviewed; independent reviewer pending).
- Gate B Visual: PARTIAL (asset generation, automated geometric checks and 360 px preview done; Dubai typeface and independent visual QA missing).
- Gate C Final export and release: **BLOCKED**.

## Next acceptance run
1. Install a legitimately acquired Dubai font in renderer; record font metadata but DO NOT commit font binaries to repository.
2. Regenerate all slides and inspect typography at actual size and 360 px; run contrast/bounds validations.
3. Obtain independent reviewer verdict, close major/critical issues, record signed QA result.
4. Inspect Instagram in-app preview and crops without publishing.
5. Present complete release package for explicit owner approval.
6. Only then enable recurring production. Publishing remains separately permissioned.

**No person or process may declare PASS for a check that was not executed.**