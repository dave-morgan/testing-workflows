---
name: goal-hybrid
description: Use when the user selects workflow 5, goal-hybrid, or a fixed combined workflow drawing on continuous execution, reviewed planning, selective validation gates, reporting, and observer steering.
---

# Goal hybrid

Combine the four original approaches in one fixed execution policy: reviewed intent and risk gates, continuous implementation between gates, independent reporting with steering authority, and a fresh whole-goal final validator. This is not a controller that changes to another named workflow.

Read [protocol](references/protocol.md), [runtime](references/runtime.md), and [v2 operations](references/v2-operations.md) before starting. V2 operations owns bounded scheduling, outage recovery, role logs and final verification. No automatic dependence on other installed goal skills is needed.

1. Preserve the original request and derive stable outcome IDs. Draft a short implementation/dependency plan with observable acceptance criteria. Identify only risk-bearing gates: authorization/state invariants, durable data contracts/migrations, hard-to-reverse decisions, and integration boundaries on which later work depends. Do not gate cosmetic changes or every internal task. Gate cost must be justified by the downstream failure it prevents.
2. Launch a separate plan reviewer to check original-goal coverage, dependency order, ambiguous policies and whether each gate is necessary/testable. Revise until PASS; INCONCLUSIVE is not approval. The reviewed plan and gate map remain durable artifacts. A material change to a gated contract requires affected plan/gate re-review; ordinary implementation choices do not.
3. The coordinator launches one implementation owner to pursue the full result continuously within the approved dependencies. The worker chooses detailed order and approach rather than waiting for approvals on low-risk tasks. Tests accompany real behavior as work progresses. Unrelated unblocked work can continue while a risky boundary awaits review; dependent work cannot cross an unpassed gate.
4. At a declared risk gate, the owner checkpoints the relevant artifact. A separate gate validator inspects/runs the gate's checks. FAIL returns concrete corrections; INCONCLUSIVE obtains missing evidence. Only PASS opens dependent work. Revalidate affected earlier outcomes on regressions; reuse valid evidence instead of duplicate whole-app reviews at every gate.
5. Run separate observer passes on the independent cadence while implementation continues. They inspect actual progress, coverage, risk and apparent drift; report findings and costs. They may issue concrete goal-linked steering instructions when evidence justifies intervention. They cannot waive a gate, expand scope, or change acceptance criteria. The worker acknowledges/adjusts at a safe boundary or supplies an evidence-backed objection. Log delivery, acknowledgement and observed result; the coordinator must not equate sending with compliance.
6. If the observer or owner believes the whole request is met, follow the v2 stable-snapshot/fresh-final-validator contract. Fix final findings, repeat affected gates where their evidence was invalidated, and obtain another fresh final review. Finish only at a validated delivered snapshot or a declared stopping condition.

The best aspects are a hypothesis about fit, not a promise of higher accuracy or lower cost. Log useful defects caught versus plan/review/observer overhead so the combined policy can be evaluated against the original four.
