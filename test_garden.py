import io
import unittest
from unittest.mock import patch

import garden


class DaysUntilWateringTests(unittest.TestCase):
    def test_example_from_the_task(self):
        self.assertEqual(garden.days_until_watering(2, 5), 3)

    def test_watered_today_waits_a_full_interval(self):
        self.assertEqual(garden.days_until_watering(0, 4), 4)

    def test_schedule_repeats_after_a_full_interval(self):
        self.assertEqual(garden.days_until_watering(7, 5), 3)

    def test_zero_interval_raises_zero_division_error(self):
        with self.assertRaises(ZeroDivisionError):
            garden.days_until_watering(3, 0)


class WaterAllTests(unittest.TestCase):
    def run_water_all(self, plants):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            garden.water_all(plants)
        return fake_out.getvalue()

    def test_prints_a_reminder_for_each_plant(self):
        output = self.run_water_all([
            {"name": "Tomato", "last_watered": 2, "interval": 5},
            {"name": "Basil", "last_watered": 1, "interval": 2},
        ])
        self.assertEqual(output, "Water Tomato in 3 days.\nWater Basil in 1 days.\n")

    def test_zero_interval_prints_message_and_keeps_going(self):
        output = self.run_water_all([
            {"name": "Cactus", "last_watered": 3, "interval": 0},
            {"name": "Fern", "last_watered": 1, "interval": 3},
        ])
        self.assertEqual(
            output,
            "Cannot calculate watering for Cactus: interval cannot be zero.\n"
            "Water Fern in 2 days.\n",
        )


class AskForPlantTests(unittest.TestCase):
    def test_valid_interval_becomes_an_integer(self):
        with patch("builtins.input", side_effect=["Mint", "3"]):
            plant = garden.ask_for_plant()
        self.assertEqual(plant, {"name": "Mint", "last_watered": 0, "interval": 3})

    def test_invalid_interval_prints_message(self):
        with patch("builtins.input", side_effect=["Mint", "abc"]):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                plant = garden.ask_for_plant()
        self.assertIsNone(plant)
        self.assertEqual(fake_out.getvalue(), "Invalid interval\n")


if __name__ == "__main__":
    unittest.main()