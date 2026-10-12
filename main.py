"""FitPlan sample run: plan a week for one member and check two workout logs."""

from exercises import SAMPLE_EXERCISES, is_safe
from planner import build_plan, format_plan, intensity_label, total_intensity
from workout_log import log_workout

DAYS_PER_WEEK = 4
WEEK_START = "2026-10-12"  # the Monday of the week being planned

SAMPLE_LOGS = [
    {"date": "2026-10-13", "exercise": "Squats", "duration": 25},
    {"date": "2026-10-14", "exercise": "Push-ups", "duration": 150},
]


def main():
    print("=== FitPlan ===")
    print(f"Week starting {WEEK_START}, {DAYS_PER_WEEK} training days")
    print()

    skipped = [ex["name"] for ex in SAMPLE_EXERCISES if not is_safe(ex)]
    print(f"Exercises given: {len(SAMPLE_EXERCISES)}")
    print(f"Skipped as unsafe for beginners: {', '.join(skipped) or 'none'}")
    print()

    plan = build_plan(SAMPLE_EXERCISES, DAYS_PER_WEEK)
    print("Weekly plan:")
    for line in format_plan(plan):
        print("  " + line)
    print()

    total = total_intensity(plan)
    print(f"Total weekly intensity: {total} ({intensity_label(total)})")
    print()

    print("Workout logs:")
    logbook = []
    for log in SAMPLE_LOGS:
        print("  " + log_workout(log, SAMPLE_EXERCISES, WEEK_START, logbook))
    print(f"Saved logs: {len(logbook)}")


if __name__ == "__main__":
    main()

