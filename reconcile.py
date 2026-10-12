"""Baggage reconciliation: compare a flight manifest with the scanned bag tags.

Run it from the command line with two arguments: the manifest CSV file
and the scan file.

Exit code: 0 = RECONCILED, 1 = DISCREPANCY, 2 = could not read the input.
"""

import csv
import os
import sys

REQUIRED_COLUMNS = ("flight_number", "passenger_name", "bag_tag")


def clean_tag(text):
    """Normalise one bag tag: drop spaces/line endings and use upper case."""
    return text.strip().upper()


def read_manifest(path):
    """Return the set of bag tags listed in the manifest CSV."""
    # utf-8-sig drops the invisible BOM that Excel puts at the start of a CSV.
    # newline="" lets the csv module handle both \n and \r\n line endings.
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = [name.strip() for name in (reader.fieldnames or [])]
        missing = [col for col in REQUIRED_COLUMNS if col not in header]
        if missing:
            raise ValueError(
                "manifest is missing column(s): " + ", ".join(missing))
        reader.fieldnames = header
        tags = set()
        for row in reader:
            tag = clean_tag(row["bag_tag"] or "")
            if tag:
                tags.add(tag)
        return tags


def read_scan(path):
    """Return the set of bag tags in the scan file (one tag per line)."""
    with open(path, encoding="utf-8-sig") as handle:
        return {clean_tag(line) for line in handle if clean_tag(line)}


def reconcile(expected, scanned):
    """Compare the two sets and return a dict with the results."""
    missing = sorted(expected - scanned)
    extra = sorted(scanned - expected)
    verdict = "RECONCILED" if not missing and not extra else "DISCREPANCY"
    return {
        "expected": len(expected),
        "scanned": len(scanned),
        "missing": missing,
        "extra": extra,
        "verdict": verdict,
    }


def format_report(result):
    """Turn the reconcile() result into the printable report text."""
    lines = [
        "BAGGAGE RECONCILIATION REPORT",
        "Total bags expected: %d" % result["expected"],
        "Total bags scanned:  %d" % result["scanned"],
        "Missing from scan (%d):" % len(result["missing"]),
    ]
    lines += ["  - " + tag for tag in result["missing"]] or ["  (none)"]
    lines.append("Not on manifest - SECURITY CHECK (%d):" % len(result["extra"]))
    lines += ["  - " + tag for tag in result["extra"]] or ["  (none)"]
    lines.append("Verdict: " + result["verdict"])
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        program = os.path.basename(sys.argv[0])
        print("Usage: python %s MANIFEST_CSV SCAN_FILE" % program)
        return 2
    manifest_path, scan_path = argv
    try:
        expected = read_manifest(manifest_path)
        scanned = read_scan(scan_path)
    except (OSError, ValueError) as error:
        print("Error: %s" % error)
        return 2
    result = reconcile(expected, scanned)
    print(format_report(result))
    return 0 if result["verdict"] == "RECONCILED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))