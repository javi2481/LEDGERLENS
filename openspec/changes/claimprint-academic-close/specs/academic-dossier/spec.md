# academic-dossier Specification

## Purpose

Export an academic HTML dossier of accepted identity facts, gold Q&A with citations, abstentions, and a HITL annex. Narrative eval cases stay out; they belong to RAGFlow chat.

## Requirements

### Requirement: Published facts use accepted claims only

The facts section MUST list only publishable claims (accept or default-accept). Rejected and flagged claims MUST NOT appear there.

#### Scenario: Reject hidden in facts

- GIVEN claims including 1T26 consolidated net income `21262335`
- AND that claim is `reject`ed
- WHEN the dossier HTML is rendered
- THEN the facts section MUST NOT contain `21262335` as a published fact

### Requirement: Gold identity Q&A cites source_text

Identity eval cases (not `narrative`) MUST appear as question, value, identity_key, page, and claim `source_text` when a matching accepted claim exists.

#### Scenario: 1T26 neto gold

- GIVEN MinerU fixtures and default accept verdicts
- WHEN the dossier is rendered from corpus claims and identity_v1 gold
- THEN the HTML MUST contain `21262335` and the matching `identity_key` for consolidado neto 1T26

### Requirement: Narrative cases are omitted

Eval cases with `route` `narrative` MUST NOT appear in the Q&A section.

#### Scenario: Skip narrative

- GIVEN identity_v1 cases including `route: narrative`
- WHEN the dossier Q&A rows are built
- THEN no narrative question MUST be included

### Requirement: Abstentions are a separate section

Abstain eval cases MUST be listed as questions the system refuses, not as invented values.

#### Scenario: YPF abstain

- GIVEN an abstain gold question about YPF
- WHEN the dossier is rendered
- THEN that question MUST appear in the abstention section
- AND MUST NOT be paired with a numeric claim value

### Requirement: Output is local HTML

The CLI MUST write under `outputs/` (gitignored). It MUST NOT call RAGFlow.

#### Scenario: No RAGFlow import

- GIVEN `scripts/informe.py`
- WHEN the module is loaded
- THEN it MUST NOT import RAGFlow client code
