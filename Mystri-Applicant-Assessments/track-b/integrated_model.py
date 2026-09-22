"""
Daybreak integrated model — one collaborating pipeline.

Combines: rules, three-speed lanes, departure board, tiered technicians,
rotating duty lead, AI assist (human-in-loop), file-request pattern, cost view.
Dry-run only; no messages sent.
"""
from __future__ import annotations

from dataclasses import dataclass

from queue_engine import baseline_naive_pending, proposed_ids, triage_all
from team_workboard import build_team_board, baseline_coordinator_only_load
from ai_assist import enrich_coordinator_tasks, photo_screening_decision, technician_prep_checklist
from cost_model import build_cost_structure
from lane_model import duty_lead_for_snapshot, prioritized_board
from approaches import hybrid_incorporation_summary


@dataclass(frozen=True)
class IntegratedStep:
    order: int
    name: str
    owner: str
    output_summary: str


def run_integrated_pipeline(cases, requests, scenario) -> dict:
    snapshot = scenario['snapshot_at']
    triage = triage_all(cases, requests, scenario)
    board = build_team_board(cases, requests, scenario, triage)
    departure = prioritized_board(cases, requests, snapshot)
    duty = duty_lead_for_snapshot(snapshot)

    cases_by_id = {c['case_id']: c for c in cases}
    ai = enrich_coordinator_tasks(board['coordinator_tasks'], cases_by_id)
    for t in board['technician_tasks'][:3]:
        ai.append(technician_prep_checklist(cases_by_id[t['case_id']]))
    uncertain = sum(1 for r in triage if r.disposition == 'uncertain')
    ai.append(photo_screening_decision('C018', has_conflict=True))

    metrics = {
        **board,
        'uncertain_count': uncertain,
        'ai_draft_count': len([s for s in ai if s.step == 'coordinator_customer_draft']),
    }
    cost = build_cost_structure(scenario, metrics)

    baseline_pending = baseline_naive_pending(requests)
    rules_proposals = proposed_ids(triage)
    solo = baseline_coordinator_only_load(cases, requests)

    lane_counts = {}
    for row in departure:
        lane_counts[row['lane']] = lane_counts.get(row['lane'], 0) + 1

    triage_rows = [
        {
            'request_id': r.request_id,
            'case_id': r.case_id,
            'item': r.item,
            'disposition': r.disposition,
            'reason': r.reason,
        }
        for r in triage
    ]
    triage_counts = {'propose': 0, 'exclude': 0, 'uncertain': 0}
    for row in triage:
        triage_counts[row.disposition] += 1

    steps = [
        IntegratedStep(
            1,
            'Daily huddle',
            f"coordinator + duty lead {duty['duty_lead']}",
            f"Review {uncertain} uncertain rows and top {min(5, len(departure))} departure-board cases",
        ),
        IntegratedStep(
            2,
            'Lane classification',
            'rules + lane_model',
            f"Express/Standard/Park counts: {lane_counts}",
        ),
        IntegratedStep(
            3,
            'Customer contact gate',
            'coordinator (approve)',
            f"{len(rules_proposals)} draft follow-ups vs {len(baseline_pending)} naive pending",
        ),
        IntegratedStep(
            4,
            'Parallel technician work',
            'tiered T1–T4',
            f"{len(board['technician_tasks'])} tasks; load {board['load_by_owner']}",
        ),
        IntegratedStep(
            5,
            'AI assist',
            'coordinator + technicians',
            f"{len(ai)} suggestions; all require human gate",
        ),
        IntegratedStep(
            6,
            'Cost check',
            'owner',
            f"Net scenario minutes/week saved {cost['time_minutes_per_week']['net_saved']}; tool cap INR {cost['inr_per_month_scenario']['tool_spend_cap']}",
        ),
    ]

    return {
        'name': 'Daybreak Integrated Collaborating Model (DICM)',
        'snapshot_at': snapshot,
        'one_line_pitch': (
            'Keep inbox and spreadsheet; add rules, lanes, tiered techs, rotating lead, '
            'and capped AI drafts with file-upload links—humans approve every customer touch.'
        ),
        'collaboration_flow': [s.__dict__ for s in steps],
        'hybrid_layers': hybrid_incorporation_summary(),
        'duty_lead': duty,
        'departure_board': departure,
        'lane_counts': lane_counts,
        'triage_counts': triage_counts,
        'triage_rows': triage_rows,
        'team_workboard': board,
        'ai_assist': [s.__dict__ for s in ai],
        'cost_structure': cost,
        'comparison': {
            'solo_coordinator_load': solo,
            'coordinator_after_split': board['coordinator_tasks_after_split'],
            'naive_pending_reminders': len(baseline_pending),
            'rules_based_drafts': len(rules_proposals),
            'prevented_bad_reminders': sorted(baseline_pending - rules_proposals),
        },
    }


def format_executive_summary(report: dict) -> str:
    lines = [
        report['name'],
        report['one_line_pitch'],
        '',
        'Collaboration steps (in order):',
    ]
    for s in report['collaboration_flow']:
        lines.append(f"  {s['order']}. {s['name']} [{s['owner']}] — {s['output_summary']}")
    lines.append('')
    lines.append(f"Duty lead this week: {report['duty_lead']['duty_lead']} (backup {report['duty_lead']['backup_lead']})")
    lines.append(f"Lanes: {report['lane_counts']}")
    c = report['comparison']
    lines.append(
        f"Contact quality: {c['rules_based_drafts']} rule-based drafts vs {c['naive_pending_reminders']} naive (prevented {len(c['prevented_bad_reminders'])} bad IDs)"
    )
    return '\n'.join(lines)
