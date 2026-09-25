"""Validate export syntax, referential integrity, and Daybreak contact policies."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


CASE_STATUSES = frozenset({'waiting_info', 'quote_sent', 'scheduled', 'completed', 'cancelled'})
REQUEST_ITEMS = frozenset({'fault_photo', 'serial_number', 'site_access', 'quote_approval'})
REQUEST_STATUSES = frozenset({'pending', 'received'})
FOLLOWUP_FLAGS = frozenset({'0', '1'})
CONTACT_RE = re.compile(r'^[^@\s]+@example\.invalid$', re.I)


@dataclass(frozen=True)
class ValidationFinding:
    severity: str  # error | warning | policy
    source: str  # cases | requests | events | customer_policy
    record_id: str
    field: str
    message: str
    handling: str


def _parse_iso(value: str) -> bool:
    if not value or not str(value).strip():
        return False
    try:
        datetime.fromisoformat(str(value).strip())
        return True
    except ValueError:
        return False


def _add(findings: list[ValidationFinding], **kwargs) -> None:
    findings.append(ValidationFinding(**kwargs))


def validate_cases(cases: Iterable[dict]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    seen: set[str] = set()
    for row in cases:
        cid = (row.get('case_id') or '').strip()
        if not cid:
            _add(
                findings,
                severity='error',
                source='cases',
                record_id='?',
                field='case_id',
                message='Missing case_id',
                handling='Row skipped from automated actions; fix export',
            )
            continue
        if cid in seen:
            _add(
                findings,
                severity='error',
                source='cases',
                record_id=cid,
                field='case_id',
                message='Duplicate case_id',
                handling='Manual merge required before automation',
            )
        seen.add(cid)

        status = (row.get('status') or '').strip()
        if status not in CASE_STATUSES:
            _add(
                findings,
                severity='error',
                source='cases',
                record_id=cid,
                field='status',
                message=f'Invalid status {status!r}',
                handling='Treat case as Park lane; coordinator review',
            )

        if not _parse_iso(row.get('opened_at', '')):
            _add(
                findings,
                severity='warning',
                source='cases',
                record_id=cid,
                field='opened_at',
                message='opened_at missing or not ISO-8601',
                handling='Departure-board priority may be wrong; fix timestamp',
            )

        quote = (row.get('quote_value_inr') or '').strip()
        if quote:
            try:
                if float(quote) < 0:
                    raise ValueError
            except ValueError:
                _add(
                    findings,
                    severity='warning',
                    source='cases',
                    record_id=cid,
                    field='quote_value_inr',
                    message='quote_value_inr must be a non-negative number when present',
                    handling='Ignore quote value in priority score',
                )
    return findings


def validate_requests(requests: Iterable[dict], case_ids: set[str]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    seen: set[str] = set()
    for row in requests:
        rid = (row.get('request_id') or '').strip()
        cid = (row.get('case_id') or '').strip()
        if not rid:
            _add(
                findings,
                severity='error',
                source='requests',
                record_id='?',
                field='request_id',
                message='Missing request_id',
                handling='Row excluded from automation',
            )
            continue
        if rid in seen:
            _add(
                findings,
                severity='error',
                source='requests',
                record_id=rid,
                field='request_id',
                message='Duplicate request_id',
                handling='Deduplicate export before automation',
            )
        seen.add(rid)

        if cid not in case_ids:
            _add(
                findings,
                severity='error',
                source='requests',
                record_id=rid,
                field='case_id',
                message=f'Unknown case_id {cid!r}',
                handling='Row routed to uncertain queue',
            )

        item = (row.get('item') or '').strip()
        if item not in REQUEST_ITEMS:
            _add(
                findings,
                severity='error',
                source='requests',
                record_id=rid,
                field='item',
                message=f'Invalid item {item!r}',
                handling='Row excluded from follow-up automation',
            )

        status = (row.get('status') or '').strip()
        if status not in REQUEST_STATUSES:
            _add(
                findings,
                severity='error',
                source='requests',
                record_id=rid,
                field='status',
                message=f'Invalid status {status!r}',
                handling='Coordinator manual review',
            )

        flag = (row.get('followup_allowed') or '').strip()
        if flag not in FOLLOWUP_FLAGS:
            _add(
                findings,
                severity='policy',
                source='customer_policy',
                record_id=rid,
                field='followup_allowed',
                message='followup_allowed must be 0 or 1',
                handling='Default to no contact until corrected',
            )

        for field in ('last_requested_at', 'received_at'):
            val = (row.get(field) or '').strip()
            if val and not _parse_iso(val):
                _add(
                    findings,
                    severity='warning',
                    source='requests',
                    record_id=rid,
                    field=field,
                    message=f'{field} is not valid ISO-8601',
                    handling='Timing rules treat as missing → uncertain/review',
                )

        if status == 'pending' and (row.get('received_at') or '').strip():
            _add(
                findings,
                severity='policy',
                source='customer_policy',
                record_id=rid,
                field='status+received_at',
                message='pending conflicts with received_at (data standards breach)',
                handling='Park automation; coordinator reconciles with customer',
            )

        contact = (row.get('contact_address') or '').strip()
        channel = (row.get('channel') or '').strip()
        if flag == '1' and status == 'pending' and contact:
            if not CONTACT_RE.match(contact):
                _add(
                    findings,
                    severity='policy',
                    source='customer_policy',
                    record_id=rid,
                    field='contact_address',
                    message='Contact must use synthetic example.invalid domain in this exercise',
                    handling='Block auto draft until valid contact on file',
                )
            if channel and channel != 'email':
                _add(
                    findings,
                    severity='policy',
                    source='customer_policy',
                    record_id=rid,
                    field='channel',
                    message='Actionable demo contacts must use email channel',
                    handling='Coordinator uses approved channel only',
                )
        if flag == '0':
            _add(
                findings,
                severity='policy',
                source='customer_policy',
                record_id=rid,
                field='followup_allowed',
                message='Customer opt-out / no follow-up flag set',
                handling='Never auto-contact; policy enforced in rules engine',
            )

    return findings


def validate_events(events: Iterable[dict], case_ids: set[str]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    seen: set[str] = set()
    for row in events:
        eid = (row.get('event_id') or '').strip()
        cid = (row.get('case_id') or '').strip()
        if eid in seen:
            _add(
                findings,
                severity='warning',
                source='events',
                record_id=eid,
                field='event_id',
                message='Duplicate event delivery in export',
                handling='Dedupe before effort metrics (already done in analysis)',
            )
        if eid:
            seen.add(eid)
        if cid and cid not in case_ids:
            _add(
                findings,
                severity='warning',
                source='events',
                record_id=eid or '?',
                field='case_id',
                message=f'Event references unknown case {cid}',
                handling='Ignore event in case-level automation',
            )
        mins = (row.get('active_minutes') or '').strip()
        if mins and not mins.isdigit():
            _add(
                findings,
                severity='warning',
                source='events',
                record_id=eid or '?',
                field='active_minutes',
                message='active_minutes must be blank or integer',
                handling='Exclude from effort sums',
            )
    return findings


def validate_all(cases: list[dict], requests: list[dict], events: list[dict]) -> dict:
    case_ids = {(c.get('case_id') or '').strip() for c in cases if (c.get('case_id') or '').strip()}
    findings: list[ValidationFinding] = []
    findings.extend(validate_cases(cases))
    findings.extend(validate_requests(requests, case_ids))
    findings.extend(validate_events(events, case_ids))

    by_severity = {'error': 0, 'warning': 0, 'policy': 0}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    return {
        'ok_to_run_pipeline': by_severity['error'] == 0,
        'note': 'Warnings/policies do not stop the pipeline; rows are handled per finding.',
        'counts': by_severity,
        'findings': [f.__dict__ for f in findings],
    }


def summarize_validation(report: dict) -> str:
    c = report['counts']
    return (
        f"errors={c.get('error', 0)} warnings={c.get('warning', 0)} "
        f"policy={c.get('policy', 0)} pipeline_ok={report['ok_to_run_pipeline']}"
    )
