import copy
import unittest

from data_policy import validate_all, validate_requests
from starter import load_inputs


class DataPolicyTests(unittest.TestCase):
    def test_pack_data_has_no_blocking_errors(self):
        inputs = load_inputs()
        report = validate_all(inputs['cases'], inputs['requests'], inputs['events'])
        self.assertTrue(report['ok_to_run_pipeline'])

    def test_invalid_status_is_error(self):
        inputs = copy.deepcopy(load_inputs())
        inputs['cases'][0]['status'] = 'not_a_status'
        report = validate_all(inputs['cases'], inputs['requests'], inputs['events'])
        self.assertFalse(report['ok_to_run_pipeline'])

    def test_bad_contact_domain_policy(self):
        case_ids = {c['case_id'] for c in load_inputs()['cases']}
        rows = [
            {
                'request_id': 'RX',
                'case_id': 'C009',
                'item': 'fault_photo',
                'status': 'pending',
                'followup_allowed': '1',
                'contact_address': 'bad@gmail.com',
                'channel': 'email',
            }
        ]
        findings = validate_requests(rows, case_ids)
        self.assertTrue(any(f.severity == 'policy' and f.field == 'contact_address' for f in findings))

    def test_pending_with_received_is_policy_conflict(self):
        inputs = load_inputs()
        report = validate_all(inputs['cases'], inputs['requests'], inputs['events'])
        self.assertTrue(
            any(
                f['field'] == 'status+received_at'
                for f in report['findings']
                if f['severity'] == 'policy'
            )
        )


if __name__ == '__main__':
    unittest.main()
