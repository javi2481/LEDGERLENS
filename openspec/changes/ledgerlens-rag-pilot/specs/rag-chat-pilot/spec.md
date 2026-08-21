# rag-chat-pilot Specification

## Purpose

Score a ten-question chat pilot after claim inject. Identity numbers remain kernel gold; the chat is scored for citation and abstention.

## Requirements

### Requirement: Ten labeled cases

The chat gold MUST include four identity, three narrative, two abstention, and one comparison case.

#### Scenario: Identity uses kernel value

- GIVEN the 1T26 neto identity case
- THEN expected value MUST be `21262335`
- AND expected citation MUST be the dedicated EEFF PDF, not a sidecar markdown

### Requirement: Skip without RAGFlow

`rag_eval.py` MUST exit 0 when the API is down.

#### Scenario: Notebook CI

- GIVEN no listener on the RAGFlow URL
- WHEN the eval script runs
- THEN the process MUST succeed with skip `no_ragflow`
