"""Exercise data for FitPlan, plus helpers to group and filter it."""

# Beginners stay at or below these limits in a single exercise.
MAX_SAFE_INTENSITY = 4
MAX_SAFE_DURATION = 45

# The coach's sample list: name, muscle group, intensity 1-5, minutes.
SAMPLE_EXERCISES = [
    {"name": "Squats", "muscle_group": "Legs", "intensity": 3, "duration": 20},
    {"name": "Lunges", "muscle_group": "Legs", "intensity": 2, "duration": 15},
    {"name": "Push-ups", "muscle_group": "Chest", "intensity": 3, "duration": 10},
    {"name": "Burpees", "muscle_group": "Chest", "intensity": 5, "duration": 15},
    {"name": "Rows", "muscle_group": "Back", "intensity": 3, "duration": 20},
    {"name": "Plank", "muscle_group": "Core", "intensity": 2, "duration": 10},
]


def is_safe(exercise):
    """Return True if a beginner can safely do this exercise."""
    intensity = exercise["intensity"]
    duration = exercise["duration"]
    if intensity < 1 or intensity > MAX_SAFE_INTENSITY:
        return False
    if duration <= 0 or duration > MAX_SAFE_DURATION:
        return False
    return True


def pick_safe(exercises):
    """Keep only the exercises that pass the safety check."""
    return [ex for ex in exercises if is_safe(ex)]


def group_by_muscle(exercises):
    """Build a dictionary: muscle group -> list of exercises in that group."""
    groups = {}
    for ex in exercises:
        group = ex["muscle_group"]
        if group not in groups:
            groups[group] = []
        groups[group].append(ex)
    return groups


def find_exercise(exercises, name):
    """Return the exercise with this name (any letter case), or None."""
    for ex in exercises:
        if ex["name"].lower() == name.strip().lower():
            return ex
    return None
# Maintain exercise management functionality.