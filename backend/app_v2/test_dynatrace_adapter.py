"""
Test Dynatrace Adapter

Purpose:
Verify that an approved claim can be converted into
evidence requests and evaluated against live Dynatrace
runtime reality.

Architecture:

Approved Claim
        ↓
Evidence Request Builder
        ↓
Evidence Request
        ↓
Dynatrace Provider
        ↓
Runtime Reality
        ↓
Dynatrace Evidence Adapter
        ↓
Evidence Record
"""

from claim_library import load_claim_library
from claim_models import ApprovedClaim
from evidence_request_builder import EvidenceRequestBuilder
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider


# Create a live Dynatrace-backed runtime reality provider.
provider = DynatraceProvider()

# Collect normalized runtime reality.
runtime_reality = provider.get_runtime_reality().to_dict()

# Load available claim templates.
claims = load_claim_library()

# Select the SERVICE_EXISTS claim template.
service_exists_claim = next(
    claim
    for claim in claims
    if claim.claim_id == "SERVICE_EXISTS"
)

# Create an approved claim instance.
# The target must match a service currently observed
# in Dynatrace runtime reality.
approved_claim = ApprovedClaim(
    claim=service_exists_claim,
    target_name="easyTravel-Business",
    thresholds={},
)

# Convert the approved claim into evidence requests.
builder = EvidenceRequestBuilder()

requests = builder.build_requests(
    approved_claim
)

# Create the evidence adapter.
adapter = DynatraceEvidenceAdapter(
    runtime_reality
)

# Collect evidence for every request.
for request in requests:

    evidence = adapter.collect(
        request
    )

    print(
        f"{evidence.claim_id} | "
        f"{evidence.target_name} | "
        f"{evidence.evidence_type} | "
        f"observed={evidence.observed}"
    )
