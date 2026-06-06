"""
seed_claims.py

Purpose:
---------
Seeds the MongoDB knowledge store with the initial claim repository
required for the AI Assurance Platform.

Collections Created:
--------------------
1. claim_patterns
   Example claims used as reference patterns for Gemini Claim Discovery.

2. executable_claims
   Claims that the Assurance Engine is currently capable of evaluating.

Usage:
------
python3 backend/app_v2/seed_claims.py

Author:
-------
Indranil Jaiswal
AI Assurance Platform
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    raise ValueError(
        "MONGODB_URI not found in environment variables"
    )

# --------------------------------------------------
# Connect to MongoDB Atlas
# --------------------------------------------------

client = MongoClient(mongodb_uri)

db = client["ai_assurance"]

claim_patterns = db["claim_patterns"]
executable_claims = db["executable_claims"]

# --------------------------------------------------
# Clear collections
#
# Helpful during development to avoid duplicates.
# Remove later if migration strategy is implemented.
# --------------------------------------------------

claim_patterns.delete_many({})
executable_claims.delete_many({})

# --------------------------------------------------
# Seed Claim Patterns
#
# These are examples Gemini can use during
# claim discovery and reasoning.
# --------------------------------------------------

claim_patterns.insert_many(
    [
        {
            "claim_name": "SERVICE_EXISTS",
            "description": "Service is deployed and reachable",
            "domain": "Availability",
            "source": "pattern"
        },
        {
            "claim_name": "SERVICE_HEALTHY",
            "description": "Service meets operational health criteria",
            "domain": "Availability",
            "source": "pattern"
        }
    ]
)

# --------------------------------------------------
# Seed Executable Claims
#
# These claims have evidence requirements
# defined and can be evaluated by the
# Assurance Engine.
# --------------------------------------------------

executable_claims.insert_many(
    [
        {
            "claim_name": "SERVICE_EXISTS",
            "required_evidence": [
                "entity_detected"
            ],
            "claim_type": "EXECUTABLE"
        },
        {
            "claim_name": "SERVICE_HEALTHY",
            "required_evidence": [
                "response_time",
                "error_rate"
            ],
            "claim_type": "EXECUTABLE"
        }
    ]
)

print("Claim repository seeded successfully.")
