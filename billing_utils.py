# Helper module for the billing office.
# One constant and two functions, used by the bill notice script.

RESIDENTIAL_RATE = 12  # cents per unit; business customers pay double


def units_used(previous_reading, current_reading):
    # Negative means the meter went backwards.
    return current_reading - previous_reading


def charge_cents(units, meter_type):
    if meter_type == "residential":
        return units * RESIDENTIAL_RATE
    if meter_type == "business":
        return units * RESIDENTIAL_RATE * 2
    raise ValueError("Unknown meter type: " + meter_type)