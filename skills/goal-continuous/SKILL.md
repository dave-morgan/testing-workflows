---
name: goal-continuous
description: Use when the user selects workflow 2, goal-continuous, or continuous whole-goal execution without an ordered implementation plan and with independent completion validation.
---

# Goal continuous

Pursue the whole request continuously, then independently verify completion. Read [the shared protocol](references/protocol.md) and [the runtime adapter](references/runtime.md) before starting. Keep the full evaluation log throughout.

## Execute

1. Preserve the original request and record observable goal criteria. These define success, not an ordered execution plan. Do not decompose the task into a formal sequence of implementation steps or introduce intermediate approval gates.
2. The main implementation agent works across the full goal: implement, test, investigate, and correct as evidence warrants. It chooses the next action as it goes. Keep working across internal iterations and context handoffs; preserve a resumable checkpoint without turning it into a step plan.
3. When the implementer believes the whole goal is satisfied, checkpoint a stable snapshot and launch a **separate final validator subagent**. Give it the original request, amendments, criteria, and access to raw artifacts. Ask it to independently check every goal and integrated behavior.
4. On FAIL, record the unmet requirements, resume continuous implementation, and fix the gaps. On INCONCLUSIVE, obtain the missing access or evidence; never treat it as success. Do not convert the findings into a gated step workflow.
5. When ready again, launch a **fresh independent validator** against the current snapshot. Repeat until final PASS covers the delivered result, or an explicit stopping condition applies. A previous PASS does not cover subsequent changes.

The implementer does not decide final success alone. The validator is a completion gate, not a periodic observer. "One shot" means a continuous attempt at the whole outcome; failed validation still requires correction and another independent review.

## Record

Log implementation/test activity, decisions, pivots, completion claims, each validation round, time spent in validation and rework, failed criteria, blockers and the final snapshot. Preserve unknown usage or cost as unknown. Write the final summary and evaluation report using the shared protocol.
