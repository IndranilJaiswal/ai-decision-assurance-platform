"""
Main runner for AI Decision Assurance Platform MVP.

Milestone 1:
requirements.json
declared_architecture.json
dynatrace_snapshot.json

↓

truth_gap_report.json
evidence_records.json
assurance_records.json
"""

import json
from pathlib import Path

from reality_engine import generate_truth_gap_report
from evidence_engine import generate_evidence_records
from assurance_engine import generate_assurance_records


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data_v2"
OUTPUT_DIR = BASE_DIR / "outputs"


def load_json(file_path: Path):
    """
    Load JSON file safely.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path: Path, data):
    """
    Save JSON output in readable format.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    requirements = load_json(DATA_DIR / "requirements.json")
    declared_architecture = load_json(DATA_DIR / "declared_architecture.json")
    dynatrace_snapshot = load_json(DATA_DIR / "dynatrace_snapshot.json")

    truth_gap_report = generate_truth_gap_report(
        declared_architecture,
        dynatrace_snapshot
    )

    evidence_records = generate_evidence_records(truth_gap_report)

    assurance_records = generate_assurance_records(
        requirements,
        evidence_records
    )

    save_json(OUTPUT_DIR / "truth_gap_report.json", truth_gap_report)
    save_json(OUTPUT_DIR / "evidence_records.json", evidence_records)
    save_json(OUTPUT_DIR / "assurance_records.json", assurance_records)

    print("AI Decision Assurance Platform MVP completed.")
    print(f"Truth gaps found: {truth_gap_report['summary']['total_gaps']}")
    print("Outputs written to /outputs")


if __name__ == "__main__":
    main()
