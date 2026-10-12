import io
import unittest
from contextlib import redirect_stdout

import main


class TestSampleRun(unittest.TestCase):
    def test_sample_run_output(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main.main()
        output = buffer.getvalue()
        self.assertIn("Skipped as unsafe for beginners: Burpees", output)
        self.assertIn("Wednesday  Rest", output)
        self.assertIn("Total weekly intensity: 42 (Moderate)", output)
        self.assertIn("Logged: Squats on 2026-10-13 for 25 min", output)
        self.assertIn("Invalid log: duration 150 is over 120 minutes", output)
        self.assertIn("Saved logs: 1", output)


if __name__ == "__main__":
    unittest.main()