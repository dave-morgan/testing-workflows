# Shared execution and evaluation protocol

Read this file on every invocation. It ships inside each skill so the skill can be copied independently. Python 3 is only needed for the logger; no provider SDK or extra package is required.

## Start and preserve the goal

Treat skill invocation as authorization to use subagents for the requested work. Retain the user's existing scope and permissions. Skill instructions do not authorize publishing, spending money, changing production, or expanding the goal.

Create a unique run directory under the workspace's `.agent-runs/<timestamp>-<workflow>-<suffix>/`, unless the user specifies a location. Keep it out of commits unless requested or needed for the deliverable; do not change repository ignore rules automatically. Preserve the original request verbatim in `request.md`; record later clarifications separately as `goal_amendment` events. Assign each requested outcome a stable goal ID and observable acceptance criteria in `goals.json`. Dependencies between real outcomes remain real even without ordered steps. Do not invent an execution plan for the continuous mode.

Record the workflow, initial repository revision and dirty state (including relevant untracked files), platform, actor IDs, actual exposed model/settings, cadence, user resource limits, and runtime capabilities in an optional config JSON passed to the logger. Unknown fields stay null. Do not choose a different provider/model without existing authorization.

Initialize with the Python executable available on this machine. Paths below are symbolic; resolve SCRIPT to this skill's `scripts/runlog.py` and RUN to the run directory. Use proper shell quoting; never interpolate the request as shell code.

```text
python SCRIPT init --run-dir RUN --workflow goal-gated --request-file REQUEST --config-file CONFIG
python SCRIPT event --run-dir RUN --actor coordinator --kind decision --detail "Selected export verification" --evidence artifacts/export-test.txt --data-file DATA
python SCRIPT exec --run-dir RUN --actor implementer-1 --label export-test -- python -m unittest test_export
python SCRIPT report --run-dir RUN
```

Use the invoked workflow name for `--workflow`. `--config-file`, `--data-file`, and `--evidence` are optional. `exec` preserves the process exit status, captures combined output, and measures command duration. It does not make a test passing claim beyond the recorded exit status. Do not wrap secret-bearing commands or commands whose output must not be logged. Direct commands remain usable when interactive tools are needed; record their actual results and evidence separately. The logger is not a daemon, scheduler, or workflow engine.

## Roles and delegation

Use separate agent contexts for implementation and independent validation. The main agent can implement in gated and continuous modes. In observer modes, the main agent coordinates while an implementation subagent works concurrently with separate observer subagent passes. Only the coordinator launches children; tell children not to recursively invoke this workflow or spawn more agents. Serialize mutation through one implementation owner; validators may run tests in scratch output locations but must not repair implementation files. Avoid tests that mutate an active implementation's shared build/cache/database state; isolate them or defer them to a checkpoint.

Give each child the original request and amendments, relevant goal criteria, workspace/artifact paths, its authority, its unique actor/log name, snapshot identity, applicable limits, and the exact evidence needed. Supply raw artifacts, not just the implementer's account. A validator should independently inspect and run meaningful checks. A distinct agent can use the same model; independence does not imply a different provider.

Read [runtime.md](runtime.md) before selecting tools. Use the actual host tools and their documented scheduling and delivery behavior. Never claim that a requested observer cadence is active just because a child was launched.

## Validation contract

Each review returns a durable artifact under `artifacts/` with:

- Reviewer identity, review start/end timestamps, and reviewed snapshot identity.
- Verdict: PASS, FAIL, or INCONCLUSIVE.
- For every relevant goal ID: verified, unmet, or unverified; evidence pointers and actual checks/results.
- Concrete findings; correction requirements only when this role has steering or gate authority.

PASS requires evidence for all criteria in that review's scope. Missing access, unavailable tests, and a check that has not run are INCONCLUSIVE, never PASS. Do not treat a build alone as proof of user-visible behavior. Do not add unrelated quality requirements as new goals.

Before a final review, request a short implementation checkpoint and receive its acknowledgement. Identify a stable snapshot using the commit plus a dirty/untracked content fingerprint, or a frozen artifact copy if there is no repository. Prevent relevant implementation writes during final checks. A review only covers its recorded snapshot. Any subsequent relevant change invalidates that final pass and requires a new review. In-progress observation may use changing artifacts, but record the snapshot/range and mark racing evidence provisional. The observer cannot declare a changing snapshot finally complete.

Failed reviews feed evidence back to implementation according to the selected mode. Repeat work and verification until the original goal passes, a user limit is reached, the user stops it, or a genuine blocker prevents useful progress. Do not stop simply because an internal iteration ended. Repeated identical failures require a different hypothesis; three attempts with no new evidence or progress trigger an explicit blocker report rather than an endless loop. Keep unmet goals visible.

## Durable log and resume state

Use `events/<actor-id>.jsonl` with exactly one writer per actor ID. Every newly spawned agent gets a unique actor ID. The coordinator owns `run.json`, `goals.json`, `checkpoint.json`, `report.json`, and `SUMMARY.md`. Reviews and artifacts use unique names. Per-actor streams form one logical append-only run log. Do not have multiple agents append to a shared file. Corrections are new events with `supersedes_event_id`; never rewrite history. Event ordering by wall-clock timestamp is approximate across machines; use explicit related event IDs for causality.

Log meaningful starts/ends, decisions, notes, tests, findings, rework, waiting, interruptions, cadence misses, and goal changes. Use these common event kinds so runs are comparable:

`run_started`, `run_resumed`, `implementation_started`, `implementation_checkpoint`, `implementation_finished`, `decision`, `note`, `test_result`, `review_started`, `review_finished`, `observation_due`, `observation_finished`, `cadence_missed`, `steering_issued`, `steering_acknowledged`, `steering_effect`, `goal_status`, `goal_amendment`, `waiting_started`, `waiting_finished`, `blocked`, `run_finished`.

Each event includes its real timestamp, actor, kind, detail, evidence paths, and optional structured `data`. In `data`, record relevant `goal_ids`, `revision`, `verdict`, `reason`, `span_id`, `related_event_id`, planned and actual observation times, and measured durations when known. Start/end pairs share a span ID. Decision notes explain the choice and reason in plain language; do not log private chain-of-thought. Use `exec` for timed commands when appropriate. Record token/cost information only from actual host usage data, with its unit, scope and source. Never infer missing metrics or emit invented timing entries.

Checkpoint after material progress and before a context handoff. `checkpoint.json` names the exact goal version, current snapshot, actor/task handles, last processed event IDs, verified/unverified outcomes, open findings, next observer deadline, any in-flight commands or steering, and the next action. Outcome verification is separate from implementer completion claims.

On resume, read the request, amendments, checkpoint, latest actor events and reports. Reconcile the actual workspace and child status before starting another writer or implementer. Revalidate affected goals after changes. Record the interruption gap and a `run_resumed` event; do not count downtime as active effort. A skill does not survive process shutdown on its own. Resume the same run when it is the same experiment; use a new run for a different workflow or experiment, linking the prior run in config.

## Final evaluation record

Once agents have checkpointed, append `run_finished` with `data.outcome` equal to `completed`, `blocked`, `stopped`, or `resource_limit`. `completed` requires a final PASS for the delivered snapshot. Generate `report.json`, then write `SUMMARY.md` linking the final evidence and describing remaining work honestly.

The summary includes goal coverage, final verdict/snapshot, elapsed wall time, measured implementation/review/wait intervals where available, validation failures, rework cycles, observation lateness/missed checks, steering interventions and effects, key decisions, and log completeness gaps. Command time can overlap other work; never present its sum as wall time. Unknown active effort stays unknown. Report tokens/costs only when captured. For steering, cite the observed result and avoid claiming causal benefit without evidence.

To compare workflows, record the same task, starting revision/dirty state, acceptance criteria, host capabilities, and agent configuration. Note differences and warm-cache/order effects. A single run supports observations, not a claim that one workflow is universally better. Finish with the result and links to the run directory, summary, and validation artifact.
