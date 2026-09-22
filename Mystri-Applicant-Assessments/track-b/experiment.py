"""Run the integrated Daybreak model (single entry point)."""
import argparse
import json
from pathlib import Path

from starter import load_inputs
from integrated_model import format_executive_summary, run_and_write_trace
from approaches import rank_approaches_for_daybreak


def main():
    parser = argparse.ArgumentParser(description='Daybreak Integrated Collaborating Model (DICM)')
    parser.add_argument(
        '--write',
        type=Path,
        default=Path('output/integrated_report.json'),
        help='Write full JSON report (default: output/integrated_report.json)',
    )
    parser.add_argument(
        '--trace',
        type=Path,
        default=Path('output/dicm_pipeline_trace.log'),
        help='Unified audit trace from start to simulated customer delivery',
    )
    args = parser.parse_args()

    inputs = load_inputs()
    integrated = run_and_write_trace(
        inputs['cases'],
        inputs['requests'],
        inputs['scenario'],
        inputs['events'],
        args.trace,
    )

    report = {
        'integrated_model': integrated,
        'approach_ranking_top5': rank_approaches_for_daybreak()[:5],
        'pipeline_trace_file': integrated.get('pipeline_trace_file'),
    }

    print(format_executive_summary(integrated))
    print('\n---')
    print('Full detail: INTEGRATED_MODEL.md')
    print('Reviewer report: OPERATING_REPORT.md')

    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('\nWrote', args.write)
    print('Wrote trace', args.trace)


if __name__ == '__main__':
    main()
