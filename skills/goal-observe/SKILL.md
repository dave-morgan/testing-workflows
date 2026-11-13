---
name: goal-observe
description: Use when the user selects workflow 3, goal-observe, or continuous long-running implementation with an independent reporting observer that has no steering authority.
---

# Goal observe

Implement the whole request while an independent observer measures progress without directing implementation. Read [the shared protocol](references/protocol.md) and [the runtime adapter](references/runtime.md) before starting. Keep the full evaluation log throughout.

## Execute

1. Preserve the request and break it into verifiable outcomes in `goals.json`. This is a coverage checklist, not an execution sequence. Do not require executing or completing its items in order.
2. Establish the runtime's independent-observation capability gate. Record cadence and wakeup mechanism. Default to five-minute observations when a permitted timer exists; use the documented event-based alternative only when actually supported. If the gate fails, log and report the blocker rather than silently changing workflows.
3. The main agent coordinates. Launch an **implementation subagent** to work continuously on the full request, with authority to choose its own order and approach. Launch **separate observer subagent passes** on the independent cadence while implementation continues. Reserve capacity for the observer; do not consume all agent slots with implementation workers.
4. At each observation, inspect actual artifacts and tests against all outcome criteria. Record verified, unmet and unverified items, evidence, provisional checks, regressions and timing. Previous verified items can become unmet after changes. The coordinator updates the canonical checklist from evidence, never from completion claims alone.
5. The observer may report drift and missing outcomes, but has **no authority to reprioritize work, prescribe a fix, send instructions to the implementer, or change its plan**. Keep its findings in the observation record and user progress reports. The coordinator must not forward them as disguised implementation directions. Intermediate observations are not step gates.
6. If the implementer claims completion **or** an observation finds every outcome apparently satisfied, request and acknowledge an implementation checkpoint, then run an **observer-role final validation pass** against the stable snapshot and original goal.
7. Final FAIL may return specific unmet requirements to implementation; this final correction loop is allowed even though periodic steering is not. INCONCLUSIVE requires resolving the evidence gap. Resume implementation and cadence, then repeat final verification when triggered again. Finish only on final PASS for the delivered snapshot or an explicit stopping condition.

## Record

Log planned/actual observations, cadence misses, observed coverage and regressions, implementer claims, final-review triggers, verification failures, decisions and blockers. Do not claim observer feedback caused a correction when the implementer never received it. Stop scheduling and settle owned children at handback. Write the final summary and evaluation report using the shared protocol.
