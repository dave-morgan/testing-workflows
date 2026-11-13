"""Portable, standard-library event logger. Each actor has one writer."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid


WORKFLOWS = ('goal-gated', 'goal-continuous', 'goal-observe', 'goal-steer', 'goal-hybrid', 'goal-adaptive')


def utc():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_run(path):
    return json.loads((path / 'run.json').read_text(encoding='utf-8'))


def append_event(run_dir, actor, kind, detail, evidence=(), data=None):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', actor):
        raise ValueError('actor must be a simple identifier, at most 80 characters')
    run = load_run(run_dir)
    event = dict(schema_version=1, event_id=uuid.uuid4().hex,
                 run_id=run['run_id'], timestamp=utc(), actor=actor,
                 kind=kind, detail=detail, evidence=list(evidence), data=data or {})
    with (run_dir / 'events' / (actor + '.jsonl')).open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + '\n')
    return event


def initialize(args):
    request = args.request_file.read_bytes()
    config = json.loads(args.config_file.read_text(encoding='utf-8')) if args.config_file else {}
    if not isinstance(config, dict):
        raise ValueError('config must be a JSON object')
    args.run_dir.mkdir(parents=True, exist_ok=False)
    (args.run_dir / 'events').mkdir()
    (args.run_dir / 'artifacts').mkdir()
    (args.run_dir / 'request.md').write_bytes(request)
    run = dict(schema_version=1, run_id=uuid.uuid4().hex, workflow=args.workflow,
               started_at=utc(), workspace=str(Path.cwd().resolve()), config=config)
    write_json(args.run_dir / 'run.json', run)
    append_event(args.run_dir, 'coordinator', 'run_started', 'Run initialized')
    print(str(args.run_dir.resolve()))
    return 0


def record(args):
    data = json.loads(args.data_file.read_text(encoding='utf-8')) if args.data_file else {}
    if not isinstance(data, dict):
        raise ValueError('event data must be a JSON object')
    event = append_event(args.run_dir, args.actor, args.kind, args.detail, args.evidence, data)
    print(json.dumps(event, ensure_ascii=False))
    return 0


def execute(args):
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise ValueError('exec requires a command after --')
    span_id = uuid.uuid4().hex
    relative = 'artifacts/' + span_id + '.txt'
    append_event(args.run_dir, args.actor, 'command_started', args.label,
                 [relative], dict(span_id=span_id, command=command, cwd=str(Path.cwd())))
    started = time.monotonic()
    try:
        with (args.run_dir / relative).open('wb') as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, shell=False)
        code = result.returncode
    except OSError as error:
        (args.run_dir / relative).write_text(str(error), encoding='utf-8')
        code = 127
    except KeyboardInterrupt:
        append_event(args.run_dir, args.actor, 'command_interrupted', args.label, [relative],
                     dict(span_id=span_id, duration_seconds=time.monotonic() - started))
        raise
    append_event(args.run_dir, args.actor, 'command_finished', args.label, [relative],
                 dict(span_id=span_id, exit_code=code, duration_seconds=time.monotonic() - started))
    print(json.dumps(dict(exit_code=code, evidence=str((args.run_dir / relative).resolve()))))
    return code


def report(args):
    run = load_run(args.run_dir)
    events = []
    for path in sorted((args.run_dir / 'events').glob('*.jsonl')):
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f'{path}:{number}: invalid event; preserve and repair in a separate artifact') from error
            if event['run_id'] != run['run_id']:
                raise ValueError(f'{path}:{number}: event belongs to another run')
            events.append(event)
    events.sort(key=lambda event: (event['timestamp'], event['event_id']))
    terminal = [event for event in events if event['kind'] == 'run_finished']
    endpoint = terminal[-1]['timestamp'] if terminal else (events[-1]['timestamp'] if events else run['started_at'])
    elapsed = (datetime.fromisoformat(endpoint) - datetime.fromisoformat(run['started_at'])).total_seconds()
    starts = {event['data']['span_id'] for event in events if event['kind'] == 'command_started'}
    ends = {event['data']['span_id'] for event in events if event['kind'] in ('command_finished', 'command_interrupted')}
    result = dict(schema_version=1, run_id=run['run_id'], workflow=run['workflow'],
                  report_generated_at=utc(), elapsed_to_last_event_seconds=elapsed,
                  outcome=terminal[-1]['data'].get('outcome') if terminal else None,
                  events_by_kind=dict(Counter(event['kind'] for event in events)),
                  command_duration_sum_seconds=sum(event['data']['duration_seconds'] for event in events if event['kind'] == 'command_finished'),
                  open_command_spans=sorted(starts - ends), token_usage=None, cost=None,
                  caveats=['Command durations may overlap; their sum is not wall time.',
                           'Elapsed time includes waiting and inactive session gaps.',
                           'Token usage and cost are unknown; inspect explicit usage events if supplied.'])
    write_json(args.run_dir / 'report.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main():
    # Windows pipe defaults may be a legacy code page; the log CLI is UTF-8.
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='action', required=True)
    init = subs.add_parser('init', help='Create a new run directory; never overwrite a run')
    init.add_argument('--run-dir', required=True, type=Path)
    init.add_argument('--workflow', choices=WORKFLOWS, required=True)
    init.add_argument('--request-file', type=Path, required=True)
    init.add_argument('--config-file', type=Path)
    init.set_defaults(func=initialize)
    event = subs.add_parser('event', help='Append one event; exactly one writer per actor')
    event.add_argument('--run-dir', required=True, type=Path)
    event.add_argument('--actor', required=True)
    event.add_argument('--kind', required=True)
    event.add_argument('--detail', required=True)
    event.add_argument('--evidence', action='append', default=[])
    event.add_argument('--data-file', type=Path)
    event.set_defaults(func=record)
    command = subs.add_parser('exec', help='Run a command and record measured duration and output')
    command.add_argument('--run-dir', required=True, type=Path)
    command.add_argument('--actor', required=True)
    command.add_argument('--label', required=True)
    command.add_argument('command', nargs=argparse.REMAINDER)
    command.set_defaults(func=execute)
    summary = subs.add_parser('report', help='Combine actor logs after writers have checkpointed')
    summary.add_argument('--run-dir', required=True, type=Path)
    summary.set_defaults(func=report)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
