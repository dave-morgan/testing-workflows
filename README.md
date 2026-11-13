# Testing Workflows

A plugin workspace containing eight portable Agent Skills for Codex and Claude Code. Each skill includes its complete supporting Markdown references, Python logging script, and Codex UI metadata.

| Skill | Execution and review |
| --- | --- |
| `goal-gated` | Reviewed plan, ordered implementation steps, independent step gates, fresh final validator |
| `goal-continuous` | Continuous whole-goal execution with independent final validation |
| `goal-observe` | Continuous execution with a periodic reporting observer |
| `goal-steer` | Continuous execution with an observer authorized to steer implementation |
| `goal-hybrid` | Reviewed planning, continuous execution, selective gates, observer steering, final validation |
| `goal-adaptive` | Observer chooses execution policies while accounting for switching costs |
| `goal-hybrid-lean` | Direct implementation, compact plan review, one risk gate, fresh final validation |
| `goal-hybrid-lean-plus` | Lean hybrid plus focused UI integration review and same-session state checks |

## Claude Code

Install from this repository's marketplace:

```text
/plugin marketplace add dave-morgan/testing-workflows
/plugin install testing-workflows@testing-workflows
```

Or load a local checkout for development:

```sh
claude --plugin-dir /absolute/path/to/testing-workflows
```

Invoke a workflow with a request, for example:

```text
/testing-workflows:goal-hybrid-lean-plus Implement the feature described in SPEC.md.
```

## Codex

The plugin manifest is `.codex-plugin/plugin.json`; it exposes the same `skills/` directory. Use that plugin root in a Codex host that supports local plugin workspaces. For direct skill installation, copy each complete `skills/goal-*/` folder into `~/.agents/skills/`, or a project's `.agents/skills/` directory. Invoke with `$goal-hybrid-lean-plus` followed by the request.

`install.ps1` provides the original Windows direct-install option: it copies selected skills into `~/.agents/skills/` and creates matching junctions in `~/.claude/skills/`. It refuses to overwrite existing installations. Use either plugin installation or direct installation to avoid duplicate skill discovery.

## Runtime and logs

Python 3 is required for the logging helper; it uses only the standard library. All workflows require independent-agent support. Observer workflows additionally require genuine concurrency and independent wakeups, and steering requires a supported message or checkpoint handoff. The skills disclose unsupported capabilities rather than simulating them. They do not keep a closed host running.

Runs default to `.agent-runs/<unique-run>/` in the target project, recording the original request, criteria, timings, decisions, per-agent events, reviews, and reports. Unavailable token or cost information stays unknown.

## Workspace maintenance

`skills/` contains the installable packages. `shared/` contains the authoring copies used by `tools/package.py`; each installed skill is self-contained. Preserve skill-specific references such as the adaptive switching policy when refreshing shared resources.

```sh
python tools/package.py
python -m unittest discover -s tests -v
python tools/validate_plugin.py
claude plugin validate .
```

`tools/check_install.py` optionally compares direct user-level installations with this workspace; it is not a plugin installation requirement. Historical benchmark outputs and audit applications are maintained separately from this plugin.

Packaging follows the [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference) and the existing Codex plugin manifest layout. The original eight workflow packages are preserved without instruction changes.
