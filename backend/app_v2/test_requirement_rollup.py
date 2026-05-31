"""
Test Requirement Rollup

Validates Requirement → Claims → Evidence → Claim Assurance → Requirement Assurance.
"""

from claim_assurance_engine import ClaimAssuranceEngine
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


requirements = load_requirements()
claims = load_claim_library()

provider = DynatraceProvider()
runtime_reality = provider.get_runtime_reality().to_dict()

adapter = DynatraceEvidenceAdapter(runtime_reality)
collection_engine = EvidenceCollectionEngine(adapter)

claim_assurance_engine = ClaimAssuranceEngine()
requirement_assurance_engine = RequirementAssuranceEngine()

for requirement in requirements:

    claim_results = []

    for claim_id in requirement.claim_ids:

        claim = next(
            claim
            for claim in claims
            if claim.claim_id == claim_id
        )

        approved_claim = ApprovedClaim(
            claim=claim,
            target_name="easyTravel-Business",
            thresholds={},
        )

        evidence_records = collection_engine.collect_evidence(
            approved_claim
        )

        claim_result = claim_assurance_engine.evaluate(
            approved_claim,
            evidence_records
        )

        claim_results.append(claim_result)

    requirement_result = requirement_assurance_engine.evaluate(
        requirement,
        claim_results
    )

    print("\nRequirement:", requirement_result.title)
    print("Status:", requirement_result.status)
    print("Explanation:", requirement_result.explanation)

    for claim_result in requirement_result.claim_results:
        print(
            f"  - {claim_result.claim_id}: "
            f"{claim_result.status}"
        )
