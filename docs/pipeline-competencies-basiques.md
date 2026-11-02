# De PDF Oficial de la Generalitat a Google Forms Autocorregible en Segons: Arquitectura d'un Pipeline Agentic

**Autor:** Adrià Santacreu (amb assistència d'Antigravity / Google DeepMind Agentic AI)  
**Data:** Setembre 2026  
**Context:** Institut Escola Sant Pol de Mar — Curs 2026/2027  
**Repositori central:** `adriasantacreu/workspace`  
**Repositori públic de codi obert:** [`github.com/adriasantacreu/gencat-cb-forms`](https://github.com/adriasantacreu/gencat-cb-forms)

---

## 1. El Repte: Digitalització Rigorosa sense Treball Manual

Cada curs, el Departament d'Educació de la Generalitat de Catalunya publica les proves oficials d'Avaluació Diagnòstica (2n d'ESO) i Competències Bàsiques (4t d'ESO) en format PDF. Són proves d'entre 16 i 20 pàgines, amb un format editorial ric: gràfics estadístics, diagrames d'enginyeria, esquemes científics, taules de dades i bateries de preguntes (opció múltiple, taules de vertader/fals i respostes obertes).

A l'hora de traslladar aquestes proves a **Google Forms** perquè l'alumnat pugui fer-les i obtenir autoavaluació immediata, el procediment tradicional requereix:
1. Retallar manualment dotzenes d'imatges (fent captures de pantalla amb eina de retall).
2. Pujar-les una a una a Google Drive.
3. Crear a mà el formulari, escrivint enunciats, pujant captures, definint les opcions i assignant les claus de correcció.
4. Temps estimat per prova: **2-3 hores de feina feixuga i propensa a errors**.

L'objectiu d'aquest projecte ha estat dissenyar un **pipeline totalment automatitzat, rígidament auditabilitzat i lliure d'errors humans**, combinant scripts Python especialitzats, processament d'imatge i visió per computador, OCR amb Tesseract, i orquestració d'un agent d'IA autònom en parella de programació (*pair programming*).

---

## 2. Arquitectura del Sistema

El pipeline s'estructura en quatre capes independents i desacoblades:

```
[ PDF Oficial Gencat ]
         │
         ▼
┌───────────────────────────────────────────────┐
│ 1. Descàrrega i Ingesta (descarrega_cb.py)    │
│    - Descàrrega directa des d'avaluacio.gencat│
│    - Arxiu canònic a docencia/materials/      │
└───────────────────────────────────────────────┘
         │
         ▼
┌───────────────────────────────────────────────┐
│ 2. Motor de Retall (retalla_cb_perfecte.py)   │
│    - PyMuPDF per a segmentació vectorial      │
│    - OpenCV autocrop_tight(pad=10)            │
│    - Eliminació total de vores blanques       │
└───────────────────────────────────────────────┘
         │
         ▼
┌───────────────────────────────────────────────┐
│ 3. Auditoria Estricta (audita_cb.py)          │
│    - Comprovació de marges (< 15 px)          │
│    - OCR Tesseract per detectar contaminació  │
│      (zero enunciats d'ítem a les imatges de  │
│       context)                                │
│    - Verificació d'integritat 100% ítems      │
└───────────────────────────────────────────────┘
         │ (Només si 100% PASS)
         ▼
┌───────────────────────────────────────────────┐
│ 4. Generació Forms API (crea_formulari_cb.py) │
│    - Pujada transparent a Google Drive        │
│    - Construcció d'items via batchUpdate      │
│    - Quiz amb ponderació entera de punts      │
│    - Assignació automàtica de solucions       │
└───────────────────────────────────────────────┘
         │
         ▼
[ Formulari Google Forms enllestit per a l'alumne ]
```

---

## 3. Els Reptes Tècnics i Com els hem Solucionat

### Repte A: El "blanc fantasma" i les captures inflades
Quan es fa un retall directe d'un PDF amb coordenades rectangulars fixes, les diferències tipogràfiques o petites variacions de layout generen sovint franges blanques laterals o inferiors enormes (de vegades centenars de píxels). En una pantalla de mòbil o tauleta, una imatge amb marge buit fa que el text es vegi minúscul.

**Solució (`autocrop_tight` amb OpenCV):**
A partir del canal monocromàtic, cerquem els píxels de tinta reals (`gray < 248`) i trobem la caixa envolvent matemàtica mínima (`np.min` / `np.max`). Després afegim exactament `pad = 10 px` perimetral d'aire estètic:
```python
def autocrop_tight(img, pad=10, white_thresh=248):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    non_white = np.where(gray < white_thresh)
    if len(non_white[0]) == 0:
        return img
    y0, y1 = int(np.min(non_white[0])), int(np.max(non_white[0]))
    x0, x1 = int(np.min(non_white[1])), int(np.max(non_white[1]))
    h, w = gray.shape
    return img[max(0, y0-pad):min(h, y1+pad+1), max(0, x0-pad):min(w, x1+pad+1)]
```

### Repte B: La contaminació creuada entre Context i Pregunta
Una situació habitual: una imatge de context ("Activitat 2: La biomassa") està situada a dalt de la pàgina i a sota comença la "Pregunta 8". Si el límit inferior del context és massa generós, agafa les primeres línies de la Pregunta 8. Això provoca que quan l'alumne llegeix la introducció, ja veu part de l'enunciat que després li torna a sortir.

**Solució (Auditoria amb OCR Tesseract en català):**
A `scripts/audita_cb.py`, cada imatge de context passa per OCR automàtic (`pytesseract.image_to_string(..., lang='cat')`). Si el text conté expressions com `r"^\s*([0-9]{1,2})\.\s+([A-ZÀ-Ú][a-zà-ú]+)"` que coincideixen amb els patrons d'enunciat de les preguntes, l'auditor avorta l'execució amb un error explícit indicant quina pregunta s'ha colat.

### Repte C: Restricció de la Google Forms API (puntuacions decimals)
Moltes proves de la Generalitat tenen preguntes amb 4 subapartats valorats en 0,25 punts cadascun (per sumar 1 punt total). Tanmateix, la **Google Forms API només admet punts enters positius** (`pointValue: integer`). Intentar posar `0.25` o `0` llança un error `INVALID_ARGUMENT`.

**Solució (Ponderació natural):**
En lloc de 0,25 punts per subapartat, cada subítem s'introdueix com un ítem independent amb `pointValue: 1`. Així, una prova com 4ESO CTE 2026 que oficialment té 25 preguntes amb subítems passa a puntuar sobre 40 punts, preservant exactament el pes relatiu de cada concepte sense cap pèrdua de precisió ni problemes amb l'API.

### Repte D: L'auditoria de taules rasteritzades i la validació efímera
Als PDFs oficials de criteris del Departament, les solucions no són text seleccionable sinó imatges rasteritzades (taules escanejades amb creuetes). Un error de transcripció manual o un malentès de l'OCR pot invalidar l'avaluació d'un curs sencer.

**Solució (Contrast 1:1 i Panell d'Auditoria Efímer):**
1. **Renderització d'alta fidelitat:** Extracció de la pàgina exacta de criteris a 200-300 DPI amb PyMuPDF (`pix.save(...)`).
2. **Doble lectura i correcció:** Contrast directe de la posició de cada creueta amb el diccionari de dades `ANSWERS` (permetent enxampar i esmenar discrepàncies abans de la publicació definitiva).
3. **Visor autònom incrustat:** Generació d'un tauler HTML (`scratch/auditoria_claus_cb.html`) amb les imatges oficials convertides a Base64 i col·locades cara a cara amb les taules de respostes.
4. **Desplegament efímer amb Tailscale Funnel:** Per estalviar a l'usuari la molèstia d'obrir fitxers locals, l'agent aixeca un servidor web local i l'exposa instantàniament amb `scripts/expose.sh public 8089 10000` sota HTTPS certificat oficial (`capiserver.tailba0ca9.ts.net:10000`). Un cop l'usuari valida el resultat des del seu mòbil o navegador, el port es tanca immediatament (`sudo tailscale funnel --https=10000 off`) sense deixar cap procés ni residu obert.

### Repte E: Segmentació 100% Automàtica i Invariant Geomètric de Gencat (`x0 <= 88.0 pt`)
Per a les proves històriques (2021-2023), definir manualment o semi-manualment coordenades de tall hauria trencat l'objectiu de reduir a zero el treball manual. S'ha desenvolupat un segmentador automàtic d'alta precisió (`scripts/tallador_automatic.py`) basat en una anàlisi geomètrica profunda del disseny editorial de la Generalitat:
1. **L'invariant d'enunciat:** En totes les proves oficials de Gencat, el número d'ítem principal comença invariablement a una coordenada `x0 <= 88.0 pt`. Qualsevol altre número de taula, opció de test (`a`, `b`, `c`, `d`) o referència interna comença a `x >= 95.0 pt`. Això permet identificar tots els límits verticals superiors d'ítem amb 0 falsos positius.
2. **Delimitació de caixes obertes ("NO ESCRIGUIS"):** Als ítems de desenvolupament, la caixa grisa amb la llegenda *"NO ESCRIGUIS EN AQUEST ESPAI / ESPAI PER A LA CORRECCIÓ"* marca el final de la zona de resposta. El segmentador calcula automàticament el límit inferior prenent el top d'aquesta caixa (`y0`), ignorant les caixes no relacionades que puguin aparèixer en pàgines posteriors.
3. **Auditoria integrada de marges i contaminació:** Totes les captures generades passen immediatament per l'auditor d'OCR Tesseract i eliminació de vores blanques (`autocrop_tight`), assolint un `100% PASS` automàtic a les 6 proves històriques sense retallar cap píxel d'informació.

### Repte F: Estilisme visual i colors de tema a Forms API
A l'especificació REST de **Google Forms API v1**, el recurs `Form` i el mètode `batchUpdate` no admeten la manipulació de la propietat de tema estètic (`themeColor` / paleta de colors). Les crides d'API només permeten canvis en l'esquema de preguntes, retroaccions i paràmetres de qüestionari. Per personalitzar el color corporatiu per matèria (blau per a Matemàtiques, verd/taronja per a Ciència i Tecnologia):
- **Opció Web:** Des de la vista d'edició del docent, a la icona superior *"Personalitza el tema"* amb 1 clic.
- **Opció Apps Script:** Mitjançant la biblioteca clàssica `FormApp.openById(id)` des d'un script de Google Apps Script.

---

## 4. El Paper de la IA: De simple generador a "Parell Programador Rigorós"

L'ús de la intel·ligència artificial en aquest projecte **no ha consistit a demanar-li que "s'inventi" o "al·lucini" contingut**, sinó a utilitzar-la com un enginyer de programari en parella:
1. **Inspecció i Enginyeria Inversa de Formats:** L'agent llegeix els blocs de text dels PDFs binaris amb PyMuPDF, extreu les posicions verticals reals de cada element i proposa els vectors de tall.
2. **Defensa en Profunditat (Auditoria d'Auditors):** En lloc de confiar cegament en la primera versió dels retalls, es va dissenyar un auditor independent (`scripts/audita_cb.py`). Quan l'auditor detectava errors (com els 8 errors trobats a CTE 2025 o els marges blancs de 300px), l'agent reajustava el codi fins a obtenir el `100% PASS`.
3. **Auditoria Visual i Blindatge de Claus:** Inspecció creuada de les taules escanejades oficials i desplegament d'eines de verificació en viu.
4. **Automatització d'APIs complexes:** Gestió dels fluxos OAuth de Google Workspace, transformació dels esquemes JSON de Forms API i gestió de carpetes a Drive sense intervenció de ratolí ni pantalla.

---

## 5. Resultat Operatiu: 18 Formularis Oficials en Producció (Banc Complet 2021-2026)

El resultat és un conjunt de **18 formularis complets, operatius i lliurats** a Google Forms (12 moderns + 6 històrics de 4t d'ESO):

| Prova | Matèria | Curs | Any | Puntuació | Form ID |
|---|---|---|---|---|---|
| Avaluació Diagnòstica | Matemàtiques | 2n ESO | 2026 | 31 punts | `1nAnrxjz3tC_-7O_2nmPOW8P4IdYJAFJY3rFsHCqCn6k` |
| Avaluació Diagnòstica | Matemàtiques | 2n ESO | 2025 | 31 punts | `15LBzQDA42CSyEBwGODGUnyeiHCjTLI9flRbYghyCZDs` |
| Avaluació Diagnòstica | Matemàtiques | 2n ESO | 2024 | 24 punts | `1w5BZVZ33xz7HwCqbScONBQBhBIB398PFaR5t1gncHaY` |
| Avaluació Diagnòstica | Ciència i Tecnologia | 2n ESO | 2026 | 40 punts | `1IqwDm94mpsb8wAx3v-8VZ67D2pCczqlVzn2kw_Q5zXU` |
| Avaluació Diagnòstica | Ciència i Tecnologia | 2n ESO | 2025 | 46 punts | `1qRu8ENWkrUSMr5VRHcSIYmEll9xKMj5MpZquctJg1t8` |
| Avaluació Diagnòstica | Ciència i Tecnologia | 2n ESO | 2024 | 39 punts | `1L8_ZWCAFzYpl7ckruCIKBcNaLoahUpz_h-61QHfp6ns` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2026 | 32 punts | `1W2y_rWOy4aHeerESMNATtjH8cjFyqeBrJZfsG5rS1Ao` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2025 | 33 punts | `1S8R0GAGAumzls4G5dYpadIx-IO0Tk0lfCnZapf2htwg` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2024 | 32 punts | `1e7x0jiJTRfRF4GvldK2n-zKb7fd740DG_viV_jtZW8I` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2023 | 35 punts | `1TKJ-0VO6E2L8Acwgh1Tin5ROZhcjVc7wrGknEkSNRkk` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2022 | 35 punts | `1Vc5Ac5JqmDgpCtsYLFEnxUkrTnDcoVG3_g14WA-TD8Q` |
| Competències Bàsiques | Matemàtiques | 4t ESO | 2021 | 35 punts | `1PrB7WbruWFsbaZf36ghpndK41Y1Vq1PECmGNdNN95JA` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2026 | 40 punts | `1GxWihmZzn9ihk1xAlMw8IsMLwlYPrGweRFnY4g58VCI` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2025 | 36 punts | `1jyodOIRqJElQhtMALa6A2_O2N08zz0H8nuzuUoF36lQ` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2024 | 43 punts | `1bCpK0riVGr98dpSjM8eXJX-NBx7-73nzXR4dXAKVTXg` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2023 | 32 punts | `1lNYaiNpFn-cB36ECtcY-4Fvlyqv6aSdmFO6D5kE8IM8` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2022 | 29 punts | `1GXxvajRfJK4NvGnPrAJuJrjSzHuaaTpVKafB-RyP65M` |
| Competències Bàsiques | Ciència i Tecnologia | 4t ESO | 2021 | 33 punts | `1Ot8U3tEA1fVoZ04pVNQAEIDqGvkVscoG8GIm_rIxX9U` |

---

## 6. Com Replicar o Automatitzar Proves Futures

Per afegir qualsevol nova prova en el futur (anys anteriors com 2020 o noves matèries de llengua):
1. Descarregar el PDF oficial a `docencia/materials/competencies_basiques/...`
2. Executar el tallador automàtic per coordenades `scripts/tallador_automatic.py`.
3. Executar `scripts/audita_cb.py --crops <carpeta> --pdf <fitxer.pdf> --items <N>` per garantir 100% d'absència de contaminació i marges nítids.
4. Afegir la clau oficial a `ANSWERS` / `STRUCTURES` i executar:
   ```bash
   .venv/bin/python scripts/crea_formulari_cb.py --curs <CURS> --materia <MATERIA> --any <ANY>
   ```
El formulari s'estructura, es puja a Drive, es comparteix i es configura a Forms API en segons.

