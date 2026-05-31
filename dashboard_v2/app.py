"""
AI Decision Assurance Platform Dashboard

Dashboard v1 shows the full Build 1 flow:

Requirement
↓
Claims
↓
Evidence
↓
Claim Assurance
↓
Requirement Assurance
"""

import sys
from pathlib import Path

import streamlit as st


# Allow dashboard to import backend modules.
ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "backend" / "app_v2"

sys.path.append(str(APP_DIR))


from claim_assurance_engine import ClaimAssuranceEngine
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


st.set_page_config(
    page_title="AI Decision Assurance Platform",
    layout="wide",
)


st.title("AI Decision Assurance Platform")
st.caption("Requirement → Claim → Evidence → Assurance")


@st.cache_data(ttl=60)
def run_assurance_pipeline():
    """
    Run the current end-to-end assurance pipeline.

    This function loads requirements and claims,
    collects live Dynatrace runtime reality,
    generates evidence,
    evaluates claims,
    and rolls them up into requirement assurance.
    """

    requirements = load_requirements()
    claims = load_claim_library()

    provider = DynatraceProvider()
    runtime_reality = provider.get_runtime_reality().to_dict()

    adapter = DynatraceEvidenceAdapter(runtime_reality)
    collection_engine = EvidenceCollectionEngine(adapter)

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    results = []

    for requirement in requirements:

        claim_results = []
        evidence_by_claim = {}

        for claim_id in requirement.claim_ids:

            claim = next(
                claim
                for claim in claims
                if claim.claim_id == claim_id
            )

            approved_claim = ApprovedClaim(
                claim=claim,
                target_name="easyTravel-Business",
                thresholds={},
            )

            evidence_records = collection_engine.collect_evidence(
                approved_claim
            )

            claim_result = claim_assurance_engine.evaluate(
                approved_claim,
                evidence_records
            )

            claim_results.append(claim_result)
            evidence_by_claim[claim_id] = evidence_records

        requirement_result = requirement_assurance_engine.evaluate(
            requirement,
            claim_results
        )

        results.append(
            {
                "requirement": requirement,
                "requirement_result": requirement_result,
                "evidence_by_claim": evidence_by_claim,
            }
        )

    return results


def status_badge(status):
    """Render a readable status label."""

    if status == "VERIFIED":
        return "✅ VERIFIED"

    if status == "PARTIALLY_ASSURED":
        return "⚠️ PARTIALLY ASSURED"

    if status == "FAILED":
        return "❌ FAILED"

    if status == "INSUFFICIENT_EVIDENCE":
        return "⚠️ INSUFFICIENT EVIDENCE"

    return status


results = run_assurance_pipeline()


summary_col1, summary_col2, summary_col3 = st.columns(3)

verified_count = sum(
    1
    for item in results
    if item["requirement_result"].status == "VERIFIED"
)

partial_count = sum(
    1
    for item in results
    if item["requirement_result"].status == "PARTIALLY_ASSURED"
)

failed_count = sum(
    1
    for item in results
    if item["requirement_result"].status == "FAILED"
)

summary_col1.metric("Verified", verified_count)
summary_col2.metric("Partially Assured", partial_count)
summary_col3.metric("Failed", failed_count)


st.divider()

for item in results:

    requirement = item["requirement"]
    requirement_result = item["requirement_result"]
    evidence_by_claim = item["evidence_by_claim"]

    with st.container(border=True):

        st.subheader(requirement.title)
        st.write(requirement.description)

        st.markdown(
            f"### Status: {status_badge(requirement_result.status)}"
        )

        st.write(requirement_result.explanation)

        st.markdown("#### Supporting Claims")

        for claim_result in requirement_result.claim_results:

            with st.expander(
                f"{claim_result.claim_id} — {status_badge(claim_result.status)}"
            ):

                st.write(f"**Target:** {claim_result.target_name}")
                st.write(f"**Confidence:** {claim_result.confidence}")
                st.write(f"**Explanation:** {claim_result.explanation}")

                if claim_result.evidence_gaps:
                    st.warning(
                        "Missing evidence: "
                        + ", ".join(claim_result.evidence_gaps)
                    )

                st.markdown("##### Evidence Records")

                evidence_records = evidence_by_claim.get(
                    claim_result.claim_id,
                    []
                )

                for evidence in evidence_records:
                    st.json(
                        {
                            "evidence_type": evidence.evidence_type,
                            "source": evidence.source,
                            "observed": evidence.observed,
                            "value": evidence.value,
                            "details": evidence.details,
                        }
                    )
