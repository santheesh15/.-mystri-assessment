import unittest

from team_workboard import TASK_WORK_LEVEL, assign_by_hierarchy, build_team_board, TECH_ROSTER
from starter import load_inputs
from queue_engine import triage_all


class HierarchyTests(unittest.TestCase):
    def test_level4_task_goes_to_senior_rank(self):
        from team_workboard import TeamTask

        tasks = assign_by_hierarchy(
            [
                TeamTask(
                    'technician',
                    '',
                    'C999',
                    'human_photo_quality_check',
                    'test',
                    ('R1',),
                    TASK_WORK_LEVEL['human_photo_quality_check'],
                )
            ]
        )
        owner = tasks[0].owner
        rank = next(t['rank'] for t in TECH_ROSTER if t['id'] == owner)
        self.assertGreaterEqual(rank, 4)

    def test_load_spreads_across_apprentices(self):
        from team_workboard import TeamTask

        many = [
            TeamTask('technician', '', f'C{i:03d}', 'standby_case_brief', 'test', (), 1)
            for i in range(1, 9)
        ]
        assigned = assign_by_hierarchy(many)
        owners = {t.owner for t in assigned}
        self.assertGreater(len(owners), 1)

    def test_board_includes_hierarchy_metadata(self):
        inputs = load_inputs()
        triage = triage_all(inputs['cases'], inputs['requests'], inputs['scenario'])
        board = build_team_board(inputs['cases'], inputs['requests'], inputs['scenario'], triage)
        self.assertIn('technician_hierarchy', board)
        self.assertIn('work_level', board['technician_tasks'][0])


if __name__ == '__main__':
    unittest.main()
