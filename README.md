# 📋 Gencat CB to Google Forms

> **Pipeline autònom d'enginyeria de documents:** transforma les proves oficials de Competències Bàsiques (4t d'ESO) i Avaluacions Diagnòstiques (2n d'ESO) de la Generalitat de Catalunya en qüestionaris autocorregibles de Google Forms en segons, sense feina manual.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Forms API](https://img.shields.io/badge/Google%20Forms%20API-v1-4285F4.svg)](https://developers.google.com/forms/api)
[![PyMuPDF](https://img.shields.io/badge/PDF%20Engine-PyMuPDF-red.svg)](https://pymupdf.readthedocs.io/)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV%20tight--crop-green.svg)](https://opencv.org/)

---

## 🎯 El Problema Docent

Cada any, el Departament d'Educació publica les proves oficials d'avaluació en PDF (16-20 pàgines amb diagrames científics, gràfiques cartesianes, taules i preguntes complexes). 

A l'hora de traslladar-les a Google Forms perquè l'alumnat pugui fer-les amb autoavaluació immediata:
* Retallar les preguntes manualment porta **més de 2 hores per examen**.
* Les captures rectangulars deixen **marges blancs gegants** que fan que el text es vegi minúscul en mòbils o tauletes.
* Sovint es produeix **contaminació creuada**: el text de la pregunta següent es cola a la part inferior de la imatge de context.
* La **transcripció manual de les solucions** a partir de taules escanejades amb creuetes és propensa a errades humanes.

Aquest repositori resol tots aquests reptes mitjançant un **pipeline matemàtic, auditat per visió per computador i lliure d'intervenció manual**.

---

## 🏗️ Arquitectura del Pipeline

```
[ PDF Oficial Gencat ]
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ 1. Descàrrega Automàtica (src/downloader.py)           │
│    - Descàrrega directa des del repositori oficial APE │
└────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ 2. Segmentador Vectorial (src/segmenter.py)            │
│    - Detecció per invariant geomètric: x0 <= 88.0 pt   │
│    - Delimitació de caixes obertes "NO ESCRIGUIS"     │
│    - OpenCV autocrop_tight(pad=6): zero vores blanques │
└────────────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│ 3. Auditoria Estricta (src/auditor.py)                 │
│    - Verificació de marges blancs (< 15 px)            │
│    - OCR Tesseract en català: zero enunciats barrejats │
│    - Verificació d'integritat 100% ítems (1..N)        │
└────────────────────────────────────────────────────────┘
         │ (Només si 100% PASS)
         ▼
┌────────────────────────────────────────────────────────┐
│ 4. Constructor Forms API (src/forms_builder.py)        │
│    - Pujada transparent d'imatges a Google Drive       │
│    - batchUpdate a Forms API v1: mode Quiz actiu       │
│    - Ponderació entera exacta i solucions oficials     │
└────────────────────────────────────────────────────────┘
         │
         ▼
[ Google Form enllestit amb enllaç per a docent i alumnes ]
```

---

## 💡 Reptes Tècnics i Solucions Clau

### 1. Invariant Geomètric de Gencat (`x0 <= 88.0 pt`)
En totes les maquetacions oficials de la Generalitat, el número d'ítem principal comença invariablement a una coordenada `x0 <= 88.0 pt`. Qualsevol altre número de taula o opció de test (`a`, `b`, `c`, `d`) comença a `x >= 95.0 pt`. Això permet aïllar els enunciats amb **zero falsos positius**.

### 2. Autocrop Estricte amb OpenCV (`autocrop_tight`)
A partir del canal monocromàtic (`gray < 248`), es calcula la caixa envolvent matemàtica mínima (`np.min`/`np.max`) de la tinta real i s'afegeixen exactament 6 px d'aire estètic:
```python
def autocrop_tight(img, pad=6, white_thresh=248):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    non_white = np.where(gray < white_thresh)
    if len(non_white[0]) == 0:
        return img
    y0, y1 = int(np.min(non_white[0])), int(np.max(non_white[0]))
    x0, x1 = int(np.min(non_white[1])), int(np.max(non_white[1]))
    h, w = gray.shape
    return img[max(0, y0-pad):min(h, y1+pad+1), max(0, x0-pad):min(w, x1+pad+1)]
```

### 3. Detecció de Contaminació amb OCR Tesseract en Català
Per garantir que cap imatge d'introducció/context contingui part de l'enunciat que ve després, cada captura passa per un filtre regex sobre el text OCR:
```python
m = re.match(r"^\s*([0-9]{1,2})\.\s+([A-ZÀ-Ú][a-zà-ú]+)", ocr_line)
```
Si es detecta cap línia coincident, l'auditor alerta de contaminació i rebutja la captura.

### 4. Restricció de la Google Forms API (Punts Enters)
L'API de Google Forms rebutja valors decimals com `0.25` o `0.5` (`INVALID_ARGUMENT`). Per a preguntes complexes amb 4 subapartats dicotòmics (Sí/No, V/F), cada fila es modela com un subítem independent de **1 punt**, preservant l'equilibri ponderat del currículum sense problemes d'API.

---

## 🚀 Instal·lació i Ús Ràpid

### Requisits
* Python 3.10+
* Tesseract OCR amb el paquet de català instal·lat:
  ```bash
  sudo apt install tesseract-ocr tesseract-ocr-cat
  ```

### Instal·lació
```bash
git clone https://github.com/adriasantacreu/gencat-cb-forms.git
cd gencat-cb-forms
pip install -r requirements.txt
```

### Comandes CLI

1. **Descarregar un examen oficial:**
   ```bash
   python -m src.cli download --curs 4ESO --materia MAT --any 2026 --out downloads
   ```

2. **Segmentar el PDF en captures ajustades:**
   ```bash
   python -m src.cli segment --pdf downloads/4ESO_MAT_2026_prova.pdf --out crops_2026 --dpi 200
   ```

3. **Executar l'auditoria estricta de marges i OCR:**
   ```bash
   python -m src.cli audit --crops crops_2026 --items 32
   ```

4. **Publicar a Google Forms:**
   ```bash
   python -m src.cli build \
     --curs 4ESO \
     --materia MAT \
     --any 2026 \
     --crops crops_2026 \
     --credentials credentials.json \
     --assets-folder <DRIVE_FOLDER_ID_IMAGES> \
     --drive-folder <DRIVE_FOLDER_ID_FORMS>
   ```

---

## 📊 Banc Proves Suportades Oficialment (18 Formularis)

Aquest repositori inclou les estructures i claus de correcció contrastades per a 18 proves completes (2021–2026):

* **4t d'ESO (Competències Bàsiques):**
  * Matemàtiques: 2026, 2025, 2024, 2023, 2022, 2021.
  * Ciència i Tecnologia: 2026, 2025, 2024, 2023, 2022, 2021.
* **2n d'ESO (Avaluacions Diagnòstiques):**
  * Matemàtiques: 2026, 2025, 2024.
  * Ciència i Tecnologia: 2026, 2025, 2024.

---

## 👤 Autor

**Adrià Santacreu**  
Professor de Matemàtiques i Robòtica / Enginyer en Sistemes  
Institut Escola Sant Pol de Mar (Maresme, Catalunya)  
GitHub: [@adriasantacreu](https://github.com/adriasantacreu)

---

## 📄 Llicència

Aquest projecte està sota llicència [MIT](LICENSE). Els continguts de les proves d'avaluació són propietat del Departament d'Educació de la Generalitat de Catalunya i es fan servir amb finalitats exclusivament pedagògiques.

## Catàleg de CCBB (`scripts/cb`)

BD consultable (SQLite + FTS5) de les 18 proves (4ESO MAT/CTE 2021–26, 2ESO MAT/CTE 2024–26): 627 ítems, 77 activitats. Cada ítem té captura pròpia, text OCR, resposta oficial (`answers_registry.py`) i el context de l'activitat enllaçat. Spec: `specs/001-cb-catalog/`.

| Ordre | Què fa |
|---|---|
| `scripts/cb index` | Reconstrueix `docencia/materials/competencies_basiques/cb_catalog/` (BD + `crops/`, fora del git) |
| `scripts/cb check` | Recompte = registre, captura i text per ítem, 0 duplicats, marges, contextos nets; excepcions a `data/excepcions.csv` |
| `scripts/cb cerca TEXT [--etapa 4ESO\|2ESO] [--materia mat\|cte]` | Cerca per paraules clau |
| `scripts/cb fulls --out F.pdf [--prova ID]` | Full de miniatures per revisar |

Bloc i tema (`data/cb_temes.csv`) són una proposta automàtica (`revisat=no`) pendent de revisió. Les captures són les de Forms (seccionades: context + un ítem cada una); no es regeneren aquí.
