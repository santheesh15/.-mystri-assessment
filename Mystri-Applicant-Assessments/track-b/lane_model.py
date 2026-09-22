"""Three-speed lanes + departure-board priority + rotating duty lead."""
from __future__ import annotations

from datetime import datetime


def _parse_ts(value: str) -> datetime | None:
    if not value or not str(value).strip():
        return None
    return datetime.fromisoformat(str(value).strip())


def classify_case_lane(case: dict, requests_for_case: list[dict]) -> dict:
    """Express = ready for technician quote path; Standard = active chase; Park = no automation."""
    status = case['status']
    if status in {'completed', 'cancelled', 'scheduled'}:
        return {'lane': 'park', 'reason': f'Case {status} — no chase'}

    if any(r.get('followup_allowed', '').strip() == '0' for r in requests_for_case):
        return {'lane': 'park', 'reason': 'Customer opt-out / do not follow up'}

    pending_conflicts = [
        r
        for r in requests_for_case
        if r.get('status') == 'pending' and (r.get('received_at') or '').strip()
    ]
    if pending_conflicts:
        return {'lane': 'park', 'reason': 'Data conflict — coordinator reconcile (human)'}

    photo_received = any(
        r['item'] == 'fault_photo'
        and ((r.get('status') == 'received') or (r.get('received_at') or '').strip())
        and r.get('status') != 'pending'
        for r in requests_for_case
    )
    if status == 'waiting_info' and photo_received:
        return {'lane': 'express', 'reason': 'Photo received — technician quality check / quote prep'}

    if status in {'waiting_info', 'quote_sent'}:
        return {'lane': 'standard', 'reason': 'Eligible for coordinated follow-up + parallel tech work'}

    return {'lane': 'park', 'reason': 'Outside active workflow'}


def priority_score(case: dict, snapshot_at: datetime) -> float:
    """Departure-board style: higher = coordinator should look first."""
    opened = _parse_ts(case.get('opened_at'))
    days_open = 0.0
    if opened:
        days_open = max(0.0, (snapshot_at - opened).total_seconds() / 86400.0)
    quote = case.get('quote_value_inr') or ''
    try:
        value = float(quote) if str(quote).strip() else 0.0
    except ValueError:
        value = 0.0
    status_boost = {'waiting_info': 2.0, 'quote_sent': 1.5}.get(case['status'], 0.0)
    return days_open * 1.0 + (value / 1000.0) + status_boost


def prioritized_board(cases: list[dict], requests: list[dict], snapshot_at: str) -> list[dict]:
    snap = _parse_ts(snapshot_at)
    if snap is None:
        raise ValueError('snapshot_at required')
    by_case: dict[str, list[dict]] = {}
    for r in requests:
        by_case.setdefault(r['case_id'], []).append(r)

    rows = []
    for case in cases:
        cid = case['case_id']
        lane = classify_case_lane(case, by_case.get(cid, []))
        if lane['lane'] == 'park' and case['status'] in {'completed', 'cancelled'}:
            continue
        rows.append(
            {
                'case_id': cid,
                'status': case['status'],
                'lane': lane['lane'],
                'lane_reason': lane['reason'],
                'priority_score': round(priority_score(case, snap), 2),
                'service_type': case.get('service_type', ''),
            }
        )
    return sorted(rows, key=lambda r: (-r['priority_score'], r['case_id']))


def duty_lead_for_snapshot(snapshot_at: str) -> dict:
    """Rotate T1 duty between T1 and T2 by week — spreads leadership load."""
    snap = _parse_ts(snapshot_at)
    if snap is None:
        return {'duty_lead': 'T1', 'note': 'Default lead'}
    week = snap.isocalendar().week
    lead = 'T1' if week % 2 else 'T2'
    backup = 'T2' if lead == 'T1' else 'T1'
    return {
        'duty_lead': lead,
        'backup_lead': backup,
        'iso_week': week,
        'note': 'Rotating duty lead runs daily huddle with coordinator; escalates uncertain rows',
    }
