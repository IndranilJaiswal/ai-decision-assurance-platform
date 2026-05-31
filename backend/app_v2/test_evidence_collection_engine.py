"""
Test Evidence Collection Engine

Validates the complete evidence collection flow.

Architecture:

Approved Claim
        ↓
Evidence Request Builder
        ↓
Evidence Requests
        ↓
Dynatrace Adapter
        ↓
Evidence Records
"""

from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine


# Collect live runtime reality.
provider = DynatraceProvider()

runtime_reality = provider.get_runtime_reality().to_dict()

# Create evidence adapter.
adapter = DynatraceEvidenceAdapter(
    runtime_reality
)

# Create collection engine.
engine = EvidenceCollectionEngine(
    adapter
)

# Load claims.
claims = load_claim_library()

# Select claim.
service_exists_claim = next(
    claim
    for claim in claims
    if claim.claim_id == "SERVICE_EXISTS"
)

approved_claim = ApprovedClaim(
    claim=service_exists_claim,
    target_name="easyTravel-Business",
    thresholds={}
)

# Collect evidence.
evidence_records = engine.collect_evidence(
    approved_claim
)

for evidence in evidence_records:

    print(
        f"{evidence.claim_id} | "
        f"{evidence.target_name} | "
        f"observed={evidence.observed}"
    )
