# preprocess-orientation Specification

## Purpose

Optionally classify cover-page rotation of sample PDFs with PaddleX `PP-LCNet_x1_0_doc_ori`. Identity parse remains MinerU. CI on hosts without Paddle MUST stay green.

## Requirements

### Requirement: Skip without Paddle

When PaddleX/PaddleOCR is not importable, the probe MUST exit successfully and report a skip reason. It MUST NOT be a `requirements-dev.txt` dependency.

#### Scenario: No paddle on notebook

- GIVEN a host without paddlex
- WHEN `scripts/preprocess_probe.py` runs
- THEN the process MUST exit 0
- AND the report MUST include a skip reason such as `no_paddle`

### Requirement: Cover page only

When Paddle is available, the probe MUST consider page 1 of each sample PDF (via `pdftoppm` argv list, `shell=False`). It MUST NOT enable UVDoc unwarping.

#### Scenario: Argv not a shell string

- GIVEN a sample PDF path
- WHEN pdftoppm is invoked
- THEN the command MUST be a sequence of arguments
- AND MUST NOT use `shell=True`

### Requirement: Not identity OCR

The probe MUST NOT replace `fixtures/mineru/*.md` or call RAGFlow. Failed or skipped orientation MUST NOT invent claim values.

#### Scenario: Probe does not write fixtures

- GIVEN a probe run
- THEN `fixtures/mineru/` MUST be unchanged
