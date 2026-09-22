import copy
import unittest

from customer_registry import canonical_contact, is_spam_or_fake, verify_customers
from starter import load_inputs


class CustomerRegistryTests(unittest.TestCase):
    def test_pack_data_all_verified_none_discarded(self):
        inputs = load_inputs()
        report = verify_customers(inputs['cases'], inputs['requests'])
        self.assertEqual(report['discarded_request_count'], 0)
        self.assertEqual(len(report['requests_for_automation']), 30)

    def test_unknown_case_discarded(self):
        inputs = load_inputs()
        rows = copy.deepcopy(inputs['requests'])
        rows[0]['case_id'] = 'C999'
        report = verify_customers(inputs['cases'], rows)
        self.assertIn(rows[0]['request_id'], report['discarded_request_ids'])

    def test_fake_domain_discarded(self):
        inputs = load_inputs()
        rows = copy.deepcopy(inputs['requests'])
        rows[0]['contact_address'] = 'case-001@mailinator.com'
        report = verify_customers(inputs['cases'], rows)
        self.assertIn(rows[0]['request_id'], report['discarded_request_ids'])
        spam, _ = is_spam_or_fake('case-001@mailinator.com', rows[0]['case_id'])
        self.assertTrue(spam)

    def test_mismatched_contact_discarded(self):
        spam, reason = is_spam_or_fake('case-999@example.invalid', 'C001')
        self.assertTrue(spam)
        self.assertIn('does not match', reason)

    def test_canonical_contact_format(self):
        self.assertEqual(canonical_contact('C009'), 'case-009@example.invalid')


if __name__ == '__main__':
    unittest.main()
