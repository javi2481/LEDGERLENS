#!/usr/bin/env python3
"""Write four synthetic Spanish financial PDFs (not real BYMA filings)."""
from __future__ import annotations

from pathlib import Path


def pdf_string(text: str) -> str:
    raw = text.encode("cp1252", errors="replace")
    out: list[str] = []
    for byte in raw:
        if byte in (0x28, 0x29, 0x5C):
            out.append("\\" + chr(byte))
        elif 32 <= byte < 127:
            out.append(chr(byte))
        else:
            out.append(f"\\{byte:03o}")
    return "".join(out)


def make_pdf(path: Path, title: str, paragraphs: list[str]) -> None:
    lines = [title, ""] + paragraphs
    content_cmds = ["BT", "/F1 12 Tf", "50 760 Td"]
    first = True
    for line in lines:
        encoded = pdf_string(line)
        if first:
            content_cmds.append(f"({encoded}) Tj")
            first = False
        else:
            content_cmds.append("0 -18 Td")
            content_cmds.append(f"({encoded}) Tj")
    content_cmds.append("ET")
    stream = "\n".join(content_cmds).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]

    buf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(buf))
        buf.extend(f"{i} 0 obj\n".encode("ascii"))
        buf.extend(obj)
        buf.extend(b"\nendobj\n")
    xref = len(buf)
    buf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    buf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        buf.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    buf.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode(
            "ascii"
        )
    )
    path.write_bytes(buf)


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "examples" / "synthetic"
    root.mkdir(parents=True, exist_ok=True)

    docs = [
        (
            "hechos-relevantes-acme-norte.pdf",
            "Hechos relevantes - Acme Norte S.A. (sintetico)",
            [
                "Documento de demostracion. No es un filing de BYMA ni de un emisor real.",
                "Emisor ficticio: Acme Norte S.A. CUIT 30-70999888-1.",
                "Hecho relevante del 12 de marzo de 2025: venta de la planta Rosario",
                "por ARS 1.250 millones a Logistica Pampeana S.R.L.",
                "La operacion no incluye el centro de distribucion de Cordoba.",
                "Contacto de prensa ficticio: prensa@acmenorte.example",
            ],
        ),
        (
            "estados-financieros-acme-norte-2024.pdf",
            "Estados financieros 2024 - Acme Norte S.A. (sintetico)",
            [
                "Documento de demostracion. Cifras inventadas. No es un balance real.",
                "Periodo: ejercicio cerrado el 31 de diciembre de 2024.",
                "Ingresos netos: ARS 4.800 millones.",
                "EBITDA: ARS 720 millones.",
                "Resultado neto: ARS 310 millones.",
                "Patrimonio neto: ARS 2.100 millones.",
                "Caja y equivalentes: ARS 180 millones.",
            ],
        ),
        (
            "memoria-acme-norte-2024.pdf",
            "Memoria anual 2024 - Acme Norte S.A. (sintetico)",
            [
                "Documento de demostracion. No describe una sociedad cotizante real.",
                "La memoria resume la estrategia de digitalizacion del deposito fiscal.",
                "Dotacion al cierre: 120 empleados en Cordoba y 40 en Rosario.",
                "Proyecto principal: torre de control logistico en el predio de Cordoba.",
                "No se realizaron pagos de dividendos en el ejercicio 2024.",
            ],
        ),
        (
            "informe-operativo-acme-norte-q1-2025.pdf",
            "Informe operativo Q1 2025 - Acme Norte S.A. (sintetico)",
            [
                "Documento de demostracion. Indicadores inventados. No es un parte real.",
                "Periodo: enero-marzo 2025. Planta de referencia: Zarate.",
                "Pallets despachados: 18.400.",
                "Merma operativa: 3.2 por ciento.",
                "Ocupacion de muelles: 81 por ciento.",
                "Incidentes de seguridad reportados: 0.",
            ],
        ),
    ]

    for name, title, paras in docs:
        make_pdf(root / name, title, paras)
        print("wrote", root / name)


if __name__ == "__main__":
    main()
