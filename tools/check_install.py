"""Check both user-level installations against the portable source packages."""

import ast
import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
NAMES = ('goal-gated', 'goal-continuous', 'goal-observe', 'goal-steer', 'goal-hybrid', 'goal-adaptive', 'goal-hybrid-lean', 'goal-hybrid-lean-plus')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    count = 0
    for name in NAMES:
        source = ROOT / 'skills' / name
        for skills_root in (Path.home() / '.agents' / 'skills', Path.home() / '.claude' / 'skills'):
            target = skills_root / name
            for file in source.rglob('*'):
                if file.is_file():
                    installed = target / file.relative_to(source)
                    if not installed.is_file() or digest(file) != digest(installed):
                        raise SystemExit(f'Missing or changed installation file: {installed}')
                    count += 1
            body = (target / 'SKILL.md').read_text(encoding='utf-8')
            for reference in re.findall(r'\]\((references/[^)]+)\)', body):
                if not (target / reference).is_file():
                    raise SystemExit(f'Broken reference: {target / reference}')
            ast.parse((target / 'scripts' / 'runlog.py').read_text(encoding='utf-8'))
            print(f'OK {target} -> {target.resolve()}')
        if (Path.home() / '.claude' / 'skills' / name).resolve() != (Path.home() / '.agents' / 'skills' / name).resolve():
            print(f'NOTE {name}: separate copies; keep future updates synchronized')
    print(f'Verified {count} installed file contents across {len(NAMES) * 2} skill paths.')


if __name__ == '__main__':
    main()
