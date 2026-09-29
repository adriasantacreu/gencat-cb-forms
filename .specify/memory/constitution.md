# Constitució de Gencat CB Forms

Regles del workspace (`/mnt/data/workspace/AGENTS.md`) per sobre de tot: català, confirmar el que és destructiu o visible per a alumnes, títols sempre en *Sentence case*.

## Principis

### I. Fidelitat verbatim a les proves oficials
Enunciats, dades, gràfics i respostes han de coincidir al 100 % amb els PDF oficials de la Generalitat (CB 4t ESO, avaluació diagnòstica 2n ESO). Res s'inventa ni s'aproxima.

### II. Unitat = activitat; cada ítem té la seva captura
Una activitat = context + ítems (i sub-ítems). Cada ítem porta la seva pròpia captura, mai la del pare ni la d'un altre ítem, i el context es conserva a part.

### III. Esquema comú amb `pau-catalog`
Mateixos camps (`id, etapa, materia, any, convocatoria, serie, activitat_id, numero, pare, punts, bloc, tema, enunciat_text, solucio_text, enunciat_img, solucio_img, context_img, font_pdf, pag`). El pla mestre és `docs/plans/2026-09-29_proves-oficials-refet.md` del workspace.

### IV. Res no és correcte fins que el `check` ho valida
`cb check` (recompte per prova = registre, 0 captures repetides, auditoria OCR i de marges 100 % PASS) i un full de miniatures revisat per l'Adrià. Cap ✓ sense evidència.

### V. Reutilització
`answers_registry.py` (respostes validades), `auditor.py`, segmentador PyMuPDF + OpenCV. Només les 18 proves ja existents; no se'n descarreguen de noves.

### VI. Estat viu
Seguiment a `specs/001-cb-catalog/tasks.md`; decisions a `plan.md`.

**Version**: 1.0.0 | **Ratified**: 2026-09-29
