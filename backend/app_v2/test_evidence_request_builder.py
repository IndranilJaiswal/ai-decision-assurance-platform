"""
Test Evidence Request Builder
"""

from claim_library import load_claim_library
from claim_models import ApprovedClaim
from evidence_request_builder import EvidenceRequestBuilder


claims = load_claim_library()

service_health_claim = next(
    claim
    for claim in claims
    if claim.claim_id == "SERVICE_HEALTHY"
)

approved_claim = ApprovedClaim(
    claim=service_health_claim,
    target_name="easyTravel Customer Frontend",
    thresholds={}
)

builder = EvidenceRequestBuilder()

requests = builder.build_requests(approved_claim)

for request in requests:
    print(
        request.claim_id,
        request.target_name,
        request.evidence_type
    )
