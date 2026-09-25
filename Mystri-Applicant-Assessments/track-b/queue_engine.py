"""Deterministic follow-up triage for Daybreak Repairs (dry-run only)."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import Iterable


CLOSED_CASE_STATUSES = frozenset({'completed', 'cancelled', 'scheduled'})
INFO_ITEMS = frozenset({'fault_photo', 'serial_number', 'site_access'})
APPROVAL_ITEMS = frozenset({'quote_approval'})


@dataclass(frozen=True)
class RowResult:
    request_id: str
    case_id: str
    item: str
    disposition: str  # propose | exclude | uncertain
    reason: str
    draft_channel: str | None = None
    draft_contact: str | None = None


def _parse_ts(value: str | None) -> datetime | None:
    if value is None or not str(value).strip():
        return None
    return datetime.fromisoformat(str(value).strip())


def _hours_since(earlier: datetime, later: datetime) -> float:
    return (later - earlier).total_seconds() / 3600.0


def triage_request(
    case: dict,
    request: dict,
    snapshot_at: datetime,
    min_gap_hours: int,
) -> RowResult:
    rid = request['request_id']
    cid = request['case_id']
    item = request['item']
    base = RowResult(rid, cid, item, 'exclude', '')

    status = case['status']
    if status in CLOSED_CASE_STATUSES:
        return replace(base, reason=f'Case {cid} is {status}')

    if request.get('followup_allowed', '').strip() != '1':
        return replace(base, reason='followup_allowed is 0')

    received_at = _parse_ts(request.get('received_at'))
    req_status = request.get('status', '').strip()
    if req_status == 'received' or received_at is not None:
        if req_status == 'pending' and received_at is not None:
            return replace(
                base,
                disposition='uncertain',
                reason='pending status conflicts with received_at; needs coordinator review',
            )
        return replace(base, reason='Item already received')

    if item in APPROVAL_ITEMS and status != 'quote_sent':
        return replace(base, reason=f'quote_approval not applicable while case is {status}')
    if item in INFO_ITEMS and status not in {'waiting_info', 'quote_sent'}:
        return replace(
            base,
            disposition='uncertain',
            reason=f'{item} on case in {status}; verify before contact',
        )

    contact = (request.get('contact_address') or '').strip()
    if not contact:
        return replace(base, disposition='uncertain', reason='Missing contact_address')

    last_at = _parse_ts(request.get('last_requested_at'))
    if last_at is None:
        return replace(base, disposition='uncertain', reason='Missing last_requested_at')

    elapsed = _hours_since(last_at, snapshot_at)
    if elapsed < min_gap_hours:
        return replace(
            base,
            reason=f'Only {elapsed:.1f}h since last request; need {min_gap_hours}h',
        )

    channel = (request.get('channel') or 'email').strip()
    return RowResult(
        rid,
        cid,
        item,
        'propose',
        f'Eligible reminder for {item} ({elapsed:.1f}h since last request)',
        draft_channel=channel,
        draft_contact=contact,
    )


def triage_all(cases: Iterable[dict], requests: Iterable[dict], scenario: dict) -> list[RowResult]:
    snapshot_at = _parse_ts(scenario['snapshot_at'])
    if snapshot_at is None:
        raise ValueError('scenario.snapshot_at is required')
    gap = int(scenario.get('minimum_followup_gap_hours', 48))
    by_case = {c['case_id']: c for c in cases}
    results: list[RowResult] = []
    for req in sorted(requests, key=lambda r: r['request_id']):
        case = by_case.get(req['case_id'])
        if case is None:
            results.append(
                RowResult(req['request_id'], req['case_id'], req['item'], 'uncertain', 'Unknown case_id')
            )
            continue
        results.append(triage_request(case, req, snapshot_at, gap))
    return results


def baseline_naive_pending(requests: Iterable[dict]) -> set[str]:
    """Baseline: remind every row still marked pending with follow-up allowed."""
    ids: set[str] = set()
    for req in requests:
        if req.get('status', '').strip() != 'pending':
            continue
        if req.get('followup_allowed', '').strip() != '1':
            continue
        ids.add(req['request_id'])
    return ids


def proposed_ids(results: Iterable[RowResult]) -> set[str]:
    return {r.request_id for r in results if r.disposition == 'propose'}
