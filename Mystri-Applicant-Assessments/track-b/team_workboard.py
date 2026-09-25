"""Five-person workboard: 1 coordinator + 4 tiered technicians (dry-run tasks only)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from queue_engine import CLOSED_CASE_STATUSES, RowResult


# Higher rank = senior; harder tasks require higher minimum rank.
TECH_ROSTER = (
    {'id': 'T1', 'rank': 4, 'title': 'Lead technician', 'capacity': 3},
    {'id': 'T2', 'rank': 3, 'title': 'Senior technician', 'capacity': 3},
    {'id': 'T3', 'rank': 2, 'title': 'Technician', 'capacity': 4},
    {'id': 'T4', 'rank': 1, 'title': 'Apprentice technician', 'capacity': 4},
)

TASK_WORK_LEVEL = {
    'human_photo_quality_check': 4,
    'prep_quote_while_waiting_for_photo': 3,
    'hold_parts_plan': 3,
    'standby_case_brief': 1,
}


@dataclass(frozen=True)
class TeamTask:
    role: str  # coordinator | technician
    owner: str  # coordinator | T1..T4
    case_id: str
    task: str
    reason: str
    request_ids: tuple[str, ...] = ()
    work_level: int = 1
    owner_title: str = ''


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


def assign_by_hierarchy(unassigned: list[TeamTask]) -> list[TeamTask]:
    """Assign each task to the least-loaded technician who meets the work level."""
    load = {t['id']: 0 for t in TECH_ROSTER}
    roster_by_id = {t['id']: t for t in TECH_ROSTER}
    assigned: list[TeamTask] = []

    for task in sorted(unassigned, key=lambda t: (-t.work_level, t.case_id)):
        level = task.work_level
        eligible = [t for t in TECH_ROSTER if t['rank'] >= level and load[t['id']] < t['capacity']]
        if not eligible:
            eligible = [t for t in TECH_ROSTER if load[t['id']] < t['capacity']]
        if not eligible:
            eligible = list(TECH_ROSTER)
        pick = min(eligible, key=lambda t: (load[t['id']], -t['rank']))
        load[pick['id']] += 1
        assigned.append(
            TeamTask(
                task.role,
                pick['id'],
                task.case_id,
                task.task,
                task.reason,
                task.request_ids,
                task.work_level,
                pick['title'],
            )
        )
    return assigned


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
    tech_unassigned: list[TeamTask] = []

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
            task_name = 'human_photo_quality_check'
            tech_unassigned.append(
                TeamTask(
                    'technician',
                    '',
                    cid,
                    task_name,
                    'Technician confirms photo/model is quotable (not automated)',
                    tuple(r['request_id'] for r in case_reqs if r['item'] == 'fault_photo'),
                    TASK_WORK_LEVEL[task_name],
                )
            )
            continue

        if status == 'waiting_info':
            has_access = any(
                r['item'] == 'site_access' and (r.get('status') == 'received' or r.get('received_at'))
                for r in case_reqs
            )
            if has_access:
                task_name = 'prep_quote_while_waiting_for_photo'
                tech_unassigned.append(
                    TeamTask(
                        'technician',
                        '',
                        cid,
                        task_name,
                        f"Parallel prep on {case['service_type']} while coordinator chases missing photo",
                        tuple(r['request_id'] for r in case_reqs if r['item'] == 'site_access'),
                        TASK_WORK_LEVEL[task_name],
                    )
                )
            else:
                task_name = 'standby_case_brief'
                tech_unassigned.append(
                    TeamTask(
                        'technician',
                        '',
                        cid,
                        task_name,
                        'Read case note; no customer contact—ready when info arrives',
                        tuple(r['request_id'] for r in case_reqs[:1]),
                        TASK_WORK_LEVEL[task_name],
                    )
                )

        if status == 'quote_sent':
            task_name = 'hold_parts_plan'
            tech_unassigned.append(
                TeamTask(
                    'technician',
                    '',
                    cid,
                    task_name,
                    'Keep parts plan ready if customer approves quote',
                    tuple(r['request_id'] for r in case_reqs if r['item'] == 'quote_approval') or (cid,),
                    TASK_WORK_LEVEL[task_name],
                )
            )

    technician_tasks = assign_by_hierarchy(tech_unassigned)

    seen = set()
    deduped_coord: list[TeamTask] = []
    for t in coordinator_tasks:
        key = (t.task, t.case_id, t.request_ids)
        if key in seen:
            continue
        seen.add(key)
        deduped_coord.append(t)

    load_by_owner: dict[str, int] = {'coordinator': len(deduped_coord)}
    load_by_level: dict[int, int] = {}
    for t in technician_tasks:
        load_by_owner[t.owner] = load_by_owner.get(t.owner, 0) + 1
        load_by_level[t.work_level] = load_by_level.get(t.work_level, 0) + 1

    baseline_single_person = len(
        [r for r in request_list if r.get('status') == 'pending' and r.get('followup_allowed') == '1']
    ) + len([c for c in cases if c['status'] == 'waiting_info'])

    return {
        'team_size': {'coordinators': int(scenario.get('coordinators', 1)), 'technicians': tech_count},
        'technician_hierarchy': list(TECH_ROSTER),
        'task_work_levels': dict(TASK_WORK_LEVEL),
        'coordinator_tasks': [t.__dict__ for t in deduped_coord],
        'technician_tasks': [t.__dict__ for t in technician_tasks],
        'load_by_owner': load_by_owner,
        'load_by_work_level': load_by_level,
        'baseline_all_work_on_coordinator': baseline_single_person,
        'coordinator_tasks_after_split': len(deduped_coord),
    }


def baseline_coordinator_only_load(cases: Iterable[dict], requests: Iterable[dict]) -> int:
    pending = sum(
        1 for r in requests if r.get('status') == 'pending' and r.get('followup_allowed', '').strip() == '1'
    )
    waiting = sum(1 for c in cases if c['status'] == 'waiting_info')
    return pending + waiting
