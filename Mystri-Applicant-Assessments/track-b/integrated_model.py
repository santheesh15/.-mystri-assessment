"""
Daybreak integrated model — one collaborating pipeline.

Combines: rules, three-speed lanes, departure board, tiered technicians,
rotating duty lead, AI assist (human-in-loop), file-request pattern, cost view.
Dry-run only; no messages sent.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from queue_engine import baseline_naive_pending, proposed_ids, triage_all
from team_workboard import build_team_board, baseline_coordinator_only_load
from ai_assist import enrich_coordinator_tasks, photo_screening_decision, technician_prep_checklist
from cost_model import build_cost_structure
from lane_model import duty_lead_for_snapshot, prioritized_board
from approaches import hybrid_incorporation_summary
from customer_registry import summarize_customer_verification, verify_customers
from data_policy import summarize_validation, validate_all
from media_intake import assess_demo_pack
from customer_acknowledgment import (
    build_all_submission_acknowledgments,
    build_demo_intake_not_ok_examples,
    summarize_acknowledgments,
)
from pipeline_trace import PipelineTrace, build_customer_deliveries


@dataclass(frozen=True)
class IntegratedStep:
    order: int
    name: str
    owner: str
    output_summary: str


def run_integrated_pipeline(
    cases,
    requests,
    scenario,
    events=None,
    trace: PipelineTrace | None = None,
) -> dict:
    events = events or []
    snapshot = scenario['snapshot_at']
    if trace is None:
        trace = PipelineTrace(snapshot, scenario.get('dry_run_only', 'dry_run_only'))

    trace.log('LOAD', 'Input registers loaded', f'cases={len(cases)} requests={len(requests)} events={len(events)}')

    validation = validate_all(cases, requests, events)
    trace.log('VALIDATE', summarize_validation(validation))
    for f in validation['findings'][:15]:
        trace.log('VALIDATE', f"{f['severity']}:{f['source']}", f"{f['record_id']} {f['field']} {f['message']}")
    if len(validation['findings']) > 15:
        trace.log('VALIDATE', f"... {len(validation['findings']) - 15} more findings omitted from trace")

    customer = verify_customers(cases, requests)
    trace.log('CUSTOMER_REGISTRY', summarize_customer_verification(customer))
    for check in customer['checks']:
        if check['status'] == 'discarded':
            trace.log('CUSTOMER_REGISTRY', 'DISCARD spam/unverified', str(check))

    requests_verified = customer['requests_for_automation']
    media_checks = assess_demo_pack()
    for m in media_checks:
        trace.log(
            'MEDIA',
            f"format={m['detected_format']} routing={m['routing']}",
            f"file={m['filename']} signals={m.get('quality_signals', ())}",
        )

    triage = triage_all(cases, requests_verified, scenario)
    for row in triage:
        trace.log(
            'RULES',
            f"{row.request_id} disposition={row.disposition}",
            f"{row.case_id} {row.item} {row.reason}",
        )

    submission_acks = build_all_submission_acknowledgments(cases, requests_verified, triage)
    intake_ack_examples = build_demo_intake_not_ok_examples(media_checks)
    trace.log('CUSTOMER_ACK', summarize_acknowledgments(submission_acks))
    trace.log_structured_acknowledgments(submission_acks)
    if intake_ack_examples:
        trace.log(
            'CUSTOMER_ACK',
            f'intake_template_examples={len(intake_ack_examples)} (demo media pack)',
        )
        trace.log_structured_acknowledgments(intake_ack_examples)

    board = build_team_board(cases, requests_verified, scenario, triage)
    departure = prioritized_board(cases, requests_verified, snapshot)
    duty = duty_lead_for_snapshot(snapshot)
    trace.log('HUDDLE', f"duty_lead={duty['duty_lead']} backup={duty['backup_lead']}")
    for row in departure[:8]:
        trace.log('DEPARTURE_BOARD', f"{row['case_id']} lane={row['lane']}", f"score={row['priority_score']} {row['lane_reason']}")

    lane_counts = {}
    for row in departure:
        lane_counts[row['lane']] = lane_counts.get(row['lane'], 0) + 1
    trace.log('LANES', 'Three-speed lane counts', str(lane_counts))

    cases_by_id = {c['case_id']: c for c in cases}
    ai = enrich_coordinator_tasks(board['coordinator_tasks'], cases_by_id)
    for t in board['technician_tasks'][:3]:
        ai.append(technician_prep_checklist(cases_by_id[t['case_id']]))
    uncertain = sum(1 for r in triage if r.disposition == 'uncertain')
    ai.append(photo_screening_decision('C018', has_conflict=True))

    for s in ai:
        trace.log('AI_ASSIST', s.step, f"{s.case_id} gate={s.human_gate}")

    for t in board['technician_tasks']:
        trace.log(
            'TECH',
            f"{t['owner']} L{t.get('work_level')} {t['task']}",
            f"{t['case_id']} {t['reason']}",
        )

    metrics = {
        **board,
        'uncertain_count': uncertain,
        'ai_draft_count': len([s for s in ai if s.step == 'coordinator_customer_draft']),
    }
    cost = build_cost_structure(scenario, metrics)
    trace.log(
        'COST',
        'Weekly time and tool cap check',
        (
            f"net_min_saved={cost['time_minutes_per_week']['net_saved']} "
            f"monthly_tool_budget_inr={cost['assumptions']['monthly_tool_budget_inr']}"
        ),
    )

    baseline_pending = baseline_naive_pending(requests_verified)
    rules_proposals = proposed_ids(triage)
    solo = baseline_coordinator_only_load(cases, requests_verified)

    requests_by_id = {r['request_id']: r for r in requests_verified}
    drafts_by_case = {
        s.case_id: s.suggestion for s in ai if s.step == 'coordinator_customer_draft'
    }
    deliveries = build_customer_deliveries(triage, requests_by_id, drafts_by_case)
    for d in deliveries:
        trace.log(
            'COORDINATOR',
            'Approve draft follow-up (simulated)',
            f"{d['request_id']} preview={d.get('draft_preview', '')[:80]}...",
        )
    trace.finish_customer_delivery(
        deliveries,
        structured_ack_count=len(submission_acks) + len(intake_ack_examples),
    )

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
        IntegratedStep(0, 'Data & policy validation', 'system → coordinator on errors', summarize_validation(validation)),
        IntegratedStep(0.25, 'Customer register verification', 'system discards spam; coordinator audit', summarize_customer_verification(customer)),
        IntegratedStep(0.5, 'Customer file intake (multi-format)', 'media_intake + technician', f"{len(media_checks)} sample files"),
        IntegratedStep(1, 'Daily huddle', f"coordinator + duty lead {duty['duty_lead']}", f"uncertain={uncertain}"),
        IntegratedStep(2, 'Lane classification', 'rules + lane_model', str(lane_counts)),
        IntegratedStep(3, 'Customer contact gate', 'coordinator (approve)', f"{len(rules_proposals)} drafts vs {len(baseline_pending)} naive"),
        IntegratedStep(4, 'Parallel technician work', 'tiered T1–T4', str(board['load_by_owner'])),
        IntegratedStep(5, 'AI assist', 'coordinator + technicians', f"{len(ai)} suggestions"),
        IntegratedStep(6, 'Cost check', 'owner', f"net_min={cost['time_minutes_per_week']['net_saved']}"),
    ]

    return {
        'name': 'Daybreak Integrated Collaborating Model (DICM)',
        'snapshot_at': snapshot,
        'one_line_pitch': (
            'Keep inbox and spreadsheet; add rules, lanes, tiered techs, rotating lead, '
            'and capped AI drafts with file-upload links—humans approve every customer touch.'
        ),
        'collaboration_flow': [s.__dict__ for s in steps],
        'data_policy_validation': validation,
        'customer_verification': customer,
        'customer_media_intake_samples': media_checks,
        'hybrid_layers': hybrid_incorporation_summary(),
        'duty_lead': duty,
        'departure_board': departure,
        'lane_counts': lane_counts,
        'triage_counts': triage_counts,
        'triage_rows': triage_rows,
        'team_workboard': board,
        'ai_assist': [s.__dict__ for s in ai],
        'cost_structure': cost,
        'customer_delivery_simulation': deliveries,
        'customer_structured_receipt_acks': [a.payload for a in submission_acks],
        'customer_structured_intake_examples': [a.payload for a in intake_ack_examples],
        'pipeline_trace_lines': trace.lines,
        'comparison': {
            'solo_coordinator_load': solo,
            'coordinator_after_split': board['coordinator_tasks_after_split'],
            'naive_pending_reminders': len(baseline_pending),
            'rules_based_drafts': len(rules_proposals),
            'prevented_bad_reminders': sorted(baseline_pending - rules_proposals),
        },
    }


def run_and_write_trace(cases, requests, scenario, events, trace_path: Path) -> dict:
    dry = scenario.get('dry_run_only', True)
    mode = 'dry_run_only' if dry else 'live_mode_not_used_in_assessment'
    trace = PipelineTrace(scenario['snapshot_at'], mode)
    report = run_integrated_pipeline(cases, requests, scenario, events, trace=trace)
    trace.write(trace_path)
    report['pipeline_trace_file'] = str(trace_path)
    return report


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
    lines.append(f"Validation: {summarize_validation(report['data_policy_validation'])}")
    cv = report['customer_verification']
    lines.append(
        f"Customers: verified={cv['verified_request_count']} discarded={cv['discarded_request_count']}"
    )
    lines.append(f"Duty lead this week: {report['duty_lead']['duty_lead']} (backup {report['duty_lead']['backup_lead']})")
    lines.append(f"Lanes: {report['lane_counts']}")
    c = report['comparison']
    lines.append(
        f"Contact quality: {c['rules_based_drafts']} rule-based drafts vs {c['naive_pending_reminders']} naive (prevented {len(c['prevented_bad_reminders'])} bad IDs)"
    )
    if report.get('pipeline_trace_file'):
        lines.append(f"Unified trace log: {report['pipeline_trace_file']}")
    acks = report.get('customer_structured_receipt_acks') or []
    if acks:
        ok_n = sum(1 for a in acks if a.get('ok'))
        lines.append(
            f"Structured receipt responses: {len(acks)} sent (ok={ok_n}, not_ok_or_review={len(acks) - ok_n})"
        )
    return '\n'.join(lines)
