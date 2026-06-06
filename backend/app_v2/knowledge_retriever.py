"""
knowledge_retriever.py

Purpose:
---------
Retrieves knowledge from MongoDB to provide
context to the Gemini Claim Discovery Agent.

Current Scope:
--------------
- claim_patterns

Future Scope:
-------------
- policies
- standards
- technical_documents
- remediation_patterns

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
        "MONGODB_URI not configured"
    )

# --------------------------------------------------
# MongoDB connection
# --------------------------------------------------

client = MongoClient(mongodb_uri)

db = client["ai_assurance"]

claim_patterns = db["claim_patterns"]


class KnowledgeRetriever:

    def get_claim_patterns(self):
        """
        Retrieve all known claim patterns.

        Returns:
            list[dict]
        """

        patterns = []

        for document in claim_patterns.find(
            {},
            {"_id": 0}
        ):
            patterns.append(document)

        return patterns
