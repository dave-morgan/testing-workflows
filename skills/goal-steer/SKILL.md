---
name: goal-steer
description: Use when the user selects workflow 4, goal-steer, or continuous long-running implementation with an independent observer authorized to redirect work toward the original goal.
---

# Goal steer

Implement the whole request while an independent observer measures progress and can redirect the implementer. Read [the shared protocol](references/protocol.md) and [the runtime adapter](references/runtime.md) before starting. Keep the full evaluation log throughout.

## Execute

1. Preserve the request and break it into verifiable outcomes in `goals.json`, without making them an ordered execution plan.
2. Establish the runtime's independent-observation capability gate **and** its supported steering-delivery mechanism. Record cadence and delivery behavior. Default to five-minute observations when a permitted timer exists; use the documented event-based alternative only when actually supported. Missing capabilities are blockers, not permission to silently switch modes.
3. The main agent coordinates. Launch an **implementation subagent** pursuing the full goal and **separate observer subagent passes** on the independent cadence. Reserve observer capacity. Implementation chooses its approach and order between interventions; checks do not depend on step-completion messages.
4. Each observer pass inspects raw artifacts and tests, records coverage and regressions, and checks for goal drift, repeated ineffective work, unsupported assumptions, and missed requirements. Intermediate findings remain provisional where artifacts are changing.
5. When evidence justifies redirection, the observer issues a **steering instruction** stating its ID, affected goal IDs, evidence, reason, requested priority/approach change, and the observable result to seek. The coordinator delivers it faithfully through the supported channel. Favor concrete goal corrections over subjective micromanagement.
6. The implementer acknowledges at the next safe boundary, records its response, and adjusts. It can report an evidence-backed objection or blocker rather than blindly applying an incorrect instruction. The observer resolves that objection against the original request. The coordinator records delivery, acknowledgement, pending decisions and later observed effects. No acknowledgement means delivery is unconfirmed; do not claim the implementer changed course.
7. Where live steering is unsupported, use the declared checkpoint/restart mechanism: request a checkpoint, obtain acknowledgement or host-confirmed termination, preserve state, and only then resume/replace the implementation worker with the instruction. Never leave two implementation writers active. If no such handoff works, report the capability blocker.
8. If either the implementer claims completion or the observer believes all outcomes are satisfied, checkpoint implementation and run an **observer-role final validation pass** against the stable snapshot and original goal. FAIL returns unmet requirements to implementation and observation; INCONCLUSIVE remains unverified. Finish only on final PASS for the delivered snapshot or an explicit stopping condition.

Steering can redirect priorities and approach within the existing goal. It cannot broaden scope, weaken acceptance criteria to obtain a pass, or authorize external actions. Preserve the original request through every intervention.

## Record

Log observations and cadence misses plus each intervention's trigger, instruction, delivery, acknowledgement/objection, handoff cost and observed effect. Separate the observer's intended benefit from demonstrated outcomes. Stop scheduling and settle owned children at handback. Write the final summary and evaluation report using the shared protocol.
