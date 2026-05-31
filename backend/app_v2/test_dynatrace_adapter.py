"""
Test Dynatrace Evidence Adapter

This test verifies that SERVICE_EXISTS can be collected
from normalized Dynatrace runtime reality.
"""

from claim_library import load_claim_library
from claim_models import ApprovedClaim
from evidence_request_builder import EvidenceRequestBuilder
from dynatrace_adapter import DynatraceEvidenceAdapter


runtime_reality = {
    "services": [
        {
            "name": "easyTravel Customer Frontend",
            "entity_type": "SERVICE",
        },
        {
            "name": "easyTravel Business Backend",
            "entity_type": "SERVICE",
        },
    ]
}

claims = load_claim_library()

service_exists_claim = next(
    claim
    for claim in claims
    if claim.claim_id == "SERVICE_EXISTS"
)

approved_claim = ApprovedClaim(
    claim=service_exists_claim,
    target_name="easyTravel Customer Frontend",
    thresholds={},
)

builder = EvidenceRequestBuilder()
requests = builder.build_requests(approved_claim)

adapter = DynatraceEvidenceAdapter(runtime_reality)

for request in requests:
    evidence = adapter.collect(request)

    print(
        f"{evidence.claim_id} | "
        f"{evidence.target_name} | "
        f"{evidence.evidence_type} | "
        f"observed={evidence.observed}"
    )
