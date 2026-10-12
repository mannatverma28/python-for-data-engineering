"""Check completed workouts before they are saved to the log."""

from datetime import date, timedelta

from exercises import find_exercise

MAX_LOG_DURATION = 120


class InvalidLogError(Exception):
    """Raised when a completed-workout entry cannot be accepted."""


def week_dates(week_start):
    """Return the first and last date of the week that starts on week_start."""
    first = date.fromisoformat(week_start)
    last = first + timedelta(days=6)
    return first, last


def validate_log(log, exercises, week_start):
    """Raise InvalidLogError with the reason if the log entry is wrong."""
    if find_exercise(exercises, log["exercise"]) is None:
        raise InvalidLogError(f"unknown exercise '{log['exercise']}'")

    duration = log["duration"]
    if duration <= 0:
        raise InvalidLogError("duration must be more than 0 minutes")
    if duration > MAX_LOG_DURATION:
        raise InvalidLogError(f"duration {duration} is over {MAX_LOG_DURATION} minutes")

    try:
        logged = date.fromisoformat(log["date"])
    except ValueError:
        raise InvalidLogError(f"date '{log['date']}' is not in YYYY-MM-DD format")

    first, last = week_dates(week_start)
    if logged < first or logged > last:
        raise InvalidLogError(f"{logged} is not in this week ({first} to {last})")


def log_workout(log, exercises, week_start, logbook):
    """Add a valid entry to logbook and return a message describing what happened."""
    try:
        validate_log(log, exercises, week_start)
    except InvalidLogError as error:
        return f"Invalid log: {error}"
    logbook.append(log)
    return f"Logged: {log['exercise']} on {log['date']} for {log['duration']} min"
# Maintain workout logging functionality.