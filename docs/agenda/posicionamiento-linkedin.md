# Posicionamiento LinkedIn / mercado IDP (agenda)

Tesis 2026 para hablar en público **sin** vender features que el demo no tiene. Estándar de evidencia primero; el roadmap sigue a esa prueba.

Dumps: `research/extract-reducto-10k-idp.json`, `research/search-idp-market-2026.json`.

## Tesis

El RAG financiero no se rompe en el LLM: se rompe cuando el parser pierde tablas, notas y el signo de los números ([Parsing the 10-K](https://reducto.ai/blog/10k-document), 8 jun 2026). Analogía local: EEFF BYMA y hechos relevantes.

Reducto es el **benchmark comercial** (Parse / Extract / citas / Deep Extract), no el stack a copiar. LedgerLens: MinerU `pipeline` self-host ahora. No vender KG ni hybrid como shipped.

GDP.pdf: frontier models 17–30 % de éxito en docs profesionales; parse estructurado **+9 pp** y **−13 %** tokens de reasoning ([Reducto GDP.pdf](https://reducto.ai/blog/reducto-raises-frontier-model-accuracy)).

LATAM: CEPAL US$187B emisión internacional récord 2025; Evident 2026, 20 bancos, ninguno había publicado ROI de todas sus actividades de IA. El hueco es evidencia medible, no otro copilot.

## Tres ángulos (elegir uno por post)

1. **La cita es el producto.** Número correcto, período o unidad equivocados. Reducto verifica contra el source. LedgerLens: cada KPI abre página + excerpt.
2. **Capa de evidencia LATAM.** Bonos récord + bancos sin ROI de IA. Ganador = ledger de evidencia sobre filings locales, comparable entre períodos.
3. **El vector no es una base.** “EBITDA por período, misma moneda, qué hecho cambió el outlook.” Vector = narración. Controlante vs consolidado pide identidad, no solo similitud.

## Details

| Tema | Decisión |
|------|----------|
| Disparador | Querés publicar / portfolio |
| No decir | “ya tenemos knowledge graph / RAPTOR / MinerU hybrid” hasta que esté shipped. El parser MinerU `pipeline` **sí** se puede nombrar cuando `demo_4` esté parseado |
| Competencia | Reducto, LlamaParse, ABBYY = otras capas. Nosotros: self-host + BYMA/EEFF |
| Relacionado | [mineru-pipeline.md](mineru-pipeline.md), [branding-cosmetic.md](branding-cosmetic.md) |

## Checklist

- [ ] Un post usa un ángulo, no los tres
- [ ] Cita sources nombradas (Reducto, CEPAL/Evident si se usan cifras)
- [ ] Chrome UI (branding) es independiente de este copy

## Next step

Borrador de **un** post cuando el corpus BYMA esté parseado con MinerU en `demo_4` en esta instancia. RAPTOR/KG siguen fuera del copy.
