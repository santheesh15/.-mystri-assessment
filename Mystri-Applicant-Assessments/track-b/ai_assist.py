"""Dry-run AI assist layer — human approval required before any customer action."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AiSuggestion:
    step: str
    case_id: str
    suggestion: str
    confidence: str  # low | medium | high
    human_gate: str
    production_note: str


def draft_reminder_email(case: dict, item: str, contact: str) -> AiSuggestion:
    """Prototype: template stand-in for a small LLM draft. Coordinator edits before send."""
    name = case.get('service_type', 'appliance').replace('_', ' ')
    text = (
        f"Subject: Photo still needed for your {name} repair (case {case['case_id']})\n"
        f"To: {contact}\n\n"
        f"Hello,\n\n"
        f"Please reply to this email with the requested {item.replace('_', ' ')} "
        f"so we can prepare your quote.\n\n"
        f"Thank you,\nDaybreak Repairs"
    )
    return AiSuggestion(
        step='coordinator_customer_draft',
        case_id=case['case_id'],
        suggestion=text,
        confidence='medium',
        human_gate='Coordinator must edit/approve; never auto-send (assessment dry-run).',
        production_note='Replace template with approved LLM prompt + audit log.',
    )


def classify_customer_reply(detail: str, case_id: str) -> AiSuggestion:
    """Prototype: keyword classifier mimicking inbox triage AI. Human confirms CRM update."""
    text = (detail or '').lower()
    if any(w in text for w in ('photo attached', 'sent photo', 'image attached')):
        label = 'likely_photo_received'
        conf = 'medium'
    elif any(w in text for w in ('stop', 'do not contact', 'unsubscribe')):
        label = 'opt_out_language_detected'
        conf = 'high'
    else:
        label = 'unclear_reply'
        conf = 'low'
    return AiSuggestion(
        step='coordinator_inbox_triage',
        case_id=case_id,
        suggestion=f"Suggested label: {label}",
        confidence=conf,
        human_gate='Coordinator confirms before changing request status.',
        production_note='Use LLM only with retrieval over case history; default to uncertain.',
    )


def technician_prep_checklist(case: dict) -> AiSuggestion:
    """Prototype: structured checklist (deterministic) stand-in for technician copilot."""
    st = case.get('service_type', 'appliance')
    items = [
        f'Confirm typical parts list for {st}',
        'Check warranty/serial location on unit',
        'Note if quote needs site visit vs bench repair',
    ]
    return AiSuggestion(
        step='technician_parallel_prep',
        case_id=case['case_id'],
        suggestion='; '.join(items),
        confidence='high',
        human_gate='Technician validates checklist; no customer message.',
        production_note='Optional LLM summarises case note—technician still signs off.',
    )


def photo_screening_decision(case_id: str, has_conflict: bool) -> AiSuggestion:
    """AI never approves photo quality in this prototype — always human technician."""
    if has_conflict:
        msg = 'Data conflict on photo row — skip vision; coordinator reconciles inbox first.'
        conf = 'high'
    else:
        msg = 'If file present, route to technician human quality check (blur/angle/model).'
        conf = 'medium'
    return AiSuggestion(
        step='photo_quality_path',
        case_id=case_id,
        suggestion=msg,
        confidence=conf,
        human_gate='Technician human review mandatory; no auto-quote from image AI.',
        production_note='Future vision API may pre-sort, but quote gate stays human.',
    )


def enrich_coordinator_tasks(coordinator_tasks: list[dict], cases_by_id: dict) -> list[AiSuggestion]:
    out: list[AiSuggestion] = []
    for task in coordinator_tasks:
        if task.get('task') != 'draft_customer_followup':
            continue
        cid = task['case_id']
        case = cases_by_id.get(cid, {})
        rid = task.get('request_ids', ('',))[0]
        item = 'fault_photo'
        if 'site_access' in task.get('reason', ''):
            item = 'site_access'
        out.append(
            draft_reminder_email(case, item, f'{cid.lower()}@example.invalid')
        )
    return out
