"""
Evidence Engine

Turns truth gaps into evidence records.
"""


def generate_evidence_records(truth_gap_report: dict) -> list:
    """
    Convert each truth gap into an evidence record.
    """

    evidence_records = []

    for index, gap in enumerate(truth_gap_report.get("gaps", []), start=1):
        evidence_records.append({
            "evidence_id": f"EV-{index:03}",
            "source": "Dynatrace Truth Gap Analysis",
            "gap_type": gap["gap_type"],
            "observation": gap["reason"],
            "related_gap": gap,
            "confidence": 0.95
        })

    return evidence_records
