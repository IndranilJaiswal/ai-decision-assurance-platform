from knowledge_retriever import (
    KnowledgeRetriever
)

retriever = KnowledgeRetriever()

print("\nPolicies")
print("========")

for policy in retriever.get_policies():
    print(policy)

print("\nStandards")
print("=========")

for standard in retriever.get_standards():
    print(standard)
