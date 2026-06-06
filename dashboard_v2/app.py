"""
AI Decision Assurance Platform Dashboard

Visible flow:

Requirement
↓
Existing Executable Claims
↓
Gemini Claim Discovery
↓
PML Claim Mapping Agent
↓
AI Decision Trace: Reason / Plan / Act
↓
Coverage Assessment
↓
PML Governance Review
↓
Current Governed Assurance Scope
↓
Dynatrace Evidence Collection
↓
Claim Assurance
↓
Requirement Assurance
↓
Assurance Explanation
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "backend" / "app_v2"
sys.path.append(str(APP_DIR))


from assurance_explanation_engine import AssuranceExplanationEngine
from claim_assurance_engine import ClaimAssuranceEngine
from claim_discovery_agent import ClaimDiscoveryAgent
from claim_library import load_claim_library
from claim_models import ApprovedClaim
from dynatrace_adapter import DynatraceEvidenceAdapter
from dynatrace_provider import DynatraceProvider
from evidence_collection_engine import EvidenceCollectionEngine
from pml_claim_mapping_agent import PMLClaimMappingAgent
from pml_governance_router import route_claim_review_package
from requirement_assurance_engine import RequirementAssuranceEngine
from requirement_library import load_requirements


st.set_page_config(
    page_title="AI Decision Assurance Platform",
    layout="wide",
)

st.title("AI Decision Assurance Platform")
st.caption(
    "AI reasons over governance knowledge, maps discovered claims, "
    "plans assurance coverage, and acts through governed Dynatrace evidence."
)


@dataclass
class DashboardClaimReviewPackage:
    claim_id: str
    category: str
    coverage_status: str


def status_badge(status: str) -> str:
    if status == "VERIFIED":
        return "✅ VERIFIED"
    if status == "PARTIALLY_ASSURED":
        return "⚠️ PARTIALLY ASSURED"
    if status == "FAILED":
        return "❌ FAILED"
    if status == "INSUFFICIENT_EVIDENCE":
        return "⚠️ INSUFFICIENT EVIDENCE"
    return status


def coverage_badge(status: str) -> str:
    if status == "SUPPORTED":
        return "✅ SUPPORTED"
    if status == "MAPPING_CANDIDATE":
        return "🧭 MAPPING CANDIDATE"
    if status == "COVERAGE_GAP":
        return "⚠️ COVERAGE GAP"
    return status


def governance_action_label(coverage_status: str) -> str:
    if coverage_status == "SUPPORTED":
        return "Approve for assurance"
    if coverage_status == "MAPPING_CANDIDATE":
        return "Approve mapping"
    if coverage_status == "COVERAGE_GAP":
        return "Classify / reject / defer"
    return "Manual review"


def get_claim_by_id(claims, claim_id):
    return next(claim for claim in claims if claim.claim_id == claim_id)


def build_claim_library_index(claims):
    return {claim.claim_id for claim in claims}


def calculate_coverage_score(assessed_claims) -> int:
    if not assessed_claims:
        return 0

    supported = [
        item
        for item in assessed_claims
        if item["coverage_status"] in ["SUPPORTED", "MAPPING_CANDIDATE"]
    ]

    return round((len(supported) / len(assessed_claims)) * 100)


@st.cache_data(ttl=60)
def recommend_pml_mapping(discovered_claim: str, governed_claims: list[str]):
    agent = PMLClaimMappingAgent()
    return agent.recommend_mapping(
        discovered_claim=discovered_claim,
        governed_claims=governed_claims,
    )


def assess_claim_coverage(suggestions, claim_library_ids):
    """
    Preserve two identities:
    - discovered_claim_id: Gemini output
    - governed_claim_id: executable claim library target

    The evidence engine only receives governed_claim_id.
    """

    assessed_claims = []
    governed_claims = list(claim_library_ids)

    for suggestion in suggestions:
        discovered_claim_id = suggestion.claim_id
        direct_match = discovered_claim_id in claim_library_ids

        mapping_recommendation = None
        governed_claim_id = discovered_claim_id
        mapping_status = "NOT_REQUIRED"

        if direct_match:
            coverage_status = "SUPPORTED"
        else:
            mapping_recommendation = recommend_pml_mapping(
                discovered_claim=discovered_claim_id,
                governed_claims=governed_claims,
            )

            candidate_mapping = mapping_recommendation.get("mapped_claim")
            confidence = mapping_recommendation.get("confidence", 0.0)

            if candidate_mapping in claim_library_ids and confidence >= 0.7:
                governed_claim_id = candidate_mapping
                coverage_status = "MAPPING_CANDIDATE"
                mapping_status = "PML_APPROVAL_REQUIRED"
            else:
                coverage_status = "COVERAGE_GAP"
                mapping_status = "NO_MAPPING_FOUND"

        route_status = (
            "SUPPORTED"
            if coverage_status in ["SUPPORTED", "MAPPING_CANDIDATE"]
            else "COVERAGE_GAP"
        )

        package = DashboardClaimReviewPackage(
            claim_id=governed_claim_id,
            category="Availability",
            coverage_status=route_status,
        )

        governance_route = route_claim_review_package(package)

        assessed_claims.append(
            {
                "suggestion": suggestion,
                "claim_id": governed_claim_id,
                "discovered_claim_id": discovered_claim_id,
                "governed_claim_id": governed_claim_id,
                "mapped_from": (
                    discovered_claim_id
                    if discovered_claim_id != governed_claim_id
                    else None
                ),
                "coverage_status": coverage_status,
                "route_status": route_status,
                "governance_route": governance_route,
                "mapping_status": mapping_status,
                "mapping_recommendation": mapping_recommendation,
                "source_type": "GEMINI_DISCOVERED_CLAIM",
            }
        )

    return assessed_claims


def add_existing_executable_claims(
    assessed_claims,
    selected_requirement,
    claim_library_ids,
):
    existing_governed_claim_ids = {
        item["governed_claim_id"]
        for item in assessed_claims
    }

    for claim_id in selected_requirement.claim_ids:
        if claim_id not in existing_governed_claim_ids and claim_id in claim_library_ids:

            suggestion = type(
                "ExistingExecutableClaimSuggestion",
                (),
                {
                    "claim_id": claim_id,
                    "policy_id": "CLAIM_LIBRARY",
                    "policy_name": "Existing Governed Claim Library",
                    "objective_id": "EXECUTABLE_ASSURANCE_SCOPE",
                    "objective_description": (
                        "Existing approved claim already available in the "
                        "governed executable claim library."
                    ),
                    "requirement": selected_requirement.description,
                    "rationale": (
                        "This claim is part of the existing governed assurance "
                        "scope for the selected requirement."
                    ),
                    "business_impact": (
                        "If this claim is not assured, the requirement may "
                        "not be fully supported by runtime evidence."
                    ),
                    "governance_need": (
                        "PML may approve this existing claim for evidence "
                        "collection and assurance evaluation."
                    ),
                },
            )()

            package = DashboardClaimReviewPackage(
                claim_id=claim_id,
                category="Availability",
                coverage_status="SUPPORTED",
            )

            governance_route = route_claim_review_package(package)

            assessed_claims.append(
                {
                    "suggestion": suggestion,
                    "claim_id": claim_id,
                    "discovered_claim_id": claim_id,
                    "governed_claim_id": claim_id,
                    "mapped_from": None,
                    "coverage_status": "SUPPORTED",
                    "route_status": "SUPPORTED",
                    "governance_route": governance_route,
                    "mapping_status": "NOT_REQUIRED",
                    "mapping_recommendation": None,
                    "source_type": "EXISTING_EXECUTABLE_CLAIM",
                }
            )

    return assessed_claims


def render_ai_explanation(suggestion):
    st.markdown("#### AI Explanation")

    st.write(
        "**Rationale:** "
        + getattr(suggestion, "rationale", suggestion.objective_description)
    )

    st.write(
        "**Business Impact:** "
        + getattr(
            suggestion,
            "business_impact",
            "If this claim is not assured, the requirement may not be fully "
            "supported by observable evidence.",
        )
    )

    st.write(
        "**Governance Need:** "
        + getattr(
            suggestion,
            "governance_need",
            "PML must classify this claim before execution.",
        )
    )


def render_ai_decision_trace(
    selected_requirement,
    assessed_claims,
    approved_claim_ids,
):
    existing_claims = [
        item
        for item in assessed_claims
        if item.get("source_type") == "EXISTING_EXECUTABLE_CLAIM"
    ]

    gemini_claims = [
        item
        for item in assessed_claims
        if item.get("source_type") == "GEMINI_DISCOVERED_CLAIM"
    ]

    supported_claims = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "SUPPORTED"
    ]

    mapping_candidates = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "MAPPING_CANDIDATE"
    ]

    coverage_gaps = [
        item
        for item in assessed_claims
        if item["coverage_status"] == "COVERAGE_GAP"
    ]

    st.markdown("## AI Decision Trace")

    reason_col, plan_col, act_col = st.columns(3)

    with reason_col:
        st.subheader("Reason")
        st.write(
            "Gemini reasons over the requirement and claim patterns retrieved "
            "from the knowledge base."
        )
        st.metric("Gemini Claims", len(gemini_claims))
        st.metric("Existing Executable Claims", len(existing_claims))

    with plan_col:
        st.subheader("Plan")
        st.write(
            "The platform plans assurance by separating executable claims, "
            "mapping candidates, and coverage gaps."
        )
        st.metric("Supported Claims", len(supported_claims))
        st.metric("Mapping Candidates", len(mapping_candidates))
        st.metric("Coverage Gaps", len(coverage_gaps))

    with act_col:
        st.subheader("Act")
        st.write(
            "The platform acts only through governed workflow: PML review "
            "first, then runtime evidence collection."
        )
        st.metric("Approved for Evidence", len(approved_claim_ids))
        st.write("Dynatrace evidence is queried only for approved claims.")


def render_governed_assurance_scope(
    approved_governed_claim_ids,
    assessed_claims,
):
    st.markdown("### Approved Claim Details")

    if not approved_governed_claim_ids:
        st.warning("No supported claims approved yet.")
        return

    approved_items = [
        item
        for item in assessed_claims
        if item["governed_claim_id"] in approved_governed_claim_ids
    ]

    if not approved_items:
        st.warning(
            "Approved claim IDs exist, but none match the currently assessed "
            "claims."
        )
        return

    for item in approved_items:
        suggestion = item["suggestion"]

        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            col1.write(
                f"**Discovered Claim:** `{item['discovered_claim_id']}`"
            )
            col2.write(
                f"**Governed Claim:** `{item['governed_claim_id']}`"
            )
            col3.write(
                f"**Coverage:** {coverage_badge(item['coverage_status'])}"
            )

            st.write(f"**Route:** `{item['governance_route']}`")
            st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

            if item.get("mapped_from"):
                mapping = item.get("mapping_recommendation") or {}

                st.info(
                    f"PML mapping approved for assurance scope. "
                    f"`{item['mapped_from']}` is normalized into "
                    f"`{item['governed_claim_id']}`."
                )

                st.write(
                    "**Mapping Confidence:** "
                    + str(mapping.get("confidence", "N/A"))
                )

                st.write(
                    "**Mapping Rationale:** "
                    + mapping.get("rationale", "No rationale provided.")
                )

            st.write(f"**Discovery Source:** {suggestion.policy_name}")
            st.write(f"**Objective:** `{suggestion.objective_id}`")

            render_ai_explanation(suggestion)

            st.markdown("#### Evidence Engine Handoff")
            st.success(
                "Approved for evidence collection. The evidence engine will "
                f"execute governed claim `{item['governed_claim_id']}`."
            )


@st.cache_data(ttl=60)
def load_runtime_reality():
    provider = DynatraceProvider()
    return provider.get_runtime_reality().to_dict()


@st.cache_data(ttl=60)
def discover_claims_with_gemini(requirement_text: str):
    agent = ClaimDiscoveryAgent()
    return agent.discover(requirement_text)


def build_fallback_suggestions(selected_requirement):
    suggestions = []

    for claim_id in selected_requirement.claim_ids:
        suggestion = type(
            "FallbackClaimSuggestion",
            (),
            {
                "claim_id": claim_id,
                "policy_id": "FALLBACK",
                "policy_name": "Requirement Claim Mapping",
                "objective_id": "REQUIREMENT_DEFAULT",
                "objective_description": (
                    "Fallback claim from requirement configuration."
                ),
                "requirement": selected_requirement.description,
                "rationale": (
                    "Fallback claim mapped from requirement configuration."
                ),
                "business_impact": (
                    "If this claim is not assured, the requirement may not be "
                    "fully supported by observable evidence."
                ),
                "governance_need": (
                    "PML should review whether this claim remains in the "
                    "assurance scope."
                ),
            },
        )()

        suggestions.append(suggestion)

    return suggestions


def run_assurance_for_requirement(requirement, approved_governed_claim_ids):
    claims = load_claim_library()
    runtime_reality = load_runtime_reality()

    adapter = DynatraceEvidenceAdapter(runtime_reality)
    collection_engine = EvidenceCollectionEngine(adapter)

    claim_assurance_engine = ClaimAssuranceEngine()
    requirement_assurance_engine = RequirementAssuranceEngine()

    claim_results = []
    evidence_by_claim = {}

    for governed_claim_id in approved_governed_claim_ids:
        claim = get_claim_by_id(claims, governed_claim_id)

        approved_claim = ApprovedClaim(
            claim=claim,
            target_name="easyTravel-Business",
            thresholds={},
        )

        evidence_records = collection_engine.collect_evidence(approved_claim)

        claim_result = claim_assurance_engine.evaluate(
            approved_claim,
            evidence_records,
        )

        claim_results.append(claim_result)
        evidence_by_claim[governed_claim_id] = evidence_records

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

        col1.metric("Verified Claims", requirement_result.verified_claims)
        col2.metric(
            "Insufficient Evidence",
            requirement_result.insufficient_claims,
        )
        col3.metric("Failed Claims", requirement_result.failed_claims)

        st.markdown("#### Claim Assurance Detail")

        for claim_result in requirement_result.claim_results:
            render_claim_result(
                claim_result,
                evidence_by_claim,
            )

    render_assurance_explanation(requirement_result)


# ---------------------------------------------------------------------------
# Main dashboard
# ---------------------------------------------------------------------------

requirements = load_requirements()
claims = load_claim_library()
claim_library_ids = build_claim_library_index(claims)

selected_requirement = st.selectbox(
    "Select Requirement",
    requirements,
    format_func=lambda requirement: (
        f"{requirement.requirement_id} - {requirement.title}"
    ),
)

st.markdown("## Requirement")
st.write(selected_requirement.description)


st.markdown("## Gemini Claim Discovery")

st.info(
    "Gemini reasons over the selected requirement and known claim patterns "
    "retrieved from the knowledge base to suggest assurance claims."
)

try:
    suggestions = discover_claims_with_gemini(
        selected_requirement.description
    )

    st.success("Gemini claim discovery completed.")

except Exception as exc:
    st.warning(
        "Gemini claim discovery failed. Falling back to requirement claim IDs."
    )
    st.code(str(exc))

    suggestions = build_fallback_suggestions(selected_requirement)


assessed_claims = assess_claim_coverage(
    suggestions=suggestions,
    claim_library_ids=claim_library_ids,
)

assessed_claims = add_existing_executable_claims(
    assessed_claims=assessed_claims,
    selected_requirement=selected_requirement,
    claim_library_ids=claim_library_ids,
)


approved_governed_claim_ids = st.session_state.get(
    "approved_governed_claim_ids",
    [],
)

if not approved_governed_claim_ids:
    approved_governed_claim_ids = [
        item["governed_claim_id"]
        for item in assessed_claims
        if item["coverage_status"] in ["SUPPORTED", "MAPPING_CANDIDATE"]
    ]


render_ai_decision_trace(
    selected_requirement=selected_requirement,
    assessed_claims=assessed_claims,
    approved_claim_ids=approved_governed_claim_ids,
)


supported_claims = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "SUPPORTED"
]

mapping_candidates = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "MAPPING_CANDIDATE"
]

coverage_gaps = [
    item
    for item in assessed_claims
    if item["coverage_status"] == "COVERAGE_GAP"
]

coverage_score = calculate_coverage_score(assessed_claims)

st.markdown("## Governance Coverage Summary")

summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)

summary_col1.metric("Total Claims in Review", len(assessed_claims))
summary_col2.metric("Supported Claims", len(supported_claims))
summary_col3.metric("Mapping Candidates", len(mapping_candidates))
summary_col4.metric("Coverage Gaps", len(coverage_gaps))
summary_col5.metric("Assurance Coverage", f"{coverage_score}%")


st.markdown("## Coverage Assessment")

st.info(
    "This section shows both existing executable claims and Gemini-discovered "
    "claims. Discovered claim names are preserved. Mapped governed claims are "
    "used only for execution."
)

for item in assessed_claims:
    suggestion = item["suggestion"]

    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([1.5, 1.5, 2, 2])

        col1.write(
            f"**Discovered Claim:** `{item['discovered_claim_id']}`"
        )
        col2.write(
            f"**Governed Claim:** `{item['governed_claim_id']}`"
        )
        col3.write(f"**Coverage:** {coverage_badge(item['coverage_status'])}")
        col4.write(
            f"**PML Action:** "
            f"{governance_action_label(item['coverage_status'])}"
        )

        st.write(f"**Route:** `{item['governance_route']}`")
        st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

        if item.get("mapped_from"):
            mapping = item.get("mapping_recommendation") or {}

            st.info(
                f"PML Claim Mapping Agent recommends mapping "
                f"`{item['mapped_from']}` → `{item['governed_claim_id']}` "
                f"with confidence `{mapping.get('confidence', 'N/A')}`."
            )

            st.write(
                "**Mapping Rationale:** "
                + mapping.get("rationale", "No rationale provided.")
            )

        st.write(f"**Discovery Source:** {suggestion.policy_name}")
        st.write(f"**Policy ID:** `{suggestion.policy_id}`")
        st.write(f"**Objective:** `{suggestion.objective_id}`")

        render_ai_explanation(suggestion)

        if item["coverage_status"] == "SUPPORTED":
            st.success(
                "This is an existing governed claim with executable "
                "assurance coverage."
            )

        elif item["coverage_status"] == "MAPPING_CANDIDATE":
            st.info(
                "This discovered claim can be normalized into an existing "
                "governed claim if PML approves the mapping."
            )

        elif item["coverage_status"] == "COVERAGE_GAP":
            st.warning(
                "This is a new or unsupported claim. It cannot enter evidence "
                "collection until PML classifies it."
            )


st.markdown("## PML Governance Review")

st.info(
    "PML approves assurance intent. Supported claims and approved mapping "
    "candidates can enter evidence collection. Coverage gaps are routed for "
    "governance classification."
)

selected_governed_claim_ids = []

for index, item in enumerate(assessed_claims):
    is_approvable = item["coverage_status"] in [
        "SUPPORTED",
        "MAPPING_CANDIDATE",
    ]

    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            selected = st.checkbox(
                item["discovered_claim_id"],
                value=(
                    item["governed_claim_id"] in approved_governed_claim_ids
                    and is_approvable
                ),
                disabled=not is_approvable,
                key=(
                    f"{selected_requirement.requirement_id}_"
                    f"pml_{index}_"
                    f"{item['discovered_claim_id']}_"
                    f"{item['governed_claim_id']}_"
                    f"{item.get('source_type', 'UNKNOWN')}"
                ),
            )

        with col2:
            st.write(
                f"**Discovered Claim:** `{item['discovered_claim_id']}`"
            )
            st.write(
                f"**Governed / Executable Claim:** "
                f"`{item['governed_claim_id']}`"
            )
            st.write(
                f"**Coverage:** "
                f"{coverage_badge(item['coverage_status'])}"
            )
            st.write(f"**Route:** `{item['governance_route']}`")
            st.write(f"**Source Type:** `{item.get('source_type', 'UNKNOWN')}`")

            if item.get("mapped_from"):
                st.info(
                    f"`{item['mapped_from']}` can be normalized into "
                    f"`{item['governed_claim_id']}` before assurance execution."
                )

            if item["coverage_status"] == "MAPPING_CANDIDATE":
                st.success(
                    "PML action: approve semantic mapping to existing "
                    "governed claim before assurance scope."
                )

            elif item["coverage_status"] == "SUPPORTED":
                st.success(
                    "PML action: approve existing governed claim for "
                    "assurance scope."
                )

            else:
                st.warning(
                    "PML action: classify as new governance claim, reject, "
                    "or defer."
                )

        if selected and is_approvable:
            selected_governed_claim_ids.append(item["governed_claim_id"])


if st.button("Approve Supported Claims and Mappings for Assurance"):
    approved_governed_claim_ids = selected_governed_claim_ids
    st.session_state["approved_governed_claim_ids"] = approved_governed_claim_ids

    if approved_governed_claim_ids:
        st.success(
            "Approved governed claims: "
            + ", ".join(approved_governed_claim_ids)
        )
    else:
        st.warning("No claims or mappings were approved.")


approved_scope_items = [
    item
    for item in assessed_claims
    if item["governed_claim_id"] in approved_governed_claim_ids
]

st.markdown("## Current Governed Assurance Scope")

scope_col1, scope_col2, scope_col3 = st.columns(3)

scope_col1.metric("Approved Governed Claims", len(approved_scope_items))
scope_col2.metric("Approved for Evidence Engine", len(approved_scope_items))
scope_col3.metric("Blocked Coverage Gaps", len(coverage_gaps))

if len(approved_scope_items) == 0:
    st.warning(
        "No executable claims are currently approved for the evidence engine. "
        "All discovered claims require governance classification or mapping."
    )
else:
    st.success(
        f"{len(approved_scope_items)} approved governed claim(s) can proceed "
        "to Dynatrace evidence collection."
    )

render_governed_assurance_scope(
    approved_governed_claim_ids=approved_governed_claim_ids,
    assessed_claims=assessed_claims,
)


st.markdown("## Evidence Plane")

with st.container(border=True):
    st.subheader("Dynatrace Runtime Evidence")

    st.info(
        "Dynatrace provides runtime evidence, but runtime evidence is not "
        "assurance by itself. A claim must be governed, executable, approved, "
        "and evaluated before it can become VERIFIED."
    )

    try:
        runtime_reality = load_runtime_reality()

        st.success("Dynatrace runtime reality loaded.")

        with st.expander("View Runtime Reality Snapshot"):
            st.json(runtime_reality)

    except Exception as exc:
        st.warning(
            "Dynatrace runtime evidence could not be loaded in the dashboard."
        )
        st.code(str(exc))


st.markdown("## Assurance Execution")

st.info(
    "Assurance is executed only for PML-approved governed claims. "
    "Coverage gaps remain in governance review."
)

if approved_governed_claim_ids:
    if st.button("Run Assurance"):
        result = run_assurance_for_requirement(
            selected_requirement,
            approved_governed_claim_ids,
        )

        st.session_state["last_assurance_result"] = result
else:
    st.warning("Approve at least one governed claim before running assurance.")


if "last_assurance_result" in st.session_state:
    st.divider()
    render_requirement_result(st.session_state["last_assurance_result"])
