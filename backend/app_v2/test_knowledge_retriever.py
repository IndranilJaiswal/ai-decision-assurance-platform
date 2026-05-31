"""
Test Knowledge Retriever

Purpose:
Verify retrieval from MongoDB knowledge collections.
"""

from knowledge_retriever import KnowledgeRetriever


def main():

    retriever = KnowledgeRetriever()

    context = retriever.retrieve(
        "Booking service must remain available"
    )

    print()
    print("Requirement:")
    print(context.requirement)

    print()
    print("Retrieved Documents:")
    print()

    for document in context.documents:

        print(
            f"{document.document_id} "
            f"({document.source_type})"
        )

        print(
            f"Title: {document.title}"
        )

        print(
            f"Score: {document.score}"
        )

        print()


if __name__ == "__main__":
    main()
