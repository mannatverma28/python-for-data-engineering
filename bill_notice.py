# Turns one customer line into a printed bill notice.
# Give the line as one quoted argument: "ada|1200|1350|30|residential"
import sys

import billing_utils


def build_notice(line):
    parts = line.strip().split("|")
    if len(parts) != 5:
        return "Rejected: expected name|previous|current|days|meter_type"

    name, previous_text, current_text, days_text, meter_type = parts
    if meter_type not in ("residential", "business"):
        return "Rejected: unknown meter type '" + meter_type + "'"

    try:
        previous = int(previous_text)
        current = int(current_text)
        days = int(days_text)
    except ValueError:
        return "Rejected: readings and days must be whole numbers"

    lines = [
        "BILL NOTICE",
        "Customer: " + name,
        "Meter type: " + meter_type,
        "Days: " + str(days),
    ]

    units = billing_utils.units_used(previous, current)
    if units < 0:
        lines.append("WARNING: meter reading went backwards ("
                     + str(current) + " is below " + str(previous) + ")")
        return "\n".join(lines)

    lines.append("Units used: " + str(units))
    charge = billing_utils.charge_cents(units, meter_type)
    lines.append("Charge: " + str(charge) + " cents")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Give one customer line in quotes, like \"ada|1200|1350|30|residential\"")
    else:
        print(build_notice(sys.argv[1]))