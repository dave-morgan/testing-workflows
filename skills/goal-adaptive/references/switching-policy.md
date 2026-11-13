# Adaptive execution policies and switching costs

## The four policies

The same independent meta-observer continues evaluating suitability in every mode. Its routing reports are distinct from task instructions. It never implements or approves its own edits.

- **continuous:** the worker chooses its next action across the whole goal; no ordered implementation plan or step gates. Meta-observation is a lightweight sample of changed artifacts, progress/risk and policy fit. It does not perform an exhaustive checklist audit every pass or deliver task-level fixes.
- **observe:** implementation stays continuous and autonomous. The observer performs a formal coverage/evidence audit across the outcome checklist, revises verified/unverified/regressed statuses, and records a progress report. It may recommend a mode switch but cannot prescribe implementation actions. This is higher reporting/evidence effort than continuous's routing sample, not an extra duplicate observer hierarchy.
- **steer:** implementation stays continuous; the observer also sends concrete evidence-backed priorities or approach corrections tied to the existing goal. Require delivery and acknowledgement/objection; report actual effects. It cannot create approvals, waive external authorization, or impose step gates without switching to gated.
- **gated:** independently review a plan for the remaining affected work; define step completion criteria/dependencies; execute build/test/separate-validator gates in order. Reuse already valid work and evidence rather than restarting the project. A fresh reviewer per re-check is required where the host requires it. The meta-observer continues policy-fit reporting but cannot waive gates. De-escalation does not erase failed invariants or prior required authorizations: equivalent evidence must resolve them before dependent work resumes.

All policies require tests and fresh final whole-goal validation. Runtime permissions, original scope, one writer and verified completion are invariant across switching. There is no need to create another top-level thread for a switch.

## Typical reasons to change

- Move toward observe when progress is plausible but coverage/evidence is unclear and reporting alone addresses the uncertainty.
- Move toward steer when there is confirmed goal drift, repeated ineffective work, ignored requirements or a correctable approach problem requiring direction.
- Move toward gated when dependent contracts or invariants repeatedly fail, a risky integration/migration needs sequential proof, or moving ahead would propagate a demonstrated defect. The gate does not itself authorize an otherwise forbidden action.
- Return toward continuous when risk is resolved, progress/evidence is stable, supervision is not discovering useful new issues, and review cost consumes the remaining benefit.
- Use reporting instead of steering when evidence visibility remains valuable but direct corrections are no longer needed. Switch directly between any policies if justified; no mandatory ladder or minimum number of switches.

## Proposal and cost test

Write a proposal artifact and mode_switch_proposed event containing:

`proposal_id`, `from_mode`, `to_mode`, `from_epoch`, `goal_ids`, `snapshot`, `evidence`, `trigger`, `stay_alternative`, `remaining_work`, `expected_benefit`, `transition_cost_estimate`, `confidence`, `decision` and `reason`.

Estimate checkpoint/acknowledgement delay, context rereading, plan/review setup, disruption or lost parallel work, additional inference/tool calls, and later return-switch cost if likely. Reusing the existing worker reduces rereading, but a policy change is not free. Account for the ongoing observer cost in every mode, plus the extra reviews the new mode introduces.

Compare expected avoided rework/risk or verification benefit over the *remaining* work with those costs. Safety/correctness losses and minutes/tokens are different units: do not silently turn them into one numerical utility. If quantities are unavailable, use explicitly qualitative low/medium/high assessments with evidence and state that a numeric break-even is unknown. Estimates are not measured savings. When a discretionary change has no clearly positive expected value, stay and reassess.

Near completion, a costly plan/reset needs stronger justification; an eight-minute handoff to save one minute is rejected even if the proposed policy is generally good. A confirmed severe authorization/data-integrity defect can justify immediate affected-work suspension and escalation despite time cost, without granting new permissions.

## Hysteresis

Default: require two consecutive independent observations supporting a discretionary switch and at least one configured observation interval in the current mode before another discretionary change. De-escalation requires two healthy observations with the original trigger resolved. Record evidence IDs and dwell time. A single confirmed critical defect or explicit user directive can bypass these defaults; record the exception and keep affected work stopped as appropriate. Do not wait for a second observation before preventing a demonstrated dangerous action.

Do not rearm a repeating timer to manufacture the required observations during an outage. User cadence/limits take precedence. If the remaining task finishes before a second observation is warranted, request final validation rather than delay solely to exercise switching.

## Commit a mode change

1. Observer selects a feasible proposal, with evidence/cost basis. Coordinator confirms host capabilities and existing authorization; if unavailable, return an INCONCLUSIVE/blocked proposal rather than pretending to switch.
2. Record mode_switch_accepted and policy_handoff_started with a span ID. Request the existing owner to checkpoint at the next safe boundary. For a severe current failure, suspend the affected operations immediately through supported control.
3. Deliver the new policy, proposal/epoch, retained outcomes/evidence, open findings and any new plan/gates. This message is a policy handoff; while leaving reporting/continuous it must not smuggle in task-level steering before the new authority is acknowledged.
4. Require the existing worker to acknowledge the new mode and epoch. On acknowledgement, the coordinator alone updates current_mode, increments mode_epoch and appends mode_changed/mode-history.jsonl; the new mode starts here. Ignore stale instructions from older epochs. If handoff fails, remain in a recorded pending/blocked state; do not record a successful switch.
5. Prefer retaining the worker/context. If replacement is necessary, obtain checkpoint and host-confirmed termination of the old owner before starting the new writer. Unknown status is not termination. The replacement receives the existing run state, not a clean slate.
6. End the handoff span; record measured transition duration and actual token deltas when exposed, otherwise null with reason. Later append mode_effect_observed with changes in progress, errors, rework and review cost. Beneficial-looking outcomes alone do not establish causal savings.

`checkpoint.json` includes current mode, epoch, observer evidence streaks, last switch time, accumulated transition costs, rejected/pending proposal, gate state, owner handle, snapshot, observation deadline/one-shot ID and final-review status. One coordinator writes mode-history.jsonl. Preserve old decisions append-only.

## Final report

Report time/usage by mode and by role when measured, switch count and reasons, rejected proposals, transition overhead, retained/discarded work, observed effects, and uncertainty. Keep final validator accuracy separate from routing quality. No required switch count, no self-awarded savings, and no final PASS carried forward after relevant changes.
