"""Refresh bundled resources from the shared authoring sources."""

from pathlib import Path
import argparse
import shutil


ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    'goal-gated': ('Goal Gated', 'Execute reviewed steps with independent validation'),
    'goal-continuous': ('Goal Continuous', 'Pursue the full goal with final independent review'),
    'goal-observe': ('Goal Observe', 'Measure continuous work with a reporting observer'),
    'goal-steer': ('Goal Steer', 'Guide continuous work with an independent observer'),
    'goal-hybrid': ('Goal Hybrid', 'Blend continuous work, risk gates, and steering'),
    'goal-adaptive': ('Goal Adaptive', 'Switch execution policies when benefits beat costs'),
    'goal-hybrid-lean': ('Goal Hybrid Lean', 'Implement directly with focused independent reviews'),
    'goal-hybrid-lean-plus': ('Goal Hybrid Lean Plus', 'Review UI integration and same-session state changes'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills', nargs='+', choices=LABELS, default=list(LABELS))
    args = parser.parse_args()
    for name in args.skills:
        title, description = LABELS[name]
        skill = ROOT / 'skills' / name
        for directory in ('references', 'scripts', 'agents'):
            (skill / directory).mkdir(exist_ok=True)
        references = (('lean-plus-operations.md',) if name == 'goal-hybrid-lean-plus' else
                      ('lean-operations.md',) if name == 'goal-hybrid-lean' else ('protocol.md', 'runtime.md'))
        for filename in references:
            shutil.copyfile(ROOT / 'shared' / filename, skill / 'references' / filename)
        if name in ('goal-hybrid', 'goal-adaptive'):
            shutil.copyfile(ROOT / 'shared' / 'v2-operations.md', skill / 'references' / 'v2-operations.md')
        shutil.copyfile(ROOT / 'shared' / 'runlog.py', skill / 'scripts' / 'runlog.py')
        (skill / 'agents' / 'openai.yaml').write_text(
            f'interface:\n  display_name: "{title}"\n'
            f'  short_description: "{description}"\n'
            f'  default_prompt: "Use ${name} to carry out this request and keep an evaluation log."\n',
            encoding='utf-8')
        print(name)


if __name__ == '__main__':
    main()
