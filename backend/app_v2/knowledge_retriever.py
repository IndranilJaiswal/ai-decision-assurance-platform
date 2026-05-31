"""
Knowledge Retriever

Purpose:
Retrieve relevant knowledge documents from MongoDB.

Current Retrieval Strategy:
- Title matching
- Tag matching
- Content matching

Future:
- Atlas Vector Search
- Embeddings
- Semantic Retrieval

Must Not:
- Call Gemini
- Generate Claims
- Perform Assurance
"""

from mongodb_client import MongoDBClient
from knowledge_models import (
    KnowledgeDocument,
    RetrievedContext,
)


class KnowledgeRetriever:
    """
    Retrieve knowledge relevant to a requirement.
    """

    COLLECTIONS = [
        "organization_policies",
        "standards",
        "technical_documentation",
    ]

    def __init__(self):

        self.mongo = MongoDBClient()

    def retrieve(
        self,
        requirement: str,
        max_results: int = 5,
    ) -> RetrievedContext:
        """
        Retrieve relevant documents.

        Current implementation uses simple keyword scoring.
        """

        requirement_lower = requirement.lower()

        scored_documents = []

        for collection_name in self.COLLECTIONS:

            collection = self.mongo.get_collection(
                collection_name
            )

            for document in collection.find({}):

                score = self._calculate_score(
                    requirement_lower,
                    document,
                )

                if score <= 0:
                    continue

                scored_documents.append(
                    KnowledgeDocument(
                        document_id=document["document_id"],
                        source_type=document["source_type"],
                        title=document["title"],
                        content=document["content"],
                        tags=document.get("tags", []),
                        score=score,
                    )
                )

        scored_documents.sort(
            key=lambda document: document.score,
            reverse=True,
        )

        return RetrievedContext(
            requirement=requirement,
            documents=scored_documents[:max_results],
        )

    def _calculate_score(
        self,
        requirement: str,
        document: dict,
    ) -> float:
        """
        Simple keyword-based scoring.

        Scoring:
        +5 title match
        +3 tag match
        +1 content match
        """

        score = 0

        title = document.get(
            "title",
            "",
        ).lower()

        content = document.get(
            "content",
            "",
        ).lower()

        tags = [
            tag.lower()
            for tag in document.get(
                "tags",
                [],
            )
        ]

        keywords = requirement.split()

        for keyword in keywords:

            if keyword in title:
                score += 5

            if keyword in tags:
                score += 3

            if keyword in content:
                score += 1

        return score
