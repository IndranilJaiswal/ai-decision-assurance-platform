# Changelog

## Version 0.7.0 - Gemini Reason → Plan → Govern → Act Architecture

### Overview

The AI Decision Assurance Platform has evolved from a recommendation engine into a governed assurance platform with explicit Reason, Plan, Govern, Act, and Assure layers.

---

### Gemini Reasoning Layer

Implemented Gemini-powered claim discovery.

Capabilities:

* Requirement analysis
* Assurance claim discovery
* Business impact explanation
* Coverage gap identification

Output:

* Discovered assurance claims
* Claim rationale
* Business impact statements

---

### Gemini Planning Layer

Implemented governed claim mapping.

Capabilities:

* Claim-to-library mapping
* Existing executable claim reuse
* Coverage gap identification
* Human approval workflow preparation

Output:

* Approved executable claims
* Coverage gaps
* Mapping recommendations

---

### PML Governance Layer

Implemented human-in-the-loop governance.

Capabilities:

* PML claim review
* Mapping approval
* Executable claim approval
* Coverage gap tracking

Output:

* Governed assurance scope
* Approved claims
* Blocked claims
* Coverage gap backlog

---

### Dynatrace Runtime Evidence

Integrated Dynatrace runtime evidence collection.

Capabilities:

* Service entity discovery
* Active problem retrieval
* Runtime reality normalization

Evidence Types Currently Supported:

* service_exists
* service_entity
* active_problems

Known Constraints:

* Metrics API access currently unavailable due to Dynatrace API permissions.
* Response time, failure rate, and latency metrics remain capability gaps until metrics.read access is available.

---

### Claim Assurance Engine

Implemented executable claim evaluation.

Capabilities:

* Evidence gap detection
* Claim evaluation
* Confidence scoring
* Assurance status generation

Statuses:

* VERIFIED
* FAILED
* INSUFFICIENT_EVIDENCE

---

### MCP Strategy

Implemented partner MCP architecture.

Current Partner Domain:

* Dynatrace Observability MCP

Capabilities:

* Service context requests
* Service health requests
* Latency analysis requests
* Dependency analysis requests

Purpose:

The platform translates governed assurance requirements into partner MCP evidence requests.

---

### Google ADK Agent

Implemented Gemini 3.1 Flash Lite orchestration layer.

Workflow:

Reason:
Discover claims

Plan:
Map claims

Govern:
PML approval

Act:
Partner MCP evidence requests

Assure:
Evidence evaluation

Explain:
Dashboard and assurance outputs

---

### New Files

backend/app_v2/mcp_request_models.py

backend/app_v2/test_mcp_request_models.py

agent_builder/decision_assurance_agent.py

backend/app_v2/assurance_mcp_server.py

backend/app_v2/dynatrace_mcp_server.py

---

### Architecture Status

Core Platform:
Complete

Reasoning:
Complete

Planning:
Complete

Governance:
Complete

Evidence Collection:
Partial

Assurance:
Complete

MCP Strategy:
Complete

Partner MCP Integration:
In Progress

Google Cloud Agent Builder Deployment:
Pending

cat > docs/CHANGELOG.md <<'EOF'
# Changelog

## 0.8.0 - Hosted Dynatrace Partner MCP Integration

### Added
- Added hosted Dynatrace Partner MCP connectivity.
- Added `dynatrace_partner_mcp_client.py`.
- Added `dynatrace_mcp_evidence_provider.py`.
- Added MCP evidence request models.
- Added Google ADK agent wrapper using `gemini-3.1-flash-lite`.
- Added MCP server discovery and hosted MCP validation flow.

### Verified
- Dynatrace MCP `initialize` succeeds.
- Dynatrace MCP `tools/list` succeeds.
- Dynatrace MCP exposes tools including:
  - `get-entity-id`
  - `query-problems`
  - `create-dql`
  - `execute-dql`
  - `explain-dql`
  - anomaly and forecasting tools
- `get-entity-id` returns `easyTravel-Business` service entities.
- `query-problems` returns active Davis problems.
- `create-dql` generates DQL for service health metrics.
- `execute-dql` returns service response time, failure count, p95 latency, and p99 latency time series.

### Architecture Update
The evidence path now moves from local Dynatrace REST adapter toward hosted Dynatrace Partner MCP:

Requirement  
→ Gemini claim discovery  
→ Gemini/PML claim mapping  
→ PML approval  
→ Dynatrace Partner MCP evidence request  
→ EvidenceRecord normalization  
→ Claim assurance  
→ Requirement assurance  
→ Dashboard explanation

### Known Issues
- Dashboard run-assurance integration still needs final validation with `DynatraceMCPEvidenceProvider`.
- Some legacy REST-based Dynatrace files remain and should be marked legacy or archived during cleanup.
- Cloud deployment is pending.
EOF
