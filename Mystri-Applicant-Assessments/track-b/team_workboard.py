"""Five-person workboard: 1 coordinator + 4 technicians (dry-run tasks only)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from queue_engine import CLOSED_CASE_STATUSES, RowResult, _parse_ts


@dataclass(frozen=True)
class TeamTask:
    role: str  # coordinator | technician
    owner: str  # coordinator | T1..T4
    case_id: str
    task: str
    reason: str
    request_ids: tuple[str, ...] = ()


def assign_technician(case_id: str, technician_count: int) -> str:
    digits = ''.join(ch for ch in case_id if ch.isdigit())
    n = int(digits or 0)
    slot = (n - 1) % max(technician_count, 1)
    return f'T{slot + 1}'


def _requests_for_case(requests: Iterable[dict], case_id: str) -> list[dict]:
    return [r for r in requests if r['case_id'] == case_id]


def _photo_received_clean(case_requests: list[dict]) -> bool:
    for r in case_requests:
        if r['item'] != 'fault_photo':
            continue
        if r.get('status') == 'received' and not (r.get('received_at') or '').strip():
            return True
        if (r.get('received_at') or '').strip() and r.get('status') != 'pending':
            return True
    return False


def _photo_uncertain(case_requests: list[dict]) -> bool:
    for r in case_requests:
        if r['item'] != 'fault_photo':
            continue
        if r.get('status') == 'pending' and (r.get('received_at') or '').strip():
            return True
    return False


def build_team_board(
    cases: Iterable[dict],
    requests: Iterable[dict],
    scenario: dict,
    triage: list[RowResult],
) -> dict:
    tech_count = int(scenario.get('technicians', 4))
    by_case = {c['case_id']: c for c in cases}
    request_list = list(requests)

    coordinator_tasks: list[TeamTask] = []
    technician_tasks: list[TeamTask] = []

    for row in triage:
        if row.disposition == 'propose':
            coordinator_tasks.append(
                TeamTask(
                    'coordinator',
                    'coordinator',
                    row.case_id,
                    'draft_customer_followup',
                    row.reason,
                    (row.request_id,),
                )
            )
        elif row.disposition == 'uncertain':
            coordinator_tasks.append(
                TeamTask(
                    'coordinator',
                    'coordinator',
                    row.case_id,
                    'review_before_any_contact',
                    row.reason,
                    (row.request_id,),
                )
            )

    for case in cases:
        cid = case['case_id']
        status = case['status']
        if status in CLOSED_CASE_STATUSES:
            continue
        if status not in {'waiting_info', 'quote_sent'}:
            continue

        case_reqs = _requests_for_case(request_list, cid)
        owner = assign_technician(cid, tech_count)

        if status == 'waiting_info' and _photo_uncertain(case_reqs):
            coordinator_tasks.append(
                TeamTask(
                    'coordinator',
                    'coordinator',
                    cid,
                    'reconcile_inbox_vs_request_row',
                    'Photo may exist off-thread; coordinator syncs status before tech quote work',
                    tuple(r['request_id'] for r in case_reqs if r['item'] == 'fault_photo'),
                )
            )
            continue

        if status == 'waiting_info' and _photo_received_clean(case_reqs):
            technician_tasks.append(
                TeamTask(
                    'technician',
                    owner,
                    cid,
                    'human_photo_quality_check',
                    'Technician confirms photo/model is quotable (not automated)',
                    tuple(r['request_id'] for r in case_reqs if r['item'] == 'fault_photo'),
                )
            )
            continue

        if status == 'waiting_info':
            has_access = any(
                r['item'] == 'site_access' and (r.get('status') == 'received' or r.get('received_at'))
                for r in case_reqs
            )
            if has_access:
                technician_tasks.append(
                    TeamTask(
                        'technician',
                        owner,
                        cid,
                        'prep_quote_while_waiting_for_photo',
                        f"Parallel prep on {case['service_type']} while coordinator chases missing photo",
                        tuple(r['request_id'] for r in case_reqs if r['item'] == 'site_access'),
                    )
                )
            else:
                technician_tasks.append(
                    TeamTask(
                        'technician',
                        owner,
                        cid,
                        'standby_case_brief',
                        'Read case note; no customer contact—ready when info arrives',
                        tuple(r['request_id'] for r in case_reqs[:1]),
                    )
                )

        if status == 'quote_sent':
            technician_tasks.append(
                TeamTask(
                    'technician',
                    owner,
                    cid,
                    'hold_parts_plan',
                    'Keep parts plan ready if customer approves quote',
                    (cid,),
                )
            )

    # De-duplicate coordinator reconcile tasks already covered by uncertain triage
    seen = set()
    deduped_coord: list[TeamTask] = []
    for t in coordinator_tasks:
        key = (t.task, t.case_id, t.request_ids)
        if key in seen:
            continue
        seen.add(key)
        deduped_coord.append(t)

    load_by_owner: dict[str, int] = {'coordinator': len(deduped_coord)}
    for t in technician_tasks:
        load_by_owner[t.owner] = load_by_owner.get(t.owner, 0) + 1

    baseline_single_person = len(
        [r for r in request_list if r.get('status') == 'pending' and r.get('followup_allowed') == '1']
    ) + len([c for c in cases if c['status'] == 'waiting_info'])

    return {
        'team_size': {'coordinators': int(scenario.get('coordinators', 1)), 'technicians': tech_count},
        'coordinator_tasks': [t.__dict__ for t in deduped_coord],
        'technician_tasks': [t.__dict__ for t in technician_tasks],
        'load_by_owner': load_by_owner,
        'baseline_all_work_on_coordinator': baseline_single_person,
        'coordinator_tasks_after_split': len(deduped_coord),
    }


def baseline_coordinator_only_load(cases: Iterable[dict], requests: Iterable[dict]) -> int:
    pending = sum(
        1 for r in requests if r.get('status') == 'pending' and r.get('followup_allowed', '').strip() == '1'
    )
    waiting = sum(1 for c in cases if c['status'] == 'waiting_info')
    return pending + waiting
