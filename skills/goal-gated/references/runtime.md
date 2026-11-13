# Platform and observer runtime adapter

The SKILL.md frontmatter uses only the portable Agent Skills name/description fields. Codex-specific UI metadata is optional; Claude can ignore `agents/openai.yaml`.

## Tool selection

- **Codex native:** when exposed, use `spawn_agent` for a separate context, `send_message` for supported in-flight messages, and the host's completion/wait mechanism. A validator should get a clean brief with the original criteria rather than an implementer-biased transcript where the host permits it. Do not hardcode a model or reasoning setting.
- **Claude Code native:** use the available `Agent` tool (older hosts may call it `Task`) for separate contexts. Sequential reviews can use foreground calls. Observer modes need actual concurrent child execution plus a host-supported way to invoke an observer before implementation completes. Do not assume ordinary subagents can receive live messages. A checkpoint/restart handoff can support steering when live delivery is absent.
- **T3 Code:** host instructions take precedence. Discover capabilities once before the first `delegate_task`. Use native same-provider agents when allowed; use `delegate_task` for background agents, another provider, requested settings, separate checkout, or explicit delegate requests. Put settings in `target.options`. Follow a delegate's returned `next`; do not poll running delegates or invent watchers/timers. A new delegated review/re-check is a new `delegate_task`. Stop unneeded delegates with `task_cancel`. Never create top-level threads as a substitute for children. If required observer wakeups conflict with host rules or are not exposed, observer mode is unavailable in that host.

A provider being installed does not establish that this session exposes its agent tools. Check the available tool surface. If independent agents are unavailable, report that the selected workflow cannot start; do not substitute self-review. Do not silently switch providers.

## Independent observation capability gate

Before starting mode 3 or 4, establish all of the following:

1. Implementation can continue while the coordinator or observer runs.
2. A permitted host mechanism produces observation opportunities independently of goal/step completion claims.
3. The observer can inspect actual current artifacts and return a separate report.
4. For mode 4, steering can reach the implementer through supported live messages or an acknowledged checkpoint/restart mechanism. Replacing a worker requires stopping the old worker before the replacement mutates files.

Prefer an already-available runtime timer, default every five minutes. Record actual deadlines and check start times, not just the configured interval. If only tool/event checkpoints are supported, an every-ten-implementation-tool-actions cadence is acceptable only if that host actually exposes those events and can invoke the observer while work continues. Record `cadence_basis=tool_events`, not a timed cadence. User-specified cadence takes precedence. Neither option depends on a step being complete.

Do not install hooks, daemons, external schedules, or paid services just to satisfy the gate without existing authorization. Do not use fabricated heartbeat messages, completion-triggered reviews, a blocking child wait, or an implementer's remembered self-check as independent observation. If no permitted mechanism works, log `blocked` with the missing capability and report it. Do not silently fall back to gated or continuous mode. Cadence may be approximate because of tool/runtime latency; log lateness and misses explicitly.

Observer passes are separate subagent invocations, or a genuinely persistent observer when the host supports it. A fresh invocation receives previous observation reports and current goals so the logical observer retains continuity. The final pass is an observer-role subagent pass, with fresh current evidence and implementation checkpointed. The coordinator must not impersonate that role.

## Scheduling lifecycle

Record `observation_due` when the permitted wakeup arrives, dispatch the observer, and record `observation_finished` on return. Do not start overlapping passes for the same observer; coalesce delayed deadlines and record missed/later checks. Keep implementation active during normal observation. Only final verification, a required snapshot-safe check, a user stop/limit, or a mode-4 steering handoff requires an implementation checkpoint. On completion or stop, cancel observer scheduling and settle/cancel owned children using host tools. Do not leave a second writer running after handback.

## Installation and invocation

Install each entire skill directory, including `references/` and `scripts/`:

- Codex personal: `~/.agents/skills/<name>/`; project: `.agents/skills/<name>/`.
- Claude Code personal: `~/.claude/skills/<name>/`; project: `.claude/skills/<name>/`.

On Windows a Claude directory junction can target the canonical Codex skill directory. On other systems use a supported directory symlink or copy the whole folder. Do not overwrite unrelated existing skill folders. Start a fresh session if the current host has not refreshed skill discovery.

Codex: `$goal-gated <request>` (or select the skill in the UI). Claude Code: `/goal-gated <request>`. Substitute `goal-continuous`, `goal-observe`, or `goal-steer` as appropriate. Explicitly supply a run directory to resume when several runs exist.

Sources checked during authoring:

- https://developers.openai.com/codex/skills/
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
