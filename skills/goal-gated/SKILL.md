---
name: goal-gated
description: Use when the user selects workflow 1, goal-gated, or a long-running multi-goal task requiring independent plan approval and validation gates between implementation steps.
---

# Goal gated

Execute a reviewed plan one verified step at a time. Read [the shared protocol](references/protocol.md) and [the runtime adapter](references/runtime.md) before starting. Keep the full evaluation log throughout.

## Execute

1. Preserve the original request and derive goal IDs and acceptance criteria. Break the work into ordered steps with dependencies and observable completion conditions in `plan.md`. The number of steps follows the task; it is not fixed at three.
2. Launch a **plan reviewer subagent**. Ask it to inspect the original request, proposed steps, coverage, order, dependencies and verification feasibility. It returns PASS, FAIL, or INCONCLUSIVE plus goal coverage and concrete gaps. Revise and submit to another independent review until PASS. Do not implement before plan approval.
3. For the next approved step, the main implementation agent builds it and runs meaningful tests. Record actual results and the implementation snapshot.
4. Launch a separate **step validator subagent** to inspect the change and independently verify the step's conditions and effects on already completed outcomes. It may require corrections but must not edit implementation files.
5. On FAIL, fix the findings, rerun relevant tests, and launch a fresh validation pass. INCONCLUSIVE stays unverified and requires resolving the evidence gap. Advance only on PASS. These are the repeating build, test, independent-validation phases.
6. Repeat for every step. If new evidence requires changing the plan, preserve prior versions, log the reason, and obtain plan review for the affected dependencies and coverage before executing changed steps. Reopen prior steps when evidence shows regressions.
7. After all steps pass, checkpoint implementation and launch a **fresh final validator subagent** distinct from the implementer, plan reviewer, and step validators. Give it the original request, amendments and final artifacts. It checks every goal and integration across steps, not just the checklist.
8. If final validation finds gaps, reopen affected work, repeat relevant build/test/step validation, then launch another fresh final validator. Finish only on final PASS at the delivered snapshot, or report the explicit unfinished status under the shared stopping rules.

## Record

Log plan revisions and review times, each step's build/test/review cycles, waiting at gates, reopened steps, validation failures, final integration findings, decisions and blockers. Distinguish implementer completion claims from independently validated steps. Write the final summary and evaluation report using the shared protocol.
