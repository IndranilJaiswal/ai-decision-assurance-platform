"""
Assurance Engine

Creates assurance records from requirements and evidence.
"""


def generate_assurance_records(requirements: list, evidence_records: list) -> list:
    """
    For MVP, every requirement with unresolved evidence gaps becomes NOT_ASSURED.

    Later, this can become smarter:
    - map evidence to specific requirements
    - assign confidence
    - include verification and validation workflows
    """

    assurance_records = []

    for index, requirement in enumerate(requirements, start=1):
        status = "ASSURED" if not evidence_records else "NOT_ASSURED"

        assurance_records.append({
            "assurance_id": f"AS-{index:03}",
            "requirement_id": requirement["id"],
            "requirement": requirement["statement"],
            "status": status,
            "evidence": [
                record["evidence_id"]
                for record in evidence_records
            ],
            "reason": (
                "Requirement cannot be assured because one or more declared "
                "architecture elements were not observed in Dynatrace."
                if evidence_records
                else "Requirement is assured based on observed runtime evidence."
            ),
            "verification_method": "Verify component and dependency visibility in Dynatrace.",
            "validation_method": "Run functional transaction test and confirm runtime dependency path."
        })

    return assurance_records
