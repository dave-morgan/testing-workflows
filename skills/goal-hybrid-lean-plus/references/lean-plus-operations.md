# Lean Plus execution operations

This reference supplies operations for goal-hybrid-lean-plus. The workflow deliberately removes independent periodic supervision; do not recreate it through timers, polling, extra agents or inherited hybrid scheduling rules.

## Runtime and reviewer briefs

Use native same-provider subagents where the host permits: Codex `spawn_agent`, Claude Code `Agent` (older hosts: `Task`). Prefer a clean context with a concise brief. In T3 follow host routing: discover capabilities once before any `delegate_task`; use it for another provider, explicit model/settings, separate checkout or background work. Follow returned `next`, do not poll, and start a new delegate for each new review. Respect user model/settings; do not silently substitute. Missing independent-agent capability prevents validation, not permission to self-approve. Never create a top-level thread to simulate a reviewer.

Every reviewer gets: exact workspace/run paths, original request/amendments, relevant outcome IDs, role and review scope, source snapshot or manifest, evidence pointers, and unique actor/log/artifact paths. Reviewers do not implement, orchestrate, spawn children or schedule work. They may run checks with isolated test data and write only their own evidence. Briefs link relevant files rather than copying full implementation transcripts or prior reports. Their verdict is PASS, FAIL or INCONCLUSIVE, with concrete evidence, accepted user amendments if any, and useful findings distinguished from confirmations. They cannot redefine acceptance. Plan/gate/UI reviewers cannot substitute for the fresh final validator.

The main agent is the sole application writer and canonical ledger writer. Hold affected files stable during gate checks and the complete deliverable stable during final checks. A manifest includes relevant tracked and untracked source, lockfiles, configuration, migrations, tests and documentation, excluding generated/dependency/runtime-data directories. Reviewers check the delivered identity at start and end; relevant mutation makes the result inconclusive. Do not confuse a commit ID with dirty/untracked source identity. Run tests against isolated data to avoid changing the candidate's source or a live user's data.

## Compact evaluation record

Use the bundled standard-library Python logger. Keep request/config staging files outside the not-yet-existing run directory, then initialize a unique run:

```text
python <skill>/scripts/runlog.py init --run-dir .agent-runs/<id> --workflow goal-hybrid-lean-plus --actor implementer-1 --request-file <request.md> --config-file <config.json>
```

Copy the request exactly. Configuration records actual platform/model/settings, workflow version, limits if supplied, and the selected risk boundary. The request, concise plan/criteria/policies and a single mutable `EVIDENCE.md` index are canonical; use file links instead of repeated full-goal coverage essays. The implementer updates the index at meaningful changes, not every read. Record decisions and rationale, failures, discarded approaches, test results, reviewer findings and corrections. Preserve original events; do not rewrite history to hide failed attempts.

Each actor writes its own `events/<actor>.jsonl`, with exactly one writer per actor. The main agent writes its own observations about other roles without impersonating them. Record reviewer handles/native session IDs where exposed. Record phase/review/wait start/end events with matching span IDs and actual UTC timestamps; record gaps and open spans honestly. A normal note uses:

```text
python <skill>/scripts/runlog.py event --run-dir <run> --actor <actor> --kind decision --detail <what-and-why> --evidence <artifact>
```

Use `--data-file <json>` for structured fields such as span identity, snapshot, finding severity, estimated versus measured costs, and role/session mappings. Time major build/test/verification commands and preserve full output without flooding the transcript:

```text
python <skill>/scripts/runlog.py exec --run-dir <run> --actor <actor> --label <check> -- <executable> <arguments>
```

Commands run without a shell; on Windows use real executable paths or invoke a shell explicitly when required. Inspect failures and relevant output, not only the wrapper's returned artifact path. The logger records evidence; it does not enforce gates or schedule agents.

Capture actual exposed provider counters per unique native session with scope and timestamps. Preserve input, cached input and output separately; reasoning output is a subset where applicable. Count the latest cumulative counters once per session, not on every checkpoint. If unavailable, record null and the role/session handles so a later audit can recover them. Never guess tokens from text length or infer dollar cost. Sum of overlapping command/reviewer durations is not elapsed time; active effort is unknown unless measured. Preparation/audit usage is outside the implementation trial.

## Interruptions, resume and completion

On visible quota/rate-limit failure, log the actual error when able, checkpoint and settle any owned reviewers; do not spin retries, switch providers/models or start replacement workers. No observation schedule exists to rearm. A failure before the agent can log it remains a gap to reconcile from host history on healthy re-entry. Resume the same run explicitly, recording the interruption and reconciling prior handles/evidence; do not claim uninterrupted execution or erase failures. An unavailable required reviewer leaves its scope unverified.

On final PASS, confirm the delivered snapshot still matches and no owned child remains active. Append one terminal `run_finished` event with structured outcome, final-review evidence and snapshot. Generate `report.json` using `runlog.py report --run-dir <run>` after writers settle, and write a short `SUMMARY.md`: criteria coverage, remaining limits, useful findings by role, measured versus unavailable timing/usage, interruptions and extra reviews with justification. A resumed stopped segment links its previous terminal event. No completion claim is valid without fresh independent final PASS at the delivered snapshot.

## Focused UI review and state-transition evidence

Use a unique ui-reviewer actor, with measured start/end, source identity, useful findings and test artifacts. Hold the reviewed UI stable; the main implementer remains the sole source writer. The reviewer tests at an integrated UI checkpoint before final validation. It is a bounded checkpoint, not independent periodic observation. Retain an explicit matrix of relevant user/role/job/view transitions and state reset/persistence expectations; both the UI reviewer and fresh final validator independently exercise the matrix with deliberately changed state in one session. Missing evidence remains unverified. A UI finding is corrected by the implementer and verified by targeted regressions plus the independent final review; material backend-contract changes still invalidate affected risk-gate evidence. Do not create an extra coordinator, timer or recurring observer.
