"""Verify requesters exist in the case register and discard spam/fake contacts."""
from __future__ import annotations

import re
from dataclasses import dataclass


SPAM_LOCAL_PART = re.compile(
    r'(spam|fake|test123|lottery|winner|crypto|noreply-no-reply)|^admin$|^root$',
    re.I,
)
FAKE_DOMAINS = frozenset(
    {
        'mailinator.com',
        'tempmail.com',
        'guerrillamail.com',
        '10minutemail.com',
        'yopmail.com',
    }
)
VALID_DOMAIN = 'example.invalid'


@dataclass(frozen=True)
class CustomerCheck:
    request_id: str
    case_id: str
    contact_address: str
    status: str  # verified | discarded
    reason: str


def canonical_contact(case_id: str) -> str:
    digits = ''.join(ch for ch in case_id if ch.isdigit())
    num = int(digits) if digits else 0
    return f'case-{num:03d}@{VALID_DOMAIN}'.lower()


def _contact_matches_case(contact: str, case_id: str) -> bool:
    contact = contact.lower().strip()
    if contact == canonical_contact(case_id):
        return True
    # Allow same numeric id in local part: case-009@ for C009
    digits = ''.join(ch for ch in case_id if ch.isdigit())
    if digits and f'case-{int(digits):03d}@' in contact:
        return contact.endswith(f'@{VALID_DOMAIN}')
    return False


def is_spam_or_fake(contact: str, case_id: str) -> tuple[bool, str]:
    c = (contact or '').strip().lower()
    if not c:
        return False, ''
    if '@' not in c:
        return True, 'contact is not a valid email shape'
    local, _, domain = c.partition('@')
    if domain in FAKE_DOMAINS:
        return True, f'disposable/spam domain {domain}'
    if domain != VALID_DOMAIN:
        return True, f'non-register domain {domain} (expected {VALID_DOMAIN})'
    if SPAM_LOCAL_PART.search(local):
        return True, 'spam-like local part in contact address'
    if not _contact_matches_case(c, case_id):
        return True, f'contact does not match registered case id {case_id}'
    return False, ''


def verify_customers(cases: list[dict], requests: list[dict]) -> dict:
    """
    Ensure each request references a known case and contact belongs to that case.
    Returns filtered requests safe for automation plus discarded spam/unverified rows.
    """
    case_ids = {(c.get('case_id') or '').strip() for c in cases}
    case_ids.discard('')

    checks: list[CustomerCheck] = []
    kept: list[dict] = []
    discarded_ids: list[str] = []

    for req in requests:
        rid = (req.get('request_id') or '').strip()
        cid = (req.get('case_id') or '').strip()
        contact = (req.get('contact_address') or '').strip()

        if cid not in case_ids:
            checks.append(
                CustomerCheck(rid, cid, contact, 'discarded', 'case_id not in register')
            )
            discarded_ids.append(rid)
            continue

        spam, why = is_spam_or_fake(contact, cid)
        if spam:
            checks.append(CustomerCheck(rid, cid, contact, 'discarded', why))
            discarded_ids.append(rid)
            continue

        if not contact:
            checks.append(
                CustomerCheck(
                    rid,
                    cid,
                    contact,
                    'verified',
                    'no contact on file — automation blocked elsewhere',
                )
            )
            kept.append(req)
            continue

        checks.append(
            CustomerCheck(rid, cid, contact, 'verified', 'matches case register')
        )
        kept.append(req)

    verified_count = sum(1 for c in checks if c.status == 'verified')
    return {
        'verified_request_count': verified_count,
        'discarded_request_count': len(discarded_ids),
        'discarded_request_ids': discarded_ids,
        'checks': [c.__dict__ for c in checks],
        'requests_for_automation': kept,
    }


def summarize_customer_verification(report: dict) -> str:
    return (
        f"verified={report['verified_request_count']} "
        f"discarded={report['discarded_request_count']} "
        f"spam_or_unknown={report['discarded_request_ids'][:5]}"
        f"{'...' if len(report['discarded_request_ids']) > 5 else ''}"
    )
