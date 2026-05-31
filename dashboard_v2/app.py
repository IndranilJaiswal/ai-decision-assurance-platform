"""
AI Decision Assurance Platform Dashboard

Purpose:
Provide an interactive dashboard for the end-to-end assurance workflow.

Current visible flow:

Requirement
↓
Policy Agent
↓
Suggested Claims
↓
Human Approval
↓
Approved Claims
↓
Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation
↓
Dashboard

Important Governance Principle:
Policy agents suggest claims.
Humans approve claims.
Evidence and deterministic rules produce assurance.
The explanation engine explains assurance outcomes.
"""

import sys
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------------------------
# Import backend modules
# ---------------------------------------------------------------------------
# Streamlit runs from the repository root, but backend modules live in:
# backend/app_v2
#
# We add that directory to sys.path so the dashboard can import the platform
# engines without packaging the project yet.
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "backend" / "app_v2"

sys.path.append(str(APP_DIR))


from assurance_explanation_engine import AssuranceExplanationEngine
from availability_policy_agent import AvailabilityPolicyAgent
from claim_approval_engine import ClaimApprovalEngine
from claim_assurance_engine import ClaimAssuranceEngine
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


# ---------------------------------------------------------------------------
# Streamlit page setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Decision Assurance Platform",
    layout="wide",
)

st.title("AI Decision Assurance Platform")
st.caption(
    "Requirement → Policy Agent → Human Approval → Evidence → Assurance → Explanation"
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def status_badge(status: str) -> str:
    """Return a readable status label with a small visual indicator."""

    if status == "VERIFIED":
        return "✅ VERIFIED"

    if status == "PARTIALLY_ASSURED":
        return "⚠️ PARTIALLY ASSURED"

    if status == "FAILED":
        return "❌ FAILED"

    if status == "INSUFFICIENT_EVIDENCE":
        return "⚠️ INSUFFICIENT EVIDENCE"

    return status


def get_claim_by_id(claims, claim_id):
    """
    Return a claim template from the claim library.

    The claim library contains approved observable claims.
    Policy agents only suggest claim IDs; this function resolves the actual
    claim definition before assurance execution.
    """

    return next(
        claim
        for claim in claims
        if claim.claim_id == claim_id
    )


@st.cache_data(ttl=60)
def load_runtime_reality():
    """
    Load live runtime reality from Dynatrace.

    The result is cached briefly to avoid repeatedly calling Dynatrace on
    every dashboard interaction.

    Runtime reality is evidence source input.
    It is not an assurance decision.
    """

    provider = DynatraceProvider()
    return provider.get_runtime_reality().to_dict()


def run_assurance_for_requirement(requirement, approved_claim_ids):
    """
    Run assurance only for human-approved claims.

    This function enforces the core governance boundary:

    Suggested claims do not enter evidence collection.
    Approved claims enter evidence collection.

    Parameters
    ----------
    requirement:
        Requirement selected by the user.

    approved_claim_ids:
        Claims selected and approved by the human reviewer.

    Returns
    -------
    dict
        Requirement, requirement assurance result, and collected evidence.
    """

    claims = load_claim_library()
    runtime_reality = load_runtime_reality()

    adapter = DynatraceEvidenceAdapter(runtime_reality)
    collection_engine = EvidenceCollectionEngine(adapter)

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    claim_results = []
    evidence_by_claim = {}

    for claim_id in approved_claim_ids:

        claim = get_claim_by_id(
            claims,
            claim_id,
        )

        # Build 1 uses one known demo target from easyTravel.
        # Future versions should make target selection configurable per
        # requirement, claim, or user input.
        approved_claim = ApprovedClaim(
            claim=claim,
            target_name="easyTravel-Business",
            thresholds={},
        )

        # Evidence collection converts observed runtime reality into
        # EvidenceRecord objects.
        evidence_records = collection_engine.collect_evidence(
            approved_claim
        )

        # Claim assurance evaluates whether collected evidence is sufficient
        # and supportive for the approved claim.
        claim_result = claim_assurance_engine.evaluate(
            approved_claim,
            evidence_records,
        )

        claim_results.append(claim_result)
        evidence_by_claim[claim_id] = evidence_records

    # Requirement assurance rolls claim assurance results into a business-level
    # requirement status.
    requirement_result = requirement_assurance_engine.evaluate(
        requirement,
        claim_results,
    )

    return {
        "requirement": requirement,
        "requirement_result": requirement_result,
        "evidence_by_claim": evidence_by_claim,
    }


def render_evidence_records(evidence_records):
    """
    Render evidence records collected for a claim.

    Evidence records are the traceable facts used by the assurance engine.
    """

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
    """
    Render claim-level assurance and evidence.

    Each claim shows:
    - Target
    - Confidence
    - Status
    - Explanation
    - Evidence gaps
    - Evidence records
    """

    with st.expander(
        f"{claim_result.claim_id} — {status_badge(claim_result.status)}",
        expanded=True,
    ):

        col1, col2, col3 = st.columns(3)

        col1.write(f"**Target:** `{claim_result.target_name}`")
        col2.write(f"**Confidence:** `{claim_result.confidence}`")
        col3.write(f"**Status:** {status_badge(claim_result.status)}")

        st.markdown("##### Claim Assurance Explanation")
        st.info(claim_result.explanation)

        if claim_result.evidence_gaps:
            st.warning(
                "Missing evidence: "
                + ", ".join(claim_result.evidence_gaps)
            )

        st.markdown("##### Evidence Records")

        evidence_records = evidence_by_claim.get(
            claim_result.claim_id,
            [],
        )

        render_evidence_records(evidence_records)


def render_assurance_explanation(requirement_result):
    """
    Render requirement-level assurance explanation.

    The explanation engine explains deterministic assurance results.
    It does not change assurance status.
    """

    explanation_engine = AssuranceExplanationEngine()
    explanation = explanation_engine.explain(requirement_result)

    st.markdown("## AI Assurance Explanation")

    with st.container(border=True):

        st.subheader(explanation.title)

        st.write(explanation.summary)

        st.markdown("### Details")

        for detail in explanation.details:
            st.write(f"• {detail}")

        st.markdown("### Recommendations")

        for recommendation in explanation.recommendations:
            st.write(f"• {recommendation}")


def render_requirement_result(item):
    """
    Render requirement-level assurance result.

    This includes:
    - Requirement status
    - Rollup counts
    - Claim assurance details
    - Evidence records
    - Assurance explanation
    """

    requirement = item["requirement"]
    requirement_result = item["requirement_result"]
    evidence_by_claim = item["evidence_by_claim"]

    st.markdown("## Requirement Assurance Result")

    with st.container(border=True):

        st.subheader(requirement.title)
        st.write(requirement.description)

        st.markdown(
            f"### Requirement Status: "
            f"{status_badge(requirement_result.status)}"
        )

        st.info(requirement_result.explanation)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Verified Claims",
            requirement_result.verified_claims,
        )

        col2.metric(
            "Insufficient Evidence",
            requirement_result.insufficient_claims,
        )

        col3.metric(
            "Failed Claims",
            requirement_result.failed_claims,
        )

        st.markdown("#### Claim Assurance Detail")

        for claim_result in requirement_result.claim_results:

            render_claim_result(
                claim_result,
                evidence_by_claim,
            )

    # Explanation is rendered after the assurance result so users first see
    # the deterministic result and then the narrative interpretation.
    render_assurance_explanation(requirement_result)


# ---------------------------------------------------------------------------
# Main dashboard
# ---------------------------------------------------------------------------

requirements = load_requirements()

selected_requirement = st.selectbox(
    "Select Requirement",
    requirements,
    format_func=lambda requirement: (
        f"{requirement.requirement_id} - {requirement.title}"
    ),
)

st.markdown("## Requirement")
st.write(selected_requirement.description)


# ---------------------------------------------------------------------------
# Policy agent claim discovery
# ---------------------------------------------------------------------------

st.markdown("## Policy Agent Suggested Claims")

policy_agent = AvailabilityPolicyAgent()

suggestions = policy_agent.suggest_claims(
    selected_requirement.title
)

approval_engine = ClaimApprovalEngine()

selected_claim_ids = []

for suggestion in suggestions:

    with st.container(border=True):

        col1, col2 = st.columns([1, 3])

        with col1:
            selected = st.checkbox(
                suggestion.claim_id,
                value=suggestion.claim_id in selected_requirement.claim_ids,
                key=(
                    f"{selected_requirement.requirement_id}_"
                    f"{suggestion.claim_id}"
                ),
            )

        with col2:
            st.write(f"**Policy:** {suggestion.policy_name}")
            st.write(f"**Policy ID:** `{suggestion.policy_id}`")
            st.write(f"**Objective:** `{suggestion.objective_id}`")
            st.write(suggestion.objective_description)

        if selected:
            selected_claim_ids.append(suggestion.claim_id)


# ---------------------------------------------------------------------------
# Human approval
# ---------------------------------------------------------------------------

st.markdown("## Human Approval")

if st.button("Approve Selected Claims"):

    approved_suggestions = approval_engine.approve_claims(
        suggestions=suggestions,
        approved_claim_ids=selected_claim_ids,
    )

    st.session_state["approved_claim_ids"] = [
        suggestion.claim_id
        for suggestion in approved_suggestions
    ]

    st.success(
        "Approved claims: "
        + ", ".join(st.session_state["approved_claim_ids"])
    )


approved_claim_ids = st.session_state.get(
    "approved_claim_ids",
    selected_requirement.claim_ids,
)

st.markdown("### Current Assurance Scope")

if approved_claim_ids:
    st.write(", ".join(approved_claim_ids))
else:
    st.warning("No claims approved yet.")


# ---------------------------------------------------------------------------
# Assurance execution
# ---------------------------------------------------------------------------

if approved_claim_ids:

    if st.button("Run Assurance"):

        result = run_assurance_for_requirement(
            selected_requirement,
            approved_claim_ids,
        )

        st.session_state["last_assurance_result"] = result


if "last_assurance_result" in st.session_state:

    st.divider()

    render_requirement_result(
        st.session_state["last_assurance_result"]
    )
