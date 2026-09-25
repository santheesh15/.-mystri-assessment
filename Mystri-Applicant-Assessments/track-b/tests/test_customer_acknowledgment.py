import unittest

from customer_acknowledgment import (
    RECEIVED_OK,
    UNDER_REVIEW,
    build_all_submission_acknowledgments,
    build_submission_acknowledgment,
)
from queue_engine import RowResult, triage_all
from starter import load_inputs


class CustomerAcknowledgmentTests(unittest.TestCase):
    def test_received_row_structured_ok(self):
        case = {'case_id': 'C002', 'status': 'waiting_info', 'service_type': 'washing_machine'}
        request = {
            'request_id': 'R002',
            'case_id': 'C002',
            'item': 'fault_photo',
            'status': 'received',
            'received_at': '2026-08-24T18:00+05:30',
            'contact_address': 'case-002@example.invalid',
            'channel': 'email',
        }
        row = RowResult('R002', 'C002', 'fault_photo', 'exclude', 'Item already received')
        ack = build_submission_acknowledgment(case, request, row)
        self.assertIsNotNone(ack)
        self.assertTrue(ack.ok)
        self.assertEqual(ack.payload['receipt_outcome'], RECEIVED_OK)
        self.assertEqual(ack.payload['schema_version'], 'daybreak.customer_ack.v1')
        self.assertIn('next_steps', ack.payload)

    def test_conflicting_pending_received_under_review(self):
        case = {'case_id': 'C018', 'status': 'waiting_info', 'service_type': 'air_conditioner'}
        request = {
            'request_id': 'R018',
            'case_id': 'C018',
            'item': 'fault_photo',
            'status': 'pending',
            'received_at': '2026-09-01T10:00+05:30',
            'contact_address': 'case-018@example.invalid',
            'channel': 'email',
        }
        row = RowResult(
            'R018',
            'C018',
            'fault_photo',
            'uncertain',
            'pending status conflicts with received_at; needs coordinator review',
        )
        ack = build_submission_acknowledgment(case, request, row)
        self.assertIsNotNone(ack)
        self.assertFalse(ack.ok)
        self.assertEqual(ack.payload['receipt_outcome'], UNDER_REVIEW)

    def test_pending_without_receipt_skipped(self):
        case = {'case_id': 'C009', 'status': 'waiting_info', 'service_type': 'washing_machine'}
        request = {
            'request_id': 'R009',
            'case_id': 'C009',
            'item': 'fault_photo',
            'status': 'pending',
            'received_at': '',
            'contact_address': 'case-009@example.invalid',
            'channel': 'email',
        }
        self.assertIsNone(build_submission_acknowledgment(case, request, None))

    def test_pack_data_builds_multiple_acks(self):
        inputs = load_inputs()
        triage = triage_all(inputs['cases'], inputs['requests'], inputs['scenario'])
        acks = build_all_submission_acknowledgments(inputs['cases'], inputs['requests'], triage)
        self.assertGreaterEqual(len(acks), 10)
        self.assertTrue(any(a.ok for a in acks))
        self.assertTrue(any(not a.ok for a in acks))


if __name__ == '__main__':
    unittest.main()
