"""Validate packaged workflow resources without requiring an agent host."""

import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'goal-gated', 'goal-continuous', 'goal-observe', 'goal-steer',
    'goal-hybrid', 'goal-adaptive', 'goal-hybrid-lean', 'goal-hybrid-lean-plus',
}


def main():
    codex = json.loads((ROOT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    claude = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
    assert codex['name'] == claude['name'] == 'testing-workflows'
    assert codex['version'] == claude['version']
    assert (ROOT / codex['skills']).resolve() == ROOT / 'skills'
    assert marketplace['plugins'][0]['name'] == claude['name']
    assert (ROOT / marketplace['plugins'][0]['source']).resolve() == ROOT
    skills = {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir() and p.name != '__pycache__'}
    assert skills == EXPECTED, skills
    files = 0
    for name in sorted(skills):
        folder = ROOT / 'skills' / name
        body = (folder / 'SKILL.md').read_text(encoding='utf-8')
        assert body.startswith('---\n') and f'name: {name}\n' in body
        assert '\ndescription: ' in body
        assert (folder / 'agents/openai.yaml').is_file()
        assert (folder / 'scripts/runlog.py').is_file()
        for path in folder.rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            files += 1
            assert not path.is_symlink(), path
            if path.suffix == '.py':
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            if path.suffix == '.md':
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                    if '://' in link or link.startswith(('#', 'mailto:')):
                        continue
                    target = (path.parent / link.split('#', 1)[0]).resolve()
                    assert target.is_relative_to(folder.resolve()), (path, link)
                    assert target.exists(), (path, link)
        print(f'OK {name}')
    print(f'Validated {len(skills)} self-contained skills and {files} packaged files.')


if __name__ == '__main__':
    main()
