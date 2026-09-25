import unittest

from ai_assist import classify_customer_reply, draft_reminder_email, photo_screening_decision
from cost_model import build_cost_structure


class AiAssistTests(unittest.TestCase):
    def test_draft_requires_human_gate(self):
        s = draft_reminder_email(
            {'case_id': 'C009', 'service_type': 'washing_machine'},
            'fault_photo',
            'test@example.invalid',
        )
        self.assertIn('approve', s.human_gate.lower())

    def test_opt_out_detection(self):
        s = classify_customer_reply('Please stop emailing me', 'C012')
        self.assertIn('opt_out', s.suggestion)

    def test_photo_never_auto_approved(self):
        s = photo_screening_decision('C001', has_conflict=False)
        self.assertIn('human', s.human_gate.lower())

    def test_cost_structure_has_net_saved(self):
        metrics = {
            'baseline_all_work_on_coordinator': 19,
            'coordinator_tasks_after_split': 8,
            'technician_tasks': [{}] * 8,
            'uncertain_count': 2,
            'ai_draft_count': 5,
        }
        cost = build_cost_structure({'monthly_tool_budget_inr': 1500}, metrics)
        self.assertIn('net_saved', cost['time_minutes_per_week'])


if __name__ == '__main__':
    unittest.main()
