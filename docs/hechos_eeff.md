# Fichas EEFF BYMA (overlay del demo)

Gold del **chat RAGFlow**, no del kernel IDP. `scripts/push_hechos.py` mete estas cifras **dentro de cada EEFF** (chunk manual + prompt de todos los chats). No se sube este `.md` como documento: Show Quote tiene que citar el EEFF.

Contrato IDP (pytest, `idp_ask.py`): `recipes/financial_statement.json` + `evals/identity_v1.json`. Las cifras coinciden; **no fusionar** los archivos.

Catálogo machine-readable de este riel: `docs/hechos_eeff.json`.

## 1T26 primer trimestre 2026 — EEFF al 31 de marzo de 2026 (página 4)

- Resultado neto consolidado (RESULTADO NETO DEL PERÍODO del estado consolidado; síntesis de la estructura de resultados consolidada): 21.262.335. No usar 21.259.769 ni 22.362.983 (ejercicio anterior).
- Resultado atribuible a la participación controlante / propietarios de la controlante: 21.259.769. No es el neto consolidado.

## 2T26 segundo trimestre 2026 — EEFF al 30 de junio de 2026 (página 4)

- Resultado neto consolidado: 81.956.525. No usar 81.946.993 (eso es controlante, y también el neto del estado separado en página 45).
- Resultado atribuible a la participación controlante / propietarios: 81.946.993. Si la pregunta pide consolidado, no usar este número.

## Comparar 2T26 y 1T26

Comparación resultado neto consolidado: 2T26 = 81.956.525 (30 de junio de 2026) vs 1T26 = 21.262.335 (31 de marzo de 2026).
Comparación controlante: 2T26 = 81.946.993 vs 1T26 = 21.259.769.
