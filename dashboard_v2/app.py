"""
AI Decision Assurance Platform Dashboard

Dashboard v1 shows the full Build 1 flow:

Requirement
↓
Supporting Claims
↓
Evidence Records
↓
Claim Assurance
↓
Requirement Assurance

AI is not making the assurance decision here.
The dashboard only displays deterministic assurance results
produced by approved claims, collected evidence, and rules.
"""

import sys
from pathlib import Path

import streamlit as st


# Add backend/app_v2 to Python import path so Streamlit can use backend modules.
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

    Current flow:
    1. Load requirements.
    2. Load claim templates.
    3. Collect live runtime reality from Dynatrace.
    4. Create approved claims for each requirement.
    5. Collect evidence for each approved claim.
    6. Evaluate claim assurance.
    7. Roll claim assurance into requirement assurance.
    """

    requirements = load_requirements()
    claims = load_claim_library()

    # Live runtime reality from Dynatrace.
    provider = DynatraceProvider()
    runtime_reality = provider.get_runtime_reality().to_dict()

    # Evidence adapter works against normalized runtime reality.
    adapter = DynatraceEvidenceAdapter(runtime_reality)
    collection_engine = EvidenceCollectionEngine(adapter)

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    results = []

    for requirement in requirements:

        claim_results = []
        evidence_by_claim = {}

        for claim_id in requirement.claim_ids:

            # Resolve claim template from claim library.
            claim = next(
                claim
                for claim in claims
                if claim.claim_id == claim_id
            )

            # For Build 1, all claims target the easyTravel business service.
            # Later this should come from requirement configuration or UI input.
            approved_claim = ApprovedClaim(
                claim=claim,
                target_name="easyTravel-Business",
                thresholds={},
            )

            # Collect evidence required by the approved claim.
            evidence_records = collection_engine.collect_evidence(
                approved_claim
            )

            # Evaluate claim assurance from evidence records.
            claim_result = claim_assurance_engine.evaluate(
                approved_claim,
                evidence_records
            )

            claim_results.append(claim_result)
            evidence_by_claim[claim_id] = evidence_records

        # Roll claim assurance results up to requirement assurance.
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


def status_badge(status: str) -> str:
    """Return readable status label with icon."""

    if status == "VERIFIED":
        return "✅ VERIFIED"

    if status == "PARTIALLY_ASSURED":
        return "⚠️ PARTIALLY ASSURED"

    if status == "FAILED":
        return "❌ FAILED"

    if status == "INSUFFICIENT_EVIDENCE":
        return "⚠️ INSUFFICIENT EVIDENCE"

    return status


def render_summary(results):
    """Render top-level dashboard summary metrics."""

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

    col1, col2, col3 = st.columns(3)

    col1.metric("Verified Requirements", verified_count)
    col2.metric("Partially Assured", partial_count)
    col3.metric("Failed Requirements", failed_count)


def render_evidence_records(evidence_records):
    """Render evidence records collected for a claim."""

    if not evidence_records:
        st.warning("No evidence records were collected for this claim.")
        return

    for evidence in evidence_records:

        evidence_col1, evidence_col2, evidence_col3 = st.columns(3)

        evidence_col1.write(f"**Evidence Type:** `{evidence.evidence_type}`")
        evidence_col2.write(f"**Source:** `{evidence.source}`")
        evidence_col3.write(f"**Observed:** `{evidence.observed}`")

        st.markdown("**Evidence Details**")
        st.json(
            {
                "value": evidence.value,
                "details": evidence.details,
            }
        )


def render_claim_result(claim_result, evidence_by_claim):
    """Render one claim assurance result and its evidence."""

    with st.expander(
        f"{claim_result.claim_id} — {status_badge(claim_result.status)}",
        expanded=True,
    ):

        col1, col2, col3 = st.columns(3)

        col1.write(f"**Target:** `{claim_result.target_name}`")
        col2.write(f"**Confidence:** `{claim_result.confidence}`")
        col3.write(f"**Status:** {status_badge(claim_result.status)}")

        st.markdown("##### Assurance Explanation")
        st.info(claim_result.explanation)

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

        render_evidence_records(evidence_records)


def render_requirement(item):
    """Render one requirement with claim, evidence, and assurance detail."""

    requirement = item["requirement"]
    requirement_result = item["requirement_result"]
    evidence_by_claim = item["evidence_by_claim"]

    with st.container(border=True):

        st.subheader(requirement.title)
        st.write(requirement.description)

        st.markdown(
            f"### Requirement Status: {status_badge(requirement_result.status)}"
        )

        st.info(requirement_result.explanation)

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        summary_col1.metric(
            "Verified Claims",
            requirement_result.verified_claims,
        )

        summary_col2.metric(
            "Insufficient Evidence",
            requirement_result.insufficient_claims,
        )

        summary_col3.metric(
            "Failed Claims",
            requirement_result.failed_claims,
        )

        st.markdown("#### Supporting Claims, Evidence & Assurance")

        for claim_result in requirement_result.claim_results:
            render_claim_result(
                claim_result,
                evidence_by_claim,
            )


# Run pipeline and render dashboard.
results = run_assurance_pipeline()

render_summary(results)

st.divider()

for item in results:
    render_requirement(item)
