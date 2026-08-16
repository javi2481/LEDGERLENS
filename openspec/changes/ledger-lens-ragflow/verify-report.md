```yaml
schema: gentle-ai.verify-result/v1
evidence_revision: sha256:2a4f75db6a23ea9495bd1216c4592351a66fbafc53be05e31b5420dbab344625
verdict: fail
blockers: 1
critical_findings: 0
requirements: 1/7
scenarios: 1/11
test_command: ls examples/synthetic/*.pdf
test_exit_code: 0
test_output_hash: sha256:2a4f75db6a23ea9495bd1216c4592351a66fbafc53be05e31b5420dbab344625
build_command: bash -n scripts/up.sh
build_exit_code: 0
build_output_hash: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

> Snapshot histórico: verify en Linux ~7 GB, `ls examples/synthetic/*.pdf` (Acme Norte). No describe el demo Windows 32 GB / corpus BYMA / MinerU `demo_4`. No re-correr este verify como evidencia actual.

## Verification Report

**Change**: ledger-lens-ragflow
**Version**: N/A (delta specs; no archived baseline)
**Mode**: Standard (`strict_tdd: false`; no pytest runner)

### Completeness
| Metric | Value |
|--------|-------|
| Tasks total | 13 |
| Tasks complete | 13 |
| Tasks incomplete | 0 |

Filesystem `openspec/changes/ledger-lens-ragflow/tasks.md` has every task checked. Engram `sdd/ledger-lens-ragflow/tasks` (#116) still has unchecked boxes (planning snapshot); apply updated the OpenSpec file. Completeness is judged from the OpenSpec tasks file.

Task 5.4 itself records that this apply host (~7.4 GB, Docker not installed) skips runtime smoke.

### Build & Tests Execution
**Build**: ⚠️ Syntax check only (no application image build)
```text
bash -n scripts/up.sh
exit 0
(no output)
```
No package.json, pyproject.toml, Makefile, or go.mod. Docker image/compose build was not run (Docker not installed).

**Tests**: ✅ file-level contracts passed / ⚠️ runtime compose+E2E skipped / ❌ 0 failed
```text
ls examples/synthetic/*.pdf
exit 0
examples/synthetic/estados-financieros-acme-norte-2024.pdf
examples/synthetic/hechos-relevantes-acme-norte.pdf
examples/synthetic/informe-operativo-acme-norte-q1-2025.pdf
examples/synthetic/memoria-acme-norte-2024.pdf
```
Additional static contracts inspected in this verify session (not the envelope test_command): vendor/PIN.md tag v0.26.4; official vendor/ragflow-docker/docker-compose.yml; overlay paddleocr on ragflow with no host ports; Dockerfile PP-StructureV3 CPU port 8080; .env.example Infinity / Compose-DNS PaddleOCR / no ACCESS_TOKEN / image v0.26.4; scripts/up.sh read-only max_map_count, no eval, no executed sysctl -w, env sync, both compose files, ollama pull docs; README Spanish E2E; no app.py or ledger_lens/.

Host probe (not a substitute for compose healthy): x86_64, MemTotal 7.45 GiB, Docker not installed, Ollama not installed, pytest not installed. `vm.max_map_count` is 1048576 (≥ 262144) but the stack still cannot start here.

**Skipped on this host (explicit)**:
- `scripts/up.sh` / `docker compose ... up -d` / `docker compose ps` (no Docker; RAM < 16 GB)
- Compose healthy checks (UI `:80`, `paddleocr` up, Ollama tags)
- Manual README E2E (ingest, in-corpus Show Quote, out-of-corpus Empty response, parser-down ingest fail)
- Demo is **not** ready on this host

**Coverage**: N/A / threshold: 0% → ➖ Not available

### Spec Compliance Matrix
| Requirement | Scenario | Test | Result |
|-------------|----------|------|--------|
| document-parse / PaddleOCR remote layout parser | Successful parse via Compose DNS | `.env.example` `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`; overlay `paddleocr` on `ragflow`; no ingest runtime | ⚠️ PARTIAL |
| document-parse / PaddleOCR remote layout parser | Parser unavailable | README E2E step 5 documents visible fail; parser-down not executed | ⚠️ PARTIAL |
| knowledge-qa / Spanish cited answers | Evidence-backed Spanish answer | README E2E in-corpus + Show Quote; chat not executed | ⚠️ PARTIAL |
| knowledge-qa / No-evidence empty response | No matching or weak chunks | README out-of-corpus Empty response; chat not executed | ⚠️ PARTIAL |
| knowledge-qa / No-evidence empty response | Blank Empty response forbidden | README first-run sets non-blank Spanish Empty response; assistant not inspected at runtime | ⚠️ PARTIAL |
| local-stack / Official pin overlay Infinity | Pinned stack starts without forbidden apps | PIN v0.26.4, vendor compose, no `app.py`/`ledger_lens/`; UI `:80` not started | ⚠️ PARTIAL |
| local-stack / Host Ollama env and up script | Ollama via host-gateway and env start | `.env.example` + vendor `extra_hosts` + `up.sh` compose/pull; overlay not up | ⚠️ PARTIAL |
| local-stack / Host Ollama env and up script | Low vm.max_map_count fails fast | `scripts/up.sh` read-only check + "Demo not ready."; not executed with low map_count | ⚠️ PARTIAL |
| portfolio-local / Synthetic Spanish financial PDFs | Fixture set present and not BYMA | `ls examples/synthetic/*.pdf` + pdftotext (Acme Norte synthetic; not BYMA) | ✅ COMPLIANT |
| portfolio-local / README startup and E2E checklist | Operator starts from README | Spanish README documents `http://localhost` port 80; UI not opened | ⚠️ PARTIAL |
| portfolio-local / README startup and E2E checklist | E2E in-corpus and out-of-corpus | README checklist present; not executed | ⚠️ PARTIAL |

**Compliance summary**: 1/11 scenarios compliant (10 PARTIAL because compose healthy + manual E2E were skipped on this host)

### Correctness (Static Evidence)
| Requirement | Status | Notes |
|------------|--------|-------|
| PaddleOCR remote layout parser | ✅ Implemented (static) | Overlay `paddleocr` on `ragflow`, no host `:8080`; Dockerfile `PP-StructureV3` CPU `--port 8080`; `PADDLEOCR_API_URL=http://paddleocr:8080/layout-parsing`; no `PADDLEOCR_ACCESS_TOKEN` assignment |
| Spanish cited answers | ⚠️ Configured in README only | First-run KB/chat: Spanish, Show Quote on; runtime Q&A skipped |
| No-evidence empty response | ⚠️ Configured in README only | Required copy: `No hay evidencia suficiente en los documentos indexados para responder. No invento datos.` |
| Official pin overlay Infinity | ✅ Implemented (static) | `vendor/PIN.md` tag v0.26.4; official `vendor/ragflow-docker/`; `DOC_ENGINE=infinity`; `RAGFLOW_IMAGE=infiniflow/ragflow:v0.26.4`; `COMPOSE_PROFILES=infinity,cpu` |
| Host Ollama env and up script | ✅ Implemented (static) | `up.sh`: read-only `vm.max_map_count`, no `eval`, no executed `sysctl -w`, sync `.env` → vendor, compose both files, `ollama pull qwen2.5:1.5b` and `bge-m3`; vendor `host.docker.internal:host-gateway` |
| Synthetic Spanish financial PDFs | ✅ Implemented | Four PDFs: hechos, estados, memoria, operativo; synthetic Acme Norte; not BYMA |
| README startup and E2E checklist | ✅ Implemented (docs) | Spanish README: x86_64, ≥16 GB, Docker ≥24, Compose ≥v2.26.1, not ARM64, `OLLAMA_HOST=0.0.0.0`, Empty response, Show Quote, synthetic-only, E2E checklist |

### Coherence (Design)
| Decision | Followed? | Notes |
|----------|-----------|-------|
| Vendor docker/ v0.26.4 + overlay | ✅ Yes | `vendor/ragflow-docker/` + `docker-compose.overlay.yml` |
| DOC_ENGINE=infinity | ✅ Yes | `.env.example` |
| CPU PP-StructureV3 POST /layout-parsing | ✅ Yes | Dockerfile CMD + env algorithm |
| OCR URL Compose DNS, no host 8080 | ✅ Yes | overlay has no `ports:` |
| Host Ollama host.docker.internal | ✅ Yes | README + vendor extra_hosts; not Compose Ollama |
| Embed bge-m3 / chat qwen2.5:1.5b | ✅ Yes | `up.sh` pulls; README model providers |
| No app.py, ledger_lens/, Gradio, HF Space | ✅ Yes | Absent from product tree |
| up.sh no eval / no sysctl -w / no :8080 publish | ✅ Yes | `sysctl -w` only in error echo + README |

### Issues Found
**CRITICAL**: None

**WARNING**:
- Runtime compose healthy and manual E2E were skipped: Docker not installed, Ollama not installed, RAM 7.45 GiB < 16 GB. This host must not be treated as a working demo.
- 10/11 spec scenarios remain PARTIAL (file contracts only). Project `openspec/config.yaml` allows no pytest and skip smoke when Docker/RAM are missing; that skip still leaves spec evidence incomplete, so this report is not archive-ready.
- Engram `sdd/ledger-lens-ragflow/tasks` is stale (unchecked) relative to OpenSpec `tasks.md` (all `[x]`).

**SUGGESTION**:
- Re-run verify on an x86_64 host with ≥16 GB RAM, Docker ≥24, Compose ≥v2.26.1, and host Ollama (`OLLAMA_HOST=0.0.0.0`) before archive.
- Pin a PaddleOCR image digest later if supply-chain pinning is required (apply used `paddlepaddle==3.1.0` + `paddlex==3.7.2`).
- Ignore leftover `openspec/changes/ledger-lens-mvp/` (design already says so).

### Verdict
FAIL
File-level contracts passed; compose healthy and manual E2E were skipped on this incapable host, so the demo is not proven ready and the change is not archive-ready.
