import unittest
from pathlib import Path

from integrated_model import run_and_write_trace
from starter import load_inputs


class PipelineTraceTests(unittest.TestCase):
    def test_trace_file_written_end_to_end(self):
        inputs = load_inputs()
        trace_path = Path(__file__).resolve().parent / 'output_test_trace.log'
        if trace_path.exists():
            trace_path.unlink()
        report = run_and_write_trace(
            inputs['cases'],
            inputs['requests'],
            inputs['scenario'],
            inputs['events'],
            trace_path,
        )
        self.assertTrue(trace_path.exists())
        text = trace_path.read_text(encoding='utf-8')
        self.assertIn('START', text)
        self.assertIn('DRY-RUN delivery simulated', text)
        self.assertIn('END', text)
        self.assertGreaterEqual(len(report['customer_delivery_simulation']), 1)
        trace_path.unlink()


if __name__ == '__main__':
    unittest.main()
