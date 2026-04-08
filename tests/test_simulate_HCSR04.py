import unittest
from unittest.mock import patch, MagicMock
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from Simulate_HCSR04 import HCSR04


class TestHCSR04(unittest.TestCase):

    def setUp(self):
        self.s = HCSR04()

    @patch.object(HCSR04, '_simulate_pulse', return_value=50.0)
    def test_measure(self, _):
        self.assertAlmostEqual(self.s.measure(), 50.0, delta=0.1)

    @patch.object(HCSR04, '_simulate_pulse', return_value=2.0)
    def test_outlier_none(self, _):
        self.assertIsNone(self.s.measure())

    @patch.object(HCSR04, '_simulate_pulse', side_effect=[50.0, 2.0])
    def test_outlier_last_valid(self, _):
        self.s.measure()
        self.assertIsNotNone(self.s.measure())

    @patch.object(HCSR04, 'measure', return_value=10.0)
    def test_status_critical(self, _):
        self.assertEqual(self.s.get_obstacle_status(15.0), "critical")

    @patch.object(HCSR04, 'measure', return_value=20.0)
    def test_status_warning(self, _):
        self.assertEqual(self.s.get_obstacle_status(15.0), "warning")

    @patch.object(HCSR04, 'measure', return_value=100.0)
    def test_status_clear(self, _):
        self.assertEqual(self.s.get_obstacle_status(15.0), "clear")

    def test_direction_forward(self):
        self.s.measure = MagicMock(return_value=100.0)
        direction, angle = self.s.get_best_direction(MagicMock(), MagicMock())
        self.assertEqual((direction, angle), ("forward", 0))

    def test_direction_left(self):
        self.s.measure = MagicMock(return_value=10.0)
        left, right = MagicMock(), MagicMock()
        left.measure.return_value = 80.0
        right.measure.return_value = 20.0
        direction, angle = self.s.get_best_direction(left, right)
        self.assertEqual(direction, "left")

    def test_direction_right(self):
        self.s.measure = MagicMock(return_value=10.0)
        left, right = MagicMock(), MagicMock()
        left.measure.return_value = 20.0
        right.measure.return_value = 80.0
        direction, angle = self.s.get_best_direction(left, right)
        self.assertEqual(direction, "right")

    def test_scan(self):
        left, right = MagicMock(), MagicMock()
        left.measure.return_value = 60.0
        right.measure.return_value = 80.0
        result = self.s.scan({"left": left, "right": right})
        self.assertEqual(result, {"left": 60.0, "right": 80.0})



if __name__ == '__main__':
    unittest.main()