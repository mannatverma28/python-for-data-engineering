import unittest

from exercises import SAMPLE_EXERCISES, find_exercise, group_by_muscle, is_safe, pick_safe


def make(name, group, intensity, duration):
    return {"name": name, "muscle_group": group, "intensity": intensity, "duration": duration}


class TestSafety(unittest.TestCase):
    def test_normal_exercise_is_safe(self):
        self.assertTrue(is_safe(make("Squats", "Legs", 3, 20)))

    def test_limits_are_still_safe(self):
        self.assertTrue(is_safe(make("Hard", "Legs", 4, 45)))
        self.assertTrue(is_safe(make("Easy", "Legs", 1, 1)))

    def test_intensity_five_is_unsafe(self):
        self.assertFalse(is_safe(make("Burpees", "Chest", 5, 15)))

    def test_intensity_below_one_is_unsafe(self):
        self.assertFalse(is_safe(make("Odd", "Chest", 0, 15)))

    def test_long_duration_is_unsafe(self):
        self.assertFalse(is_safe(make("Run", "Legs", 2, 46)))

    def test_zero_duration_is_unsafe(self):
        self.assertFalse(is_safe(make("Nothing", "Legs", 2, 0)))

    def test_pick_safe_drops_burpees_from_sample(self):
        names = [ex["name"] for ex in pick_safe(SAMPLE_EXERCISES)]
        self.assertEqual(names, ["Squats", "Lunges", "Push-ups", "Rows", "Plank"])

    def test_pick_safe_does_not_change_input(self):
        data = [make("A", "Legs", 5, 10)]
        pick_safe(data)
        self.assertEqual(len(data), 1)


class TestGrouping(unittest.TestCase):
    def test_groups_sample_by_muscle(self):
        groups = group_by_muscle(SAMPLE_EXERCISES)
        self.assertEqual(list(groups.keys()), ["Legs", "Chest", "Back", "Core"])
        self.assertEqual([ex["name"] for ex in groups["Legs"]], ["Squats", "Lunges"])

    def test_empty_list_gives_empty_dict(self):
        self.assertEqual(group_by_muscle([]), {})


class TestFindExercise(unittest.TestCase):
    def test_finds_by_exact_name(self):
        self.assertEqual(find_exercise(SAMPLE_EXERCISES, "Rows")["muscle_group"], "Back")

    def test_ignores_case_and_spaces(self):
        self.assertIsNotNone(find_exercise(SAMPLE_EXERCISES, "  push-UPS "))

    def test_unknown_returns_none(self):
        self.assertIsNone(find_exercise(SAMPLE_EXERCISES, "Deadlift"))


if __name__ == "__main__":
    unittest.main()