import unittest

from lane_model import classify_case_lane, duty_lead_for_snapshot, prioritized_board
from starter import load_inputs


class LaneModelTests(unittest.TestCase):
    def test_opt_out_case_parks(self):
        inputs = load_inputs()
        case = next(c for c in inputs['cases'] if c['case_id'] == 'C012')
        reqs = [r for r in inputs['requests'] if r['case_id'] == 'C012']
        lane = classify_case_lane(case, reqs)
        self.assertEqual(lane['lane'], 'park')

    def test_departure_board_sorted(self):
        inputs = load_inputs()
        board = prioritized_board(inputs['cases'], inputs['requests'], inputs['scenario']['snapshot_at'])
        scores = [r['priority_score'] for r in board]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_duty_lead_rotates(self):
        a = duty_lead_for_snapshot('2026-09-07T09:00:00+05:30')
        b = duty_lead_for_snapshot('2026-09-14T09:00:00+05:30')
        self.assertIn(a['duty_lead'], {'T1', 'T2'})
        self.assertNotEqual(a['iso_week'], b['iso_week'])


if __name__ == '__main__':
    unittest.main()
