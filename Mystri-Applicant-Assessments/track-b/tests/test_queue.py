"""Verification checks for the follow-up queue experiment."""
import copy
import json
import unittest
from pathlib import Path

from starter import load_inputs
from queue_engine import baseline_naive_pending, proposed_ids, triage_all


DATA = Path(__file__).resolve().parent.parent / 'data'


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.inputs = load_inputs()

    def test_no_action_when_all_requests_received(self):
        inputs = copy.deepcopy(self.inputs)
        for req in inputs['requests']:
            req['status'] = 'received'
            req['received_at'] = '2026-09-01T10:00:00+05:30'
        results = triage_all(inputs['cases'], inputs['requests'], inputs['scenario'])
        self.assertEqual(proposed_ids(results), set())
        self.assertGreater(sum(1 for r in results if r.disposition == 'exclude'), 0)

    def test_followup_not_allowed_excluded(self):
        results = triage_all(self.inputs['cases'], self.inputs['requests'], self.inputs['scenario'])
        r012 = next(r for r in results if r.request_id == 'R012')
        self.assertEqual(r012.disposition, 'exclude')
        self.assertIn('followup_allowed', r012.reason)

    def test_conflicting_pending_and_received_is_uncertain(self):
        results = triage_all(self.inputs['cases'], self.inputs['requests'], self.inputs['scenario'])
        r018 = next(r for r in results if r.request_id == 'R018')
        self.assertEqual(r018.disposition, 'uncertain')

    def test_changed_input_blocks_recent_request(self):
        inputs = copy.deepcopy(self.inputs)
        req = next(r for r in inputs['requests'] if r['request_id'] == 'R009')
        req['last_requested_at'] = '2026-09-07T08:00:00+05:30'
        results = triage_all(inputs['cases'], inputs['requests'], inputs['scenario'])
        r009 = next(r for r in results if r.request_id == 'R009')
        self.assertEqual(r009.disposition, 'exclude')
        self.assertIn('48', r009.reason)

    def test_rerun_is_stable(self):
        first = triage_all(self.inputs['cases'], self.inputs['requests'], self.inputs['scenario'])
        second = triage_all(self.inputs['cases'], self.inputs['requests'], self.inputs['scenario'])
        self.assertEqual([r.__dict__ for r in first], [r.__dict__ for r in second])

    def test_baseline_contacts_more_than_rules_on_pack_data(self):
        baseline = baseline_naive_pending(self.inputs['requests'])
        rules = proposed_ids(triage_all(self.inputs['cases'], self.inputs['requests'], self.inputs['scenario']))
        self.assertGreater(len(baseline), len(rules))


if __name__ == '__main__':
    unittest.main()
