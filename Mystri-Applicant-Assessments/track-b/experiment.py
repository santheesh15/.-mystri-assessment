"""Run Product 1 — Daybreak DICM Core (Track B scoped experiment)."""
import argparse
import json
from pathlib import Path

from console_io import configure_utf8_stdout
from starter import load_inputs
from integrated_model import format_executive_summary, run_and_write_trace
from approaches import rank_approaches_for_daybreak


def main():
    configure_utf8_stdout()
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
    parser.add_argument(
        '--acks',
        type=Path,
        default=Path('output/customer_structured_responses.json'),
        help='Structured OK/not-OK receipt responses for customers',
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

    ack_bundle = {
        'schema_version': 'daybreak.customer_ack_bundle.v1',
        'submission_receipts': integrated.get('customer_structured_receipt_acks', []),
        'intake_quality_examples': integrated.get('customer_structured_intake_examples', []),
    }
    report = {
        'integrated_model': integrated,
        'approach_ranking_top5': rank_approaches_for_daybreak()[:5],
        'pipeline_trace_file': integrated.get('pipeline_trace_file'),
        'customer_structured_responses': ack_bundle,
    }

    print(format_executive_summary(integrated))
    print('\n---')
    print('Full detail: INTEGRATED_MODEL.md')
    print('Reviewer report: OPERATING_REPORT.md')

    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(report, indent=2), encoding='utf-8')
    args.acks.parent.mkdir(parents=True, exist_ok=True)
    args.acks.write_text(json.dumps(ack_bundle, indent=2), encoding='utf-8')
    print('\nWrote', args.write)
    print('Wrote trace', args.trace)
    print('Wrote structured customer responses', args.acks)


if __name__ == '__main__':
    main()
