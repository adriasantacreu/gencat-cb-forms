# Pla d'implementació 001 — BD consultable de CCBB

**Spec**: `spec.md` (validada 2026-09-29)

## Disseny

- `src/catalog.py`: BD SQLite + FTS5 (`cb_catalog.db`), taules `activitats` i `items` (esquema comú amb PAU).
- `src/indexer.py` (`cb index`): per prova, llegeix `STRUCTURES`/`ANSWERS`, copia les captures de `crops_dir` a `crops/<PROVA>/`, extreu text de l'ítem del PDF (PyMuPDF; OCR Tesseract de reserva) i el registra amb `context_img` de l'activitat.
- `src/check.py` (`cb check`) i `src/fulls.py` (`cb fulls`); `cb cerca` a `cli.py`.
- Reutilitza `auditor.py` (marges/OCR) i el registre. Cap canvi a Forms ni al segmentador.
- Origen de captures: 2n ESO des de `scratch/crops_2eso*_clean`; 4t ESO **recuperades de Drive** (carpeta d'assets dels Forms) a `scratch/cb_recuperat/<crops_dir>`, i llavors indexades igual. Si no hi són → avisar abans de regenerar.
- Sortida: `docencia/materials/competencies_basiques/cb_catalog/{cb_catalog.db,crops/}` (no versionat).

## Verificació

`cb check` verd (582 ítems, 0 duplicats, auditoria 100 %) + 5 cerques + `cb fulls` per prova (porta).

## Vigilància i neteja

Check diari `cb check` a `scripts/checks-diaris.sh`. Neteja final (amb OK): `scratch/crops_*`, `scratch/cb_recuperat`.
