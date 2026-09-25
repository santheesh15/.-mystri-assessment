"""Single-file audit trace for the full Track B pipeline (dry-run)."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


class PipelineTrace:
    def __init__(self, snapshot_at: str, scenario_note: str = 'dry_run_only') -> None:
        self.snapshot_at = snapshot_at
        self.scenario_note = scenario_note
        self._seq = 0
        self.lines: list[str] = []
        self.log('START', 'Track B DICM pipeline run begins', f'snapshot={snapshot_at}')
        self.log('START', 'Assessment mode', scenario_note)

    def log(self, phase: str, message: str, detail: str = '') -> None:
        self._seq += 1
        stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        extra = f' detail={detail}' if detail else ''
        self.lines.append(
            f'{stamp} seq={self._seq:04d} phase={phase} message={message}{extra}'
        )

    def log_many(self, phase: str, prefix: str, items: list[str]) -> None:
        for item in items:
            self.log(phase, prefix, item)

    def log_structured_acknowledgments(self, acknowledgments: list) -> None:
        """Log dry-run structured receipt responses (OK / not OK / under review)."""
        if not acknowledgments:
            self.log('CUSTOMER_ACK', 'No submission receipts to confirm in this run')
            return
        for ack in acknowledgments:
            payload = ack.payload
            self.log(
                'CUSTOMER_ACK',
                'DRY-RUN structured receipt to customer (no real send)',
                (
                    f"request_id={payload['request_id']} case_id={payload['case_id']} "
                    f"ok={payload['ok']} outcome={payload['receipt_outcome']} "
                    f"to={payload['meta']['contact']} channel={payload['meta']['channel']}"
                ),
            )
            self.log(
                'CUSTOMER_ACK',
                'Structured JSON body',
                ack.to_json().replace('\n', ' '),
            )

    def finish_customer_delivery(
        self,
        deliveries: list[dict],
        *,
        structured_ack_count: int = 0,
    ) -> None:
        if not deliveries:
            self.log('CUSTOMER', 'No eligible follow-ups to deliver in this run')
        for d in deliveries:
            self.log(
                'CUSTOMER',
                'DRY-RUN delivery simulated (no real email sent)',
                (
                    f"request_id={d['request_id']} case_id={d['case_id']} "
                    f"to={d['contact']} channel={d.get('channel', 'email')} "
                    f"coordinator_approval=simulated_yes item={d.get('item', '')}"
                ),
            )
        self.log(
            'END',
            'Pipeline trace complete',
            f'structured_receipt_acks={structured_ack_count} followup_deliveries_simulated={len(deliveries)}',
        )

    def write(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        header = [
            '# Daybreak Track B — unified pipeline trace',
            f'# Business snapshot clock: {self.snapshot_at}',
            '# Format: UTC timestamp | seq | phase | message | optional detail',
            '',
        ]
        path.write_text('\n'.join(header + self.lines) + '\n', encoding='utf-8')
        return path


def build_customer_deliveries(triage, requests_by_id: dict, ai_drafts_by_case: dict) -> list[dict]:
    """Map proposed follow-ups to contacts for end-of-trace customer delivery lines."""
    out: list[dict] = []
    for row in triage:
        if row.disposition != 'propose':
            continue
        req = requests_by_id.get(row.request_id, {})
        contact = req.get('contact_address') or f"{row.case_id.lower()}@example.invalid"
        out.append(
            {
                'request_id': row.request_id,
                'case_id': row.case_id,
                'item': row.item,
                'contact': contact,
                'channel': req.get('channel', 'email'),
                'draft_preview': (ai_drafts_by_case.get(row.case_id) or '')[:120],
            }
        )
    return out
