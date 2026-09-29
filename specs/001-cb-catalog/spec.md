# Especificació de la funcionalitat: BD de Competències Bàsiques (CCBB)

**Branca**: `001-cb-catalog` · **Creada**: 2026-09-29 · **Estat**: Esborrany (pendent de validació de l'Adrià)

**Entrada**: fase 3 de `docs/plans/2026-09-29_proves-oficials-refet.md`. Decisions ja preses (no replantejar): D3 (la BD viu a `gencat-cb-forms`, ordre `cb index`), D4 (PAU i CCBB surten junts al mostrari), només les 18 proves que ja tenim.

## Context

`gencat-cb-forms` sap crear un Google Form autocorregible per prova (segmentador, auditor i `answers_registry.py` amb 582 respostes validades), però **no té cap BD**: les captures auditades vivien a `scratch/crops_*_clean` i només en queden les de 2n d'ESO (6 de 18 proves); les de 4t s'han perdut i s'han de regenerar. El registre defineix a mà l'estructura de cada prova (seccions, imatges de context amb noms triats a mà, ítems). El segmentador geomètric automàtic és genèric i no en reprodueix la granularitat (contextos compartits per subconjunts d'ítems, sub-ítems `item_6_1`). Un intent anterior (`banc-proves-oficials`) va reutilitzar la captura del pare per als sub-ítems i va deixar 410/627 textos amb només el resum de l'activitat.

**Diferència amb PAU**: a PAU la unitat és l'exercici; aquí és l'**activitat** (context + ítems, de vegades amb sub-ítems). Un ítem no s'entén sense el seu context, i el context es comparteix entre ítems.

## Proves cobertes (18)

| Etapa | Matèria | Anys | Ítems (registre) |
|---|---|---|---|
| 4t ESO (CB) | Matemàtiques | 2021–2026 | 178 |
| 4t ESO (CB) | Ciència i tecnologia | 2021–2026 | 217 |
| 2n ESO (avaluació de diagnòstic) | Matemàtiques | 2024–2026 | 69 |
| 2n ESO (avaluació de diagnòstic) | Ciència i tecnologia | 2024–2026 | 118 |
| | | **Total** | **582** |

Font: PDF de `docencia/materials/competencies_basiques/{2ESO,4ESO}/…` (prova + criteris). No se'n descarreguen de nous.

## Escenaris d'usuari i proves *(obligatori)*

### Història 1 — Saber que la BD és completa (Prioritat: P1)

Com a professor vull que el nombre d'ítems de cada prova a la BD sigui el del registre oficial de respostes, i que qualsevol forat sigui una excepció escrita i justificada.

**Prova independent**: `cb check` compara, per prova, ítems BD vs. registre (582 en total).

1. **Donada** una prova, **quan** s'executa `cb check`, **llavors** cada ítem del registre existeix a la BD amb la seva captura, i viceversa.
2. **Donat** un ítem sense captura o sense resposta oficial, **llavors** `cb check` falla llevat que sigui a `data/excepcions.csv` amb motiu.

### Història 2 — Cada ítem té la seva captura i el seu context (Prioritat: P1)

Com a professor vull que cada ítem i sub-ítem tingui **la seva pròpia captura**, i que el context de l'activitat sigui una imatge a part enllaçada, perquè no es repeteixi el mateix retall per a ítems diferents ni es mostri un ítem sense el que necessita.

**Prova independent**: `cb check` (captures repetides, marges, OCR) i el full de miniatures per prova.

1. **Donats** dos ítems diferents, **llavors** les seves captures no són idèntiques (0 duplicats per hash).
2. **Donat** un sub-ítem, **llavors** la seva captura no és la del pare.
3. **Donat** un ítem que depèn d'un context (compartit o no), **llavors** té `context_img` apuntant a una imatge existent, i la captura de l'ítem no conté el text del context (auditoria OCR).
4. **Donada** qualsevol captura, **llavors** té marges blancs ≤ 15 px i no conté el número/enunciat d'un altre ítem.

### Història 3 — Text i resposta oficial per a cada ítem (Prioritat: P1)

Com a professor vull text cercable de l'enunciat de cada ítem (no només de l'activitat) i la seva resposta oficial, per poder cercar i mostrar-los.

**Prova independent**: mostra de ítems al full de miniatures + `cb check` comprova que `enunciat_text` no és buit ni és el resum de l'activitat.

1. **Donat** un ítem, **llavors** `enunciat_text` prové de l'ítem (text extret del PDF o OCR) i `solucio_text` és la resposta del registre (`answers_registry.py`); s'hi afegeix la justificació de la pauta quan n'hi ha.
2. **Donat** un ítem amb resposta tipus opció múltiple, **llavors** guarda també la lletra correcta.

### Història 4 — Fer servir la BD sense repetir feina (Prioritat: P2)

Com a professor vull que `cb index` reconstrueixi tota la BD amb una sola ordre i que els Google Forms existents (18) no es trenquin.

**Prova independent**: `cb index` seguit de `cb check` és verd; `cb build` per a una prova genera el Form com abans, ara a partir de la BD.

1. **Donats** els 18 PDF i el registre, **quan** s'executa `cb index`, **llavors** es regenera `cb_catalog.db` + `crops/` sense passos manuals.
2. **Donada** la BD, **llavors** un check diari (`scripts/checks-diaris.sh`) avisa si `cb check` falla o falten captures.

## Requisits funcionals

- **FR-001** Esquema compartit amb PAU (`id, etapa, materia, any, convocatoria, serie, activitat_id, numero, pare, punts, bloc, tema, enunciat_text, solucio_text, enunciat_img, solucio_img, context_img, font_pdf, pag`), amb `serie` buit i `convocatoria` = «CB» o «AD» segons la prova.
- **FR-002** Id d'ítem: `CB_<etapa>_<MAT|CTE>_<any>_A<activitat>_I<n>` (sub-ítems: `…_I<n>_<s>`); id d'activitat: `CB_…_A<n>`.
- **FR-003** Dues taules: `activitats` (context: títol, `context_img`, pàgines) i `items` (amb `activitat_id` i `pare`); un ítem pot apuntar a un context compartit.
- **FR-004** L'estructura (quins ítems i contextos hi ha, i quins contextos són per a quins ítems) surt del registre existent i es verifica contra el PDF, no s'inventa.
- **FR-005** Captura d'ítem = només l'ítem (i les seves opcions/figures); mai el context ni els ítems veïns.
- **FR-006** `solucio_img`: només si els criteris oficials tenen una captura útil; si no, buit i documentat (la resposta del registre és la font).
- **FR-007** `bloc`/`tema`: taula `data/cb_temes.csv` per activitat (proposta per paraules clau, marcada `revisat=no` fins que l'Adrià la reveu); la competència/dimensió oficial de la pauta s'hi guarda si hi és.
- **FR-008** `cb check` verd = recompte per prova, 0 captures repetides, 0 sub-ítems amb la captura del pare, marges i OCR 100 % PASS, context enllaçat, text no buit.
- **FR-009** `cb fulls` genera per prova un PDF de miniatures (context | ítem | resposta) per a la revisió visual.
- **FR-010** Excepcions a `data/excepcions.csv` amb motiu; cap error de la font es corregeix a mà a la BD (`docs/METODOLOGIA.md`).

## Fora d'abast

- Descarregar proves noves (només les 18).
- El mostrari web (fase 5) i canvis als Forms ja creats, llevat que `cb build` passi a llegir la BD.
- Dades d'alumnes (no n'hi ha ni n'hi haurà).

## Criteris d'èxit

- **SC-001** `cb check` verd sobre les 18 proves i 582 ítems.
- **SC-002** El full de miniatures de cada prova, revisat per l'Adrià, sense captures errònies (porta de la fase 3).
- **SC-003** `cb index` + `cb check` es poden repetir en una màquina neta amb només els PDF i el registre (temps esperat < 10 min).
- **SC-004** 0 captures a `scratch/`: totes viuen a `docencia/materials/competencies_basiques/cb_catalog/crops/`.

## Riscos i preguntes obertes

1. **Estructura a mà del registre**: les imatges de context tenen noms triats a mà (`context_act1_temps`). Proposta: el registre continua sent la font de l'estructura i el segmentador ha de trobar-ne les regions al PDF; els contextos que no es trobin automàticament es marquen amb coordenades manuals a `data/overrides.csv` (com a PAU).
2. **Text dels ítems**: els PDF són vectorials (text extraïble) però hi pot haver gràfics amb text incrustat; OCR només com a reserva.
3. **`solucio_img`**: probablement no en calgui (respostes curtes al registre); vegeu FR-006.
4. **Versionar `crops/` i BD**: proposta = no (es regeneren amb `cb index`), igual que a PAU.

## Preguntes per a l'Adrià

- (a) Vols captura de la resposta/pauta oficial a cada ítem o n'hi ha prou amb la clau del registre? *(recomanat: la clau + justificació en text)*
- (b) `bloc`/`tema` per a CB: activitat → bloc (Numeració, Espai i forma, Canvi i relacions, Estadística… per a Mat; Ciències per a CTE) us serveix, o vols una altra classificació?
- (c) Confirmes no versionar `crops/` ni la BD (es regeneren amb `cb index`)?
