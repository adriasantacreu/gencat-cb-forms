# Especificació de la funcionalitat: BD consultable de CCBB

**Branca**: `001-cb-catalog` · **Creada**: 2026-09-29 · **Estat**: Validada per l'Adrià (2026-09-29)

**Entrada**: fase 3 de `docs/plans/2026-09-29_proves-oficials-refet.md`. Decisions fixades: D3 (la BD viu aquí, ordre `cb index`), D4, només les 18 proves existents.

## Objectiu (dues coses, i ja n'hi ha una de feta)

- **A. BD consultable per paraules clau** (captures + text/OCR), amb el mateix esquema que PAU. *Això és el que falta.*
- **B. Captures netes per als Google Forms.** *Ja fet i auditat* (18 Forms, `answers_registry.py` amb 582 ítems). **No es toca**: aquesta feina és l'entrada de la BD, no s'hi refà.

## Decisió (Adrià, 2026-09-29)

Les captures són **seccionades** (context, ítem 1, ítem 2…), tal com ja necessiten els Forms. **No es fa cap captura global de l'exercici** (seria la pàgina sencera). Un exercici és el conjunt de captures que comparteixen `activitat_id`: la BD les lliga i qui consumeix (cerca, mostrari) les apila en pantalla.

**Sub-preguntes**: al registre, els ítems amb `_` (`4_1`, `4_2`…) són sub-preguntes d'un ítem que es responen **sobre la captura de l'ítem pare**; no tenen captura pròpia. A la BD són files amb `pare` i comparteixen la `enunciat_img` del pare (això és correcte, no un duplicat). Captura pròpia: cada ítem principal i cada context.

## Principi: aprofitar, no refer

| Ja existeix | Ús |
|---|---|
| `answers_registry.py` (estructura: activitats, contextos, ítems, sub-ítems + clau) | Font de veritat del recompte i de l'estructura |
| Captures auditades de 2n ESO (`scratch/crops_2eso*_clean`, 6 proves) | S'importen tal qual a `crops/` |
| Captures auditades de 4t ESO (12 proves) | **Perdudes localment**; recuperades de la carpeta `_Assets_Imatges` de Drive (verificat: 607/607 captures del registre hi són, prefixades per prova) |
| `auditor.py`, `retalla_cb_perfecte.py` | Verificació, sense codi nou |

Les captures de `banc-proves-oficials/.cache/cb` **no** serveixen (segmentació automàtica genèrica: p. ex. 25 ítems per CTE quan el registre en té 27–49).

## Proves (18, 582 ítems)

4t ESO Mat 2021–26 (178) · 4t ESO CTE 2021–26 (217) · 2n ESO Mat 2024–26 (69) · 2n ESO CTE 2024–26 (118). Font: `docencia/materials/competencies_basiques/`.

## Històries

1. **P1 — Cercar.** `cb cerca "energia" --etapa 4ESO` dona ítems amb enunciat, captura, context i resposta. *Prova*: 5 cerques fixades amb resultats revisats.
2. **P1 — BD completa.** `cb index` importa captures + registre i extreu el text (PDF; OCR de reserva) de cada ítem. `cb check`: 582 ítems = registre, cada ítem amb captura i text no buit, 0 captures repetides entre captures d'ítems diferents, auditoria de marges/OCR (`auditor.py`) 100 % PASS. Excepcions escrites amb motiu.
3. **P1 — Revisió ràpida.** `cb fulls` genera per prova un full de miniatures (context | ítem | resposta) per a la porta.
4. **P2 — Vigilància.** `cb check` al check diari.

## Requisits clau

- Esquema comú amb PAU (`id, etapa, materia, any, activitat_id, numero, pare, punts, bloc, tema, enunciat_text, solucio_text, enunciat_img, solucio_img, context_img, font_pdf, pag`). Dues taules: `activitats` (context) i `items`.
- Ids: `CB_<etapa>_<MAT|CTE>_<any>_A<n>_I<n>[_<s>]`.
- `solucio_text` = clau del registre (+ lletra correcta); sense captura de pauta.
- `bloc/tema` per activitat: proposta per paraules clau, `revisat=no` fins que l'Adrià la reveu.
- `crops/` i BD no es versionen: `cb index` els reconstrueix.
- Ni Forms ni captures existents es modifiquen.

## Riscos

1. Que les imatges de 4t no siguin recuperables de Drive → es regeneren amb l'estructura del registre (més feina; s'avisa abans).
2. Text d'ítems amb gràfics: OCR només on el PDF no té text.

## Decisions preses

- Bloc/tema per activitat (proposta, `revisat=no`); `crops/` i BD no es versionen.
