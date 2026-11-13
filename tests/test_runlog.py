import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'shared' / 'runlog.py'


class RunlogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run_dir = self.root / 'run'
        self.request = self.root / 'request.txt'
        self.request.write_text('Build login and CSV export.\nKeep Unicode: café.', encoding='utf-8')

    def call(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, encoding='utf-8')

    def init(self):
        result = self.call('init', '--run-dir', self.run_dir, '--workflow', 'goal-observe', '--request-file', self.request)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_init_preserves_request_and_refuses_overwrite(self):
        self.init()
        self.assertEqual((self.run_dir / 'request.md').read_bytes(), self.request.read_bytes())
        before = (self.run_dir / 'run.json').read_bytes()
        result = self.call('init', '--run-dir', self.run_dir, '--workflow', 'goal-gated', '--request-file', self.request)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.run_dir / 'run.json').read_bytes(), before)

    def test_new_workflows_preserve_mode_and_switch_evidence(self):
        for name in ('goal-hybrid', 'goal-adaptive'):
            with self.subTest(workflow=name):
                target = self.root / name
                result = self.call('init', '--run-dir', target, '--workflow', name, '--request-file', self.request)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = self.root / (name + '-switch.json')
                data.write_text(json.dumps({'from_mode': 'continuous', 'to_mode': 'steer', 'estimated_cost': {'seconds': 40, 'basis': 'explicit test fixture, not a measured run'}, 'actual_tokens': None}), encoding='utf-8')
                result = self.call('event', '--run-dir', target, '--actor', 'controller', '--kind', 'mode_switch_proposed', '--detail', 'Test fixture switch', '--data-file', data)
                self.assertEqual(result.returncode, 0, result.stderr)
                event = json.loads(result.stdout)
                self.assertEqual(event['data']['from_mode'], 'continuous')
                self.assertIsNone(event['data']['actual_tokens'])
                report = self.call('report', '--run-dir', target)
                self.assertEqual(json.loads(report.stdout)['workflow'], name)

    def test_lean_workflow_preserves_direct_implementer_identity(self):
        result = self.call('init', '--run-dir', self.run_dir,
                           '--workflow', 'goal-hybrid-lean', '--actor', 'implementer-1',
                           '--request-file', self.request)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.run_dir / 'request.md').read_bytes(), self.request.read_bytes())
        events = list((self.run_dir / 'events').glob('*.jsonl'))
        self.assertEqual([path.name for path in events], ['implementer-1.jsonl'])
        started = json.loads(events[0].read_text(encoding='utf-8'))
        self.assertEqual(started['actor'], 'implementer-1')
        result = self.call('report', '--run-dir', self.run_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['workflow'], 'goal-hybrid-lean')

    def test_lean_plus_workflow_is_distinct_and_records_ui_review(self):
        result = self.call('init', '--run-dir', self.run_dir,
                           '--workflow', 'goal-hybrid-lean-plus', '--actor', 'implementer-1',
                           '--request-file', self.request)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.call('event', '--run-dir', self.run_dir, '--actor', 'ui-reviewer',
                           '--kind', 'review_finished', '--detail', 'FAIL: state leaks between sessions',
                           '--evidence', 'state-matrix.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        event = json.loads(result.stdout)
        self.assertEqual(event['actor'], 'ui-reviewer')
        self.assertEqual(event['evidence'], ['state-matrix.json'])
        result = self.call('report', '--run-dir', self.run_dir)
        report = json.loads(result.stdout)
        self.assertEqual(report['workflow'], 'goal-hybrid-lean-plus')
        self.assertEqual(report['events_by_kind']['review_finished'], 1)
        self.assertIsNone(report['token_usage'])

    def test_actor_logs_and_unknown_metrics(self):
        self.init()
        for actor in ('implementer-1', 'observer-1'):
            result = self.call('event', '--run-dir', self.run_dir, '--actor', actor, '--kind', 'decision', '--detail', 'Inspect café\nthen continue', '--evidence', 'artifact.txt')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsNotNone(result.stdout)
            self.assertIn('café', result.stdout)
        result = self.call('report', '--run-dir', self.run_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['events_by_kind']['decision'], 2)
        self.assertIsNone(report['token_usage'])
        self.assertIsNone(report['cost'])
        self.assertEqual(len(list((self.run_dir / 'events').glob('*.jsonl'))), 3)

    def test_rejects_actor_path_traversal(self):
        self.init()
        result = self.call('event', '--run-dir', self.run_dir, '--actor', '../escape', '--kind', 'note', '--detail', 'unsafe')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'escape.jsonl').exists())

    def test_command_preserves_failure_and_captures_evidence(self):
        self.init()
        result = self.call('exec', '--run-dir', self.run_dir, '--actor', 'implementer-1', '--label', 'export-test', '--', sys.executable, '-c', 'print("export failed"); raise SystemExit(7)')
        self.assertEqual(result.returncode, 7, result.stderr)
        events = [json.loads(line) for line in (self.run_dir / 'events' / 'implementer-1.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual([e['kind'] for e in events], ['command_started', 'command_finished'])
        end = events[-1]
        self.assertEqual(end['data']['exit_code'], 7)
        self.assertGreaterEqual(end['data']['duration_seconds'], 0)
        evidence = self.run_dir / end['evidence'][0]
        self.assertIn('export failed', evidence.read_text(encoding='utf-8'))

    def test_missing_executable_is_recorded(self):
        self.init()
        result = self.call('exec', '--run-dir', self.run_dir, '--actor', 'implementer-1', '--label', 'missing', '--', '__missing_workflow_test_executable__')
        self.assertEqual(result.returncode, 127, result.stderr)
        events = [json.loads(line) for line in (self.run_dir / 'events' / 'implementer-1.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(events[-1]['data']['exit_code'], 127)

    def test_concurrent_actors_keep_all_events(self):
        self.init()
        processes = []
        for i in range(8):
            processes.append(subprocess.Popen([sys.executable, str(SCRIPT), 'event', '--run-dir', str(self.run_dir), '--actor', f'worker-{i}', '--kind', 'note', '--detail', f'event {i}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for process in processes:
            _, error = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, error)
        result = self.call('report', '--run-dir', self.run_dir)
        self.assertEqual(json.loads(result.stdout)['events_by_kind']['note'], 8)


if __name__ == '__main__':
    unittest.main()
