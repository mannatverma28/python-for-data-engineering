"""Build a balanced 7-day workout plan and rate its weekly intensity."""

from exercises import group_by_muscle, pick_safe

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def choose_training_days(days_per_week):
    """Spread the training days across the week so rest days fall in between."""
    if days_per_week < 1 or days_per_week > 7:
        raise ValueError("days per week must be between 1 and 7")
    return [DAYS[i * 7 // days_per_week] for i in range(days_per_week)]


def build_plan(exercises, days_per_week):
    """Return a dictionary with all 7 days: a list of exercises, or 'Rest'.

    Every training day gets one exercise from each muscle group, so no group
    is skipped. Groups with several exercises take turns from day to day.
    """
    groups = group_by_muscle(pick_safe(exercises))
    if not groups:
        raise ValueError("no safe exercises to plan with")
    training_days = choose_training_days(days_per_week)

    plan = {}
    session = 0
    for day in DAYS:
        if day in training_days:
            plan[day] = [group[session % len(group)] for group in groups.values()]
            session += 1
        else:
            plan[day] = "Rest"
    return plan


def total_intensity(plan):
    """Add up the intensity of every exercise on every training day."""
    total = 0
    for workout in plan.values():
        if workout != "Rest":
            for ex in workout:
                total += ex["intensity"]
    return total


def intensity_label(total):
    """Light below 40, Moderate from 40 to 80, Intense above 80."""
    if total < 40:
        return "Light"
    elif total <= 80:
        return "Moderate"
    else:
        return "Intense"


def format_plan(plan):
    """Turn the plan into printable lines, one per day."""
    lines = []
    for day, workout in plan.items():
        if workout == "Rest":
            lines.append(f"{day:<10} Rest")
        else:
            names = ", ".join(ex["name"] for ex in workout)
            minutes = sum(ex["duration"] for ex in workout)
            lines.append(f"{day:<10} {names} ({minutes} min)")
    return lines
# Maintain workout planning functionality.