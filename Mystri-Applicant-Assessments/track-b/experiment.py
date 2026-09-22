"""Run the Track B experiment: rules queue vs naive baseline (dry-run)."""
import argparse
import json
from pathlib import Path

from starter import load_inputs
from queue_engine import baseline_naive_pending, proposed_ids, triage_all
from team_workboard import baseline_coordinator_only_load, build_team_board
from ai_assist import enrich_coordinator_tasks, photo_screening_decision, technician_prep_checklist
from cost_model import build_cost_structure
from approaches import hybrid_incorporation_summary, rank_approaches_for_daybreak
from lane_model import duty_lead_for_snapshot, prioritized_board


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

    cases_by_id = {c['case_id']: c for c in inputs['cases']}
    ai_samples = enrich_coordinator_tasks(board['coordinator_tasks'], cases_by_id)
    for t in board['technician_tasks'][:3]:
        case = cases_by_id[t['case_id']]
        ai_samples.append(technician_prep_checklist(case))
    uncertain_count = sum(1 for r in results if r.disposition == 'uncertain')
    ai_samples.append(
        photo_screening_decision('C018', has_conflict=True)
    )

    metrics = {
        **board,
        'uncertain_count': uncertain_count,
        'ai_draft_count': len([s for s in ai_samples if s.step == 'coordinator_customer_draft']),
    }
    cost = build_cost_structure(inputs['scenario'], metrics)

    board_rows = prioritized_board(inputs['cases'], inputs['requests'], inputs['scenario']['snapshot_at'])
    lane_counts = {}
    for row in board_rows:
        lane_counts[row['lane']] = lane_counts.get(row['lane'], 0) + 1
    duty = duty_lead_for_snapshot(inputs['scenario']['snapshot_at'])
    synthesis = {
        'hybrid_layers': hybrid_incorporation_summary(),
        'approach_ranking': rank_approaches_for_daybreak()[:5],
        'three_speed_lanes': lane_counts,
        'departure_board_top5': board_rows[:5],
        'rotating_duty_lead': duty,
    }

    report = {
        'snapshot_at': inputs['scenario']['snapshot_at'],
        'counts': summarize(results),
        'baseline_pending_followups': len(baseline),
        'rules_proposed_followups': len(rules),
        'baseline_would_contact_prevented_by_rules': prevented,
        'rules_only_not_in_baseline': missed,
        'team_workboard': board,
        'cost_structure': cost,
        'ai_assist_samples': [s.__dict__ for s in ai_samples],
        'out_of_box_synthesis': synthesis,
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
    print('Tasks by work level:', board.get('load_by_work_level'))
    if board.get('technician_hierarchy'):
        print('Technician hierarchy:', [f"{t['id']} rank {t['rank']} ({t['title']})" for t in board['technician_hierarchy']])
    print('Cost/time (scenario): net saved min/week =', cost['time_minutes_per_week']['net_saved'])
    print('Tool cap INR/month =', cost['inr_per_month_scenario']['tool_spend_cap'])
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
            print(
                f"  {t['owner']} ({t.get('owner_title', '')}) L{t.get('work_level', '?')} "
                f"{t['case_id']} {t['task']}: {t['reason']}"
            )

    if ai_samples:
        print('\nAI assist samples (human approval required):')
        for s in ai_samples[:3]:
            print(f"  [{s.step}] {s.case_id} ({s.confidence}): {s.human_gate}")

    print('\nThree-speed lanes:', lane_counts)
    print('Rotating duty lead:', duty)
    print('Departure board (top 3 priorities):')
    for row in board_rows[:3]:
        print(f"  {row['case_id']} score={row['priority_score']} lane={row['lane']} — {row['lane_reason']}")
    print('Hybrid model layers:', [layer['layer'] for layer in synthesis['hybrid_layers']])

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('\nWrote', args.write)


if __name__ == '__main__':
    main()
