import json
import unittest
from pathlib import Path

TRACK_B = Path(__file__).resolve().parent.parent


class Product1GateTests(unittest.TestCase):
    def test_manifest_and_product1_readme_exist(self):
        self.assertTrue((TRACK_B / 'product1' / 'MANIFEST.json').is_file())
        self.assertTrue((TRACK_B / 'product1' / 'README.md').is_file())
        self.assertTrue((TRACK_B / 'PROJECT_README.md').is_file())
        self.assertTrue((TRACK_B / 'docs' / 'SETUP.md').is_file())
        self.assertTrue((TRACK_B / 'docs' / 'RULES_AND_LIMITATIONS.md').is_file())

    def test_manifest_lists_core_modules(self):
        manifest = json.loads((TRACK_B / 'product1' / 'MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['product_id'], 'product1')
        self.assertIn('queue_engine.py', manifest['python_modules'])
        self.assertIn('customer_acknowledgment.py', manifest['python_modules'])
        self.assertTrue(manifest['dry_run_only'])


if __name__ == '__main__':
    unittest.main()
