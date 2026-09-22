"""Run the Track B experiment: rules queue vs naive baseline (dry-run)."""
import argparse
import json
from pathlib import Path

from starter import load_inputs
from queue_engine import baseline_naive_pending, proposed_ids, triage_all
from team_workboard import baseline_coordinator_only_load, build_team_board


def summarize(results):
    counts = {'propose': 0, 'exclude': 0, 'uncertain': 0}
    for row in results:
        counts[row.disposition] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description='Daybreak follow-up queue experiment')
    parser.add_argument('--write', type=Path, help='Write JSON report to this path')
    args = parser.parse_args()

    inputs = load_inputs()
    results = triage_all(inputs['cases'], inputs['requests'], inputs['scenario'])
    board = build_team_board(inputs['cases'], inputs['requests'], inputs['scenario'], results)
    baseline = baseline_naive_pending(inputs['requests'])
    rules = proposed_ids(results)
    solo_load = baseline_coordinator_only_load(inputs['cases'], inputs['requests'])

    prevented = sorted(baseline - rules)
    missed = sorted(rules - baseline)

    report = {
        'snapshot_at': inputs['scenario']['snapshot_at'],
        'counts': summarize(results),
        'baseline_pending_followups': len(baseline),
        'rules_proposed_followups': len(rules),
        'baseline_would_contact_prevented_by_rules': prevented,
        'rules_only_not_in_baseline': missed,
        'team_workboard': board,
        'rows': [
            {
                'request_id': r.request_id,
                'case_id': r.case_id,
                'item': r.item,
                'disposition': r.disposition,
                'reason': r.reason,
                'draft_channel': r.draft_channel,
                'draft_contact': r.draft_contact,
            }
            for r in results
        ],
    }

    print('Daybreak follow-up queue (dry-run)')
    print('Team:', board['team_size'])
    print('Snapshot:', report['snapshot_at'])
    print('Disposition counts:', report['counts'])
    print('Baseline naive pending reminders:', report['baseline_pending_followups'])
    print('Rules-engine proposed drafts:', report['rules_proposed_followups'])
    print('Prevented mistaken baseline contacts:', len(prevented), prevented)
    print(
        'Workload — old way (coordinator alone):',
        solo_load,
        'items vs split model coordinator queue:',
        board['coordinator_tasks_after_split'],
        '+ technician parallel tasks:',
        len(board['technician_tasks']),
    )
    print('Tasks per person:', board['load_by_owner'])
    if missed:
        print('Rules-only proposals (not in baseline):', missed)

    proposes = [r for r in results if r.disposition == 'propose']
    if proposes:
        print('\nCoordinator draft actions (not sent):')
        for r in proposes[:5]:
            print(f"  {r.request_id} -> {r.draft_channel} {r.draft_contact}: {r.reason}")

    tech = board['technician_tasks'][:5]
    if tech:
        print('\nSample technician parallel tasks (no customer contact):')
        for t in tech:
            print(f"  {t['owner']} {t['case_id']} {t['task']}: {t['reason']}")

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('\nWrote', args.write)


if __name__ == '__main__':
    main()
