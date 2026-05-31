"""
Test Requirement Assurance

Validates Requirement → Claim → Evidence → Assurance.
"""

from claim_assurance_engine import ClaimAssuranceEngine
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine
from requirement_library import load_requirements


requirements = load_requirements()
claims = load_claim_library()

requirement = requirements[0]

claim = next(
    claim
    for claim in claims
    if claim.claim_id == requirement.claim_ids[0]
)

approved_claim = ApprovedClaim(
    claim=claim,
    target_name="easyTravel-Business",
    thresholds={},
)

provider = DynatraceProvider()
runtime_reality = provider.get_runtime_reality().to_dict()

adapter = DynatraceEvidenceAdapter(runtime_reality)
collection_engine = EvidenceCollectionEngine(adapter)

evidence_records = collection_engine.collect_evidence(approved_claim)

assurance_engine = ClaimAssuranceEngine()
result = assurance_engine.evaluate(approved_claim, evidence_records)

print(f"Requirement: {requirement.title}")
print(f"Claim: {result.claim_id}")
print(f"Target: {result.target_name}")
print(f"Status: {result.status}")
print(f"Confidence: {result.confidence}")
print(f"Explanation: {result.explanation}")
