---
name: goal-hybrid-lean
description: Use when the user selects goal-hybrid-lean, workflow 7, or the reduced-overhead hybrid experiment for a long-running goal.
---

# Goal hybrid lean

The main agent implements the full request directly. Separate agents review the plan, one coalesced risk boundary, and the final result. There is no separate coordinator or implementation worker, periodic observer, observation schedule, or automatic workflow switching. Four agent contexts are the normal topology; justified re-reviews may add contexts. This is an efficiency hypothesis, not a promise of equal quality or savings.

Read [lean operations](references/lean-operations.md) for logging, review briefs, runtime adapters and interruption handling. This skill is self-contained; do not load another goal skill or its observer protocols.

1. Preserve the original request and accepted amendments. Derive stable outcome IDs and observable acceptance criteria. Write a short dependency plan and explicit policies for consequential ambiguities. Select one coalesced gate for authorization/state, durable data, or integration contracts that later work will depend on. Explain the risk it prevents. For a task without such a boundary, the plan reviewer must confirm why no gate is justified; cosmetic tasks do not create gates.
2. Launch an independent plan reviewer with the original request, plan, policies and proposed gate. Ask for missing coverage, policy errors and unnecessary gates, not a second implementation plan. Resolve blocking findings and obtain PASS before implementation. Plan approval is not runtime verification.
3. Implement continuously as the main agent. Choose the detailed order, test real behavior, and keep one compact evidence ledger. Work on independent areas may proceed while a gate awaits review; dependent integration must wait. Use targeted checks during iteration, then a complete candidate verification. Do not repeatedly run unchanged full suites just to produce progress reports.
4. At the selected boundary, checkpoint its source and launch a separate gate reviewer to inspect contracts and run focused adversarial checks. PASS opens dependent work; FAIL requires correction, and INCONCLUSIVE requires missing evidence. Preserve useful executable checks. Later material changes invalidate affected evidence and require focused re-review. Additional reviews require a logged concrete risk, changed contract or unresolved failure requiring independent diagnosis, not elapsed time, cosmetic changes or ordinary progress.
5. When the result appears complete, run the candidate checks, finish setup/limitations documentation, freeze the delivered source snapshot and launch a fresh final validator, distinct from the implementer and earlier reviewers. Give it the original criteria and evidence index, not an instruction to ratify completion. It must independently exercise the integrated result, including relevant permissions, state/date boundaries, persistence, primary user journeys and required UX/accessibility. Automated PASS alone is not whole-goal approval. Fix FAIL findings and invalidate affected prior evidence; after relevant changes obtain another fresh final review of the corrected snapshot. INCONCLUSIVE stays unverified.

Do not create a separate observer to verify routine corrections. The implementer runs targeted regression checks; gate re-review is needed only when gate evidence is affected. Final verification remains independent and comprehensive. Never omit a required check or weaken acceptance criteria to meet an efficiency target.
