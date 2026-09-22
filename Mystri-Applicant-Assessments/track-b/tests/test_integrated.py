import unittest

from integrated_model import run_integrated_pipeline
from starter import load_inputs


class IntegratedModelTests(unittest.TestCase):
    def test_pipeline_produces_collaboration_flow(self):
        inputs = load_inputs()
        report = run_integrated_pipeline(inputs['cases'], inputs['requests'], inputs['scenario'])
        self.assertEqual(report['name'], 'Daybreak Integrated Collaborating Model (DICM)')
        self.assertEqual(len(report['collaboration_flow']), 6)
        self.assertIn('team_workboard', report)
        self.assertIn('cost_structure', report)
        self.assertIn('ai_assist', report)
        self.assertIn('lane_counts', report)

    def test_prevented_bad_reminders_non_empty_on_pack(self):
        inputs = load_inputs()
        report = run_integrated_pipeline(inputs['cases'], inputs['requests'], inputs['scenario'])
        self.assertGreater(len(report['comparison']['prevented_bad_reminders']), 0)


if __name__ == '__main__':
    unittest.main()
