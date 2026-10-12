import unittest

from exercises import SAMPLE_EXERCISES
from planner import (
    DAYS,
    build_plan,
    choose_training_days,
    format_plan,
    intensity_label,
    total_intensity,
)


class TestTrainingDays(unittest.TestCase):
    def test_four_days(self):
        self.assertEqual(choose_training_days(4), ["Monday", "Tuesday", "Thursday", "Saturday"])

    def test_three_days_alternate(self):
        self.assertEqual(choose_training_days(3), ["Monday", "Wednesday", "Friday"])

    def test_seven_days_is_every_day(self):
        self.assertEqual(choose_training_days(7), DAYS)

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            choose_training_days(0)
        with self.assertRaises(ValueError):
            choose_training_days(8)


class TestBuildPlan(unittest.TestCase):
    def setUp(self):
        self.plan = build_plan(SAMPLE_EXERCISES, 4)

    def test_plan_has_all_seven_days_in_order(self):
        self.assertEqual(list(self.plan.keys()), DAYS)

    def test_rest_on_non_training_days(self):
        rest_days = [day for day, workout in self.plan.items() if workout == "Rest"]
        self.assertEqual(rest_days, ["Wednesday", "Friday", "Sunday"])

    def test_every_training_day_covers_every_safe_group(self):
        for workout in self.plan.values():
            if workout != "Rest":
                groups = [ex["muscle_group"] for ex in workout]
                self.assertEqual(groups, ["Legs", "Chest", "Back", "Core"])

    def test_leg_exercises_take_turns(self):
        legs = [self.plan[day][0]["name"] for day in ["Monday", "Tuesday", "Thursday", "Saturday"]]
        self.assertEqual(legs, ["Squats", "Lunges", "Squats", "Lunges"])

    def test_unsafe_exercise_never_planned(self):
        for workout in self.plan.values():
            if workout != "Rest":
                self.assertNotIn("Burpees", [ex["name"] for ex in workout])

    def test_no_safe_exercises_raises(self):
        unsafe = [{"name": "Burpees", "muscle_group": "Chest", "intensity": 5, "duration": 15}]
        with self.assertRaises(ValueError):
            build_plan(unsafe, 3)


class TestIntensity(unittest.TestCase):
    def test_sample_total(self):
        self.assertEqual(total_intensity(build_plan(SAMPLE_EXERCISES, 4)), 42)

    def test_all_rest_is_zero(self):
        self.assertEqual(total_intensity({day: "Rest" for day in DAYS}), 0)

    def test_label_boundaries(self):
        self.assertEqual(intensity_label(0), "Light")
        self.assertEqual(intensity_label(39), "Light")
        self.assertEqual(intensity_label(40), "Moderate")
        self.assertEqual(intensity_label(80), "Moderate")
        self.assertEqual(intensity_label(81), "Intense")


class TestFormatPlan(unittest.TestCase):
    def test_lines(self):
        lines = format_plan(build_plan(SAMPLE_EXERCISES, 4))
        self.assertEqual(len(lines), 7)
        self.assertEqual(lines[0], "Monday     Squats, Push-ups, Rows, Plank (60 min)")
        self.assertEqual(lines[2], "Wednesday  Rest")


if __name__ == "__main__":
    unittest.main()