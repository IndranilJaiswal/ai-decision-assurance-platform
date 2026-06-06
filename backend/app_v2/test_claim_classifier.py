"""
test_claim_classifier.py

Purpose:
---------
Validates claim classification behaviour.

Expected Results:
-----------------

SERVICE_EXISTS
→ EXECUTABLE_CLAIM

SERVICE_HEALTHY
→ EXECUTABLE_CLAIM

REDIS_AVAILABLE
→ POTENTIAL_ASSURANCE_GAP

POSTGRESQL_AVAILABLE
→ POTENTIAL_ASSURANCE_GAP
"""

from claim_classifier import ClaimClassifier

classifier = ClaimClassifier()

test_claims = [
    "SERVICE_EXISTS",
    "SERVICE_HEALTHY",
    "REDIS_AVAILABLE",
    "POSTGRESQL_AVAILABLE"
]

print("\n==============================")
print("CLAIM CLASSIFICATION TEST")
print("==============================")

for claim in test_claims:

    result = classifier.classify(claim)

    print(result)
