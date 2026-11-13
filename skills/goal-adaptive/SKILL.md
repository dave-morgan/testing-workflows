---
name: goal-adaptive
description: Use when the user selects workflow 6, goal-adaptive, or wants an independent observer to repeatedly choose between continuous, reporting, steering, and gated execution while accounting for switching costs.
---

# Goal adaptive

Start with continuous execution and let an independent reporting observer select a more suitable policy as evidence changes. Keep one orchestration run and one implementation owner. Switching policies is allowed repeatedly, but must earn its transition cost.

Read [protocol](references/protocol.md), [runtime](references/runtime.md), [v2 operations](references/v2-operations.md), and [switching policy](references/switching-policy.md). The policies are defined locally; do not invoke the original four goal skills as nested coordinators.

1. Preserve the original goal and acceptance criteria. Default current_mode=continuous, mode_epoch=1. Record the starting rationale: for a well-scoped request, continuous execution had the lowest observed overhead in the previous trial. This is a default hypothesis, not a universal performance fact.
2. Establish independent meta-observation and safe policy-delivery capabilities. The main agent coordinates; a worker pursues the whole goal. A reporting/meta-observer examines actual artifacts at the bounded independent cadence, even in continuous mode. That persistent routing overhead means this starting state is not identical to the original zero-periodic-observer continuous baseline.
3. At each pass, the observer reports progress, open risks and whether to stay or propose a change. It has authority to select an execution policy through the coordinator, but no task-level steering authority while the current mode is continuous or reporting. The coordinator may validate feasibility/authorization and request a revised recommendation; it must not silently override or invent a mode choice.
4. Evaluate a proposal with the switching-policy benefit/cost/hysteresis rule. Include remaining work, alternative of staying, transition costs, evidence strength and expected outcome. Log rejected proposals and reasons as well as accepted ones. Prefer the lightest adequate policy; never change mode just to exercise the experiment.
5. On acceptance, follow the acknowledged single-owner handoff. Preserve goal IDs, valid evidence and open findings; update the mode/epoch only after the worker receives and acknowledges the new policy. Keep the observer's own meta-routing authority across every mode. Record actual handoff costs and whether the expected effect subsequently appeared.
6. Reassess later; escalation, de-escalation and returning to an earlier mode are all valid when the evidence and remaining horizon justify their cost. Respect dwell/hysteresis rules so a noisy observation does not cause repeated context resets.
7. Either worker or observer may request final validation in any mode. Use a fresh independent validator against a frozen snapshot and the unchanged original goal. FAIL returns to work under the current policy or a separately justified new policy; a failed final review does not automatically force a mode switch. Completion is independent of which policy is active.

The evaluation must show whether switching helped, merely added overhead, or cannot be judged. No switch is a valid result when the initial policy remains suitable.
