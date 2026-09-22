"""Structured customer receipt responses — OK / not OK / under review (dry-run)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from queue_engine import RowResult

SCHEMA_VERSION = 'daybreak.customer_ack.v1'

RECEIVED_OK = 'received_ok'
RECEIVED_NOT_OK = 'received_not_ok'
UNDER_REVIEW = 'under_review'
NOT_APPLICABLE = 'no_submission_on_file'


@dataclass(frozen=True)
class StructuredCustomerResponse:
    """Machine-readable receipt ack plus a short human-facing summary."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload.get('ok'))

    @property
    def request_id(self) -> str:
        return str(self.payload['request_id'])

    def to_json(self) -> str:
        return json.dumps(self.payload, indent=2, sort_keys=True)

    def customer_email_body(self) -> str:
        msg = self.payload['message']
        lines = [
            f"Subject: {msg['title']}",
            f"To: {self.payload['meta']['contact']}",
            '',
            msg['summary'],
            '',
            '--- Structured receipt (for apps / SMS templates) ---',
            self.to_json(),
        ]
        return '\n'.join(lines)


def _item_label(item: str) -> str:
    return item.replace('_', ' ')


def _quality_from_media(media: dict | None) -> dict[str, Any]:
    if not media:
        return {'accepted': True, 'signals': [], 'routing': 'not_checked', 'notes': []}
    routing = media.get('routing', 'human_review')
    signals = list(media.get('quality_signals') or ())
    accepted = routing == 'auto_queue' and 'reject' not in routing
    if routing == 'reject':
        accepted = False
    elif routing == 'human_review' and signals:
        accepted = False
    notes = [media.get('handling', '')] if media.get('handling') else []
    return {
        'accepted': accepted,
        'signals': signals,
        'routing': routing,
        'format': media.get('detected_format'),
        'notes': notes,
    }


def build_submission_acknowledgment(
    case: dict,
    request: dict,
    triage_row: RowResult | None,
    *,
    media_hint: dict | None = None,
) -> StructuredCustomerResponse | None:
    """Build structured ack when the customer has submitted (received on file)."""
    req_status = (request.get('status') or '').strip()
    received_at = (request.get('received_at') or '').strip()
    if not received_at and req_status != 'received':
        return None

    rid = request['request_id']
    cid = request['case_id']
    item = request['item']
    contact = (request.get('contact_address') or f'{cid.lower()}@example.invalid').strip()
    channel = (request.get('channel') or 'email').strip()

    disposition = triage_row.disposition if triage_row else 'exclude'
    triage_reason = triage_row.reason if triage_row else ''

    if disposition == 'uncertain' or (req_status == 'pending' and received_at):
        outcome = UNDER_REVIEW
        ok = False
        title = f'We are confirming your {_item_label(item)} (case {cid})'
        summary = (
            'We see a submission timestamp on your case, but our records need a quick '
            'coordinator check before we mark it fully accepted.'
        )
        next_steps = [
            'A coordinator will email you within one business day with a final yes/no.',
            'You do not need to resend unless we ask.',
        ]
    elif media_hint and media_hint.get('routing') == 'reject':
        outcome = RECEIVED_NOT_OK
        ok = False
        title = f'We could not accept your {_item_label(item)} (case {cid})'
        summary = (
            'We received your file, but it did not pass our basic format checks. '
            'Please resend using JPEG, PNG, PDF, or plain text.'
        )
        next_steps = [
            'Resend a clear photo or document using a supported format.',
            'Optional: use the secure upload link from our earlier email.',
        ]
    elif media_hint and media_hint.get('routing') == 'human_review' and media_hint.get('quality_signals'):
        outcome = RECEIVED_NOT_OK
        ok = False
        title = f'Your {_item_label(item)} needs a clearer copy (case {cid})'
        summary = (
            'We received your submission, but image quality or format needs improvement '
            'before we can use it for your repair quote.'
        )
        next_steps = [
            'Send a brighter, in-focus photo showing the full appliance and fault area.',
            'Minimum suggested size: 320×240 pixels; avoid HEIC unless converted to JPEG.',
        ]
    else:
        outcome = RECEIVED_OK
        ok = True
        title = f'We received your {_item_label(item)} — OK (case {cid})'
        summary = (
            'Thank you — your submission is on file and passed our initial checks. '
            'Our team will use it for the next step on your repair.'
        )
        next_steps = [
            'No action needed unless we contact you for more detail.',
            f'Request reference: {rid}.',
        ]

    quality = _quality_from_media(media_hint)
    if outcome == RECEIVED_OK and not quality['accepted'] and media_hint:
        outcome = RECEIVED_NOT_OK
        ok = False

    payload: dict[str, Any] = {
        'schema_version': SCHEMA_VERSION,
        'request_id': rid,
        'case_id': cid,
        'item': item,
        'ok': ok,
        'receipt_outcome': outcome,
        'message': {
            'title': title,
            'summary': summary,
            'locale': 'en-IN',
        },
        'receipt': {
            'status_on_file': req_status or 'received',
            'received_at': received_at or None,
            'triage_disposition': disposition,
            'triage_reason': triage_reason or None,
        },
        'quality': quality,
        'next_steps': next_steps,
        'meta': {
            'dry_run': True,
            'channel': channel,
            'contact': contact,
        },
    }
    return StructuredCustomerResponse(payload)


def build_media_rejection_acknowledgment(
    case_id: str,
    request_id: str,
    contact: str,
    media: dict,
) -> StructuredCustomerResponse:
    """Example structured not-OK when intake rejects or flags a customer upload."""
    item = 'fault_photo'
    payload = {
        'schema_version': SCHEMA_VERSION,
        'request_id': request_id,
        'case_id': case_id,
        'item': item,
        'ok': False,
        'receipt_outcome': RECEIVED_NOT_OK,
        'message': {
            'title': f'Please resend your photo (case {case_id})',
            'summary': (
                f"We could not auto-accept `{media.get('filename', 'upload')}`: "
                f"{media.get('handling', 'See quality notes.')}"
            ),
            'locale': 'en-IN',
        },
        'receipt': {
            'status_on_file': 'pending',
            'received_at': None,
            'triage_disposition': 'n/a',
            'triage_reason': 'intake_quality_gate',
        },
        'quality': _quality_from_media(media),
        'next_steps': [
            'Resend as JPEG or PNG with the full appliance visible.',
            media.get('handling', 'Contact coordinator if you cannot convert HEIC/unknown files.'),
        ],
        'meta': {
            'dry_run': True,
            'channel': 'email',
            'contact': contact,
            'sample_filename': media.get('filename'),
        },
    }
    return StructuredCustomerResponse(payload)


def build_all_submission_acknowledgments(
    cases: list[dict],
    requests: list[dict],
    triage: list[RowResult],
) -> list[StructuredCustomerResponse]:
    cases_by_id = {c['case_id']: c for c in cases}
    triage_by_id = {r.request_id: r for r in triage}
    out: list[StructuredCustomerResponse] = []
    for req in sorted(requests, key=lambda r: r['request_id']):
        case = cases_by_id.get(req['case_id'])
        if not case:
            continue
        ack = build_submission_acknowledgment(
            case,
            req,
            triage_by_id.get(req['request_id']),
        )
        if ack:
            out.append(ack)
    return out


def build_demo_intake_not_ok_examples(media_checks: list[dict]) -> list[StructuredCustomerResponse]:
    """Teaching examples from demo media pack — structured not-OK templates."""
    examples: list[StructuredCustomerResponse] = []
    for i, media in enumerate(media_checks):
        if media.get('routing') == 'auto_queue' and not media.get('quality_signals'):
            continue
        examples.append(
            build_media_rejection_acknowledgment(
                case_id=f'C-DEMO-{i + 1:02d}',
                request_id=f'R-DEMO-{i + 1:02d}',
                contact=f'demo-{i + 1}@example.invalid',
                media=media,
            )
        )
    return examples


def summarize_acknowledgments(responses: list[StructuredCustomerResponse]) -> str:
    ok_n = sum(1 for r in responses if r.ok)
    not_ok = sum(1 for r in responses if not r.ok)
    return f'structured_acks={len(responses)} ok={ok_n} not_ok_or_review={not_ok}'
