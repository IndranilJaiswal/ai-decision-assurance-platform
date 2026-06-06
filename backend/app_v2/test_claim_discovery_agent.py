"""
test_claim_discovery_agent.py

Purpose:
---------
Validate requirement-to-claim discovery.
"""

from claim_discovery_agent import (
    ClaimDiscoveryAgent
)

agent = ClaimDiscoveryAgent()

suggestions = agent.discover(
    "Booking service must remain available."
)

print("\n==============================")
print("CLAIM DISCOVERY")
print("==============================")

for suggestion in suggestions:

    print(
        suggestion.claim_id
    )
