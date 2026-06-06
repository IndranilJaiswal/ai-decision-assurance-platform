# AI Decision Assurance Platform

Transforms architecture intent and Dynatrace runtime reality into evidence-backed assurance records.

## Core Narrative

Requirements → Reality → Recommendation → Assurance

## MVP Milestone 1

This version compares declared architecture against observed runtime reality and generates:

- Truth gap report
- Evidence records
- Assurance records

## Core Principle

If Dynatrace cannot observe it, the AI should not treat it as verified truth.

## Run

```bash
python backend/app_v2/main.py


Requirement
    ↓
Gemini Claim Discovery Agent
    ↓
PML Claim Mapping Agent
    ↓
Governance Review
    ↓
Approved Assurance Scope
    ↓
Dynatrace Evidence Collection
    ↓
Claim Assurance
    ↓
Requirement Assurance
    ↓
Assurance Explanation

Current Status

Reasoning Layer      ✅
Planning Layer       ✅
Governance Layer     ✅
Evidence Layer       ✅
Assurance Layer      ✅
Execution Layer      🚧 Planned
MCP Integration      🚧 Planned

cat >> README.md <<'EOF'

---

## Current Architecture: Gemini + PML + Dynatrace Partner MCP

The AI Decision Assurance Platform implements a governed assurance workflow:

```text
Requirement
    ↓
Gemini Claim Discovery
    ↓
PML Claim Mapping
    ↓
PML Governance Approval
    ↓
Dynatrace Partner MCP Evidence Collection
    ↓
Claim Assurance Engine
    ↓
Requirement Assurance Engine
    ↓
Dashboard Explanation
