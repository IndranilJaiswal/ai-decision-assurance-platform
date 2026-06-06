"""
test_claims.py

Purpose:
---------
Validates that the MongoDB claim repository
has been seeded correctly.

This script is intended for development and
sanity-check verification before building
the Claim Classification Engine.

Collections Validated:
----------------------

1. claim_patterns

Expected:
- SERVICE_EXISTS
- SERVICE_HEALTHY

2. executable_claims

Expected:
- SERVICE_EXISTS
- SERVICE_HEALTHY

Usage:
------
python3 backend/app_v2/test_claims.py

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

# --------------------------------------------------
# Read collections
# --------------------------------------------------

claim_patterns = db["claim_patterns"]
executable_claims = db["executable_claims"]

# --------------------------------------------------
# Display Claim Patterns
# --------------------------------------------------

print("\n==============================")
print("CLAIM PATTERNS")
print("==============================")

for document in claim_patterns.find():
    print(document)

# --------------------------------------------------
# Display Executable Claims
# --------------------------------------------------

print("\n==============================")
print("EXECUTABLE CLAIMS")
print("==============================")

for document in executable_claims.find():
    print(document)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nMongoDB claim repository validation complete.")
