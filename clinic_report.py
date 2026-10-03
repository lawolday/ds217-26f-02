#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return usable encounters with a patient ID, visit date, and systolic reading."""
    with open(data_path, "r", encoding="utf-8") as file:
        rows = file.readlines()

    data_rows = rows[1:]
    encounters = []
    skipped = 0

    for row in data_rows:
        fields = row.strip().split(",")

        if len(fields) != 3:
            skipped += 1
            print(f"Skipping row: {row.strip()}")
            continue

        patient_id, visit_date, raw_systolic = fields

        try:
            systolic = int(raw_systolic)
        except ValueError:
            skipped += 1
            print(f"Skipping row: {row.strip()}")
            continue

        if not 60 <= systolic <= 250:
            skipped += 1
            print(f"Skipping row: {row.strip()}")
            continue

        encounter = {
            "patient_id": patient_id,
            "visit_date": visit_date,
            "systolic": systolic,
        }
        encounters.append(encounter)

    return encounters, skipped

def main():
    """Write the vitals report and follow-up list."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)
    mean = mean_systolic(readings)
    patients_seen = count_patients(encounters)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {patients_seen}",
        f"Mean systolic: {mean:.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "vitals_report.txt"
    report_text = "\n".join(report_lines) + "\n"
    report_path.write_text(report_text, encoding="utf-8")

    saved_text = report_path.read_text(encoding="utf-8")
    print(saved_text, end="")
    cutoff = 160
    reason = "I chose 160 mmHg because I want to focus on patients with higher readings who may need follow-up sooner."

    followup_patients = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ]
    for patient_id in followup_patients:
        followup_lines.append(patient_id)

    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_text = "\n".join(followup_lines) + "\n"
    followup_path.write_text(followup_text, encoding="utf-8")

if __name__ == "__main__":
    main()
