"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list of systolic readings from the encounters."""
    readings = []

    for encounter in encounters:
        readings.append(encounter["systolic"])

    return readings


def mean_systolic(readings):
    """Return the mean systolic reading, or None when there are no readings."""
    if not readings:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in the encounters."""
    patient_ids = set()

    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])

    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return patient IDs with a systolic reading at or above the cutoff."""
    patient_ids = set()

    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patient_ids.add(encounter["patient_id"])

    return sorted(patient_ids)