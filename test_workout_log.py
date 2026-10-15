import unittest

from exercises import SAMPLE_EXERCISES
from workout_log import InvalidLogError, log_workout, validate_log, week_dates

WEEK = "2026-10-12"


def entry(date, exercise, duration):
    return {"date": date, "exercise": exercise, "duration": duration}


class TestValidateLog(unittest.TestCase):
    def test_valid_entry_passes(self):
        validate_log(entry("2026-10-13", "Squats", 25), SAMPLE_EXERCISES, WEEK)

    def test_first_and_last_day_of_week_pass(self):
        validate_log(entry("2026-10-12", "Rows", 10), SAMPLE_EXERCISES, WEEK)
        validate_log(entry("2026-10-18", "Rows", 120), SAMPLE_EXERCISES, WEEK)

    def test_unknown_exercise(self):
        with self.assertRaises(InvalidLogError) as caught:
            validate_log(entry("2026-10-13", "Deadlift", 20), SAMPLE_EXERCISES, WEEK)
        self.assertEqual(str(caught.exception), "unknown exercise 'Deadlift'")

    def test_duration_over_120(self):
        with self.assertRaises(InvalidLogError) as caught:
            validate_log(entry("2026-10-13", "Squats", 121), SAMPLE_EXERCISES, WEEK)
        self.assertEqual(str(caught.exception), "duration 121 is over 120 minutes")

    def test_zero_duration(self):
        with self.assertRaises(InvalidLogError):
            validate_log(entry("2026-10-13", "Squats", 0), SAMPLE_EXERCISES, WEEK)

    def test_date_before_week(self):
        with self.assertRaises(InvalidLogError) as caught:
            validate_log(entry("2026-10-11", "Squats", 20), SAMPLE_EXERCISES, WEEK)
        self.assertEqual(
            str(caught.exception), "2026-10-11 is not in this week (2026-10-12 to 2026-10-18)"
        )

    def test_date_after_week(self):
        with self.assertRaises(InvalidLogError):
            validate_log(entry("2026-10-19", "Squats", 20), SAMPLE_EXERCISES, WEEK)

    def test_badly_written_date(self):
        with self.assertRaises(InvalidLogError) as caught:
            validate_log(entry("13/10/2026", "Squats", 20), SAMPLE_EXERCISES, WEEK)
        self.assertEqual(str(caught.exception), "date '13/10/2026' is not in YYYY-MM-DD format")

    def test_week_dates(self):
        first, last = week_dates(WEEK)
        self.assertEqual((first.isoformat(), last.isoformat()), ("2026-10-12", "2026-10-18"))


class TestLogWorkout(unittest.TestCase):
    def test_valid_log_is_saved(self):
        logbook = []
        message = log_workout(entry("2026-10-13", "Squats", 25), SAMPLE_EXERCISES, WEEK, logbook)
        self.assertEqual(message, "Logged: Squats on 2026-10-13 for 25 min")
        self.assertEqual(len(logbook), 1)

    def test_invalid_log_is_reported_not_saved(self):
        logbook = []
        message = log_workout(entry("2026-10-14", "Push-ups", 150), SAMPLE_EXERCISES, WEEK, logbook)
        self.assertEqual(message, "Invalid log: duration 150 is over 120 minutes")
        self.assertEqual(logbook, [])

    def test_unknown_exercise_message(self):
        message = log_workout(entry("2026-10-14", "Yoga", 30), SAMPLE_EXERCISES, WEEK, [])
        self.assertEqual(message, "Invalid log: unknown exercise 'Yoga'")


if __name__ == "__main__":
    unittest.main()