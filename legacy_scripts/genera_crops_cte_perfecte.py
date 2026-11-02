#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador i auditor de talls ultra-precisos per a 4ESO CTE 2025 i 2024.
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np
import pymupdf

def autocrop_tight(img, pad=10, white_thresh=248):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    non_white = np.where(gray < white_thresh)
    if len(non_white[0]) == 0:
        return img
    y0, y1 = int(np.min(non_white[0])), int(np.max(non_white[0]))
    x0, x1 = int(np.min(non_white[1])), int(np.max(non_white[1]))
    h, w = gray.shape
    y0 = max(0, y0 - pad)
    y1 = min(h, y1 + pad + 1)
    x0 = max(0, x0 - pad)
    x1 = min(w, x1 + pad + 1)
    return img[y0:y1, x0:x1]

def pixmap_to_cv2(pix):
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif pix.n == 1:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img

def render_crops(pdf_path, crops, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    mat = pymupdf.Matrix(2.0, 2.0)
    for c in crops:
        page = doc[c["pno"]]
        rect = pymupdf.Rect(c["rect"])
        pix = page.get_pixmap(matrix=mat, clip=rect)
        img = pixmap_to_cv2(pix)
        cropped = autocrop_tight(img, pad=10)
        cv2.imwrite(str(out_dir / f"{c['id']}.png"), cropped)
    print(f"✓ Generats {len(crops)} crops a {out_dir}")

# =========================================================================
# 4ESO CTE 2025
# =========================================================================
CROPS_CTE_2025 = [
    # Act 1: La qualitat de l'aire a l'aula (pno 1 a 5)
    {"id": "context_act1_intro", "pno": 1, "rect": (70, 90, 525, 440)},
    {"id": "item_1", "pno": 1, "rect": (70, 442, 525, 680)},
    {"id": "item_2", "pno": 2, "rect": (70, 115, 525, 335)},
    {"id": "item_3", "pno": 2, "rect": (70, 338, 525, 535)},
    {"id": "item_4", "pno": 2, "rect": (70, 538, 525, 780)},
    {"id": "context_act1_fig2", "pno": 3, "rect": (70, 115, 525, 470)},
    {"id": "item_5", "pno": 3, "rect": (70, 472, 525, 780)},
    {"id": "context_act1_grafic", "pno": 4, "rect": (70, 115, 525, 435)},
    {"id": "item_6", "pno": 5, "rect": (70, 115, 525, 330)},
    {"id": "item_7", "pno": 5, "rect": (70, 332, 525, 520)},

    # Act 2: L'ecolocalització en els dofins (pno 6 a 10)
    {"id": "context_act2_intro", "pno": 6, "rect": (70, 90, 525, 520)},
    {"id": "item_8", "pno": 6, "rect": (70, 522, 525, 700)},
    {"id": "item_9", "pno": 7, "rect": (70, 115, 525, 780)},
    {"id": "context_act2_taula2", "pno": 8, "rect": (70, 115, 525, 350)},
    {"id": "item_10", "pno": 8, "rect": (70, 352, 525, 570)},
    {"id": "item_11", "pno": 9, "rect": (70, 115, 525, 565)},
    {"id": "context_act2_fig3", "pno": 9, "rect": (70, 568, 525, 800)},
    {"id": "item_12", "pno": 10, "rect": (70, 115, 525, 290)},
    {"id": "item_13", "pno": 10, "rect": (70, 292, 525, 555)},
    {"id": "item_14", "pno": 10, "rect": (70, 558, 525, 720)},

    # Act 3: Centrals hidroelèctriques reversibles (pno 11 a 13)
    {"id": "context_act3_intro", "pno": 11, "rect": (70, 90, 525, 540)},
    {"id": "item_15", "pno": 11, "rect": (70, 542, 525, 720)},
    {"id": "item_16", "pno": 12, "rect": (70, 115, 525, 310)},
    {"id": "context_act3_fig2", "pno": 12, "rect": (70, 315, 525, 800)},
    {"id": "item_17", "pno": 13, "rect": (70, 115, 525, 270)},
    {"id": "item_18", "pno": 13, "rect": (70, 272, 525, 440)},
    {"id": "item_19", "pno": 13, "rect": (70, 445, 525, 750)},

    # Act 4: Aigua al planeta Mart (pno 14 a 17)
    {"id": "context_act4_intro", "pno": 14, "rect": (70, 90, 525, 790)},
    {"id": "item_20", "pno": 15, "rect": (70, 115, 525, 270)},
    {"id": "item_21", "pno": 15, "rect": (70, 272, 525, 465)},
    {"id": "item_22", "pno": 15, "rect": (70, 468, 525, 620)},
    {"id": "context_act4_electrolisi", "pno": 16, "rect": (70, 115, 525, 560)},
    {"id": "item_23", "pno": 16, "rect": (70, 562, 525, 790)},
    {"id": "item_24", "pno": 17, "rect": (70, 115, 525, 335)},
    {"id": "item_25", "pno": 17, "rect": (70, 338, 525, 630)},
]

# =========================================================================
# 4ESO CTE 2024
# =========================================================================
CROPS_CTE_2024 = [
    # Act 1: Sense gluten (pno 1 a 4)
    {"id": "context_act1_intro", "pno": 1, "rect": (70, 90, 525, 780)},
    {"id": "item_1", "pno": 2, "rect": (70, 115, 525, 320)},
    {"id": "item_2", "pno": 2, "rect": (70, 322, 525, 650)},
    {"id": "item_3", "pno": 3, "rect": (70, 115, 525, 320)},
    {"id": "item_4", "pno": 3, "rect": (70, 322, 525, 670)},
    {"id": "item_5", "pno": 4, "rect": (70, 115, 525, 290)},
    {"id": "item_6", "pno": 4, "rect": (70, 292, 525, 640)},

    # Act 2: Calderes de biomassa (pno 5 a 8)
    {"id": "context_act2_intro", "pno": 5, "rect": (70, 90, 525, 780)},
    {"id": "item_7", "pno": 6, "rect": (70, 115, 525, 310)},
    {"id": "item_8", "pno": 6, "rect": (70, 312, 525, 515)},
    {"id": "item_9", "pno": 6, "rect": (70, 518, 525, 780)},
    {"id": "item_10", "pno": 7, "rect": (70, 115, 525, 410)},
    {"id": "item_11", "pno": 7, "rect": (70, 412, 525, 565)},
    {"id": "item_12", "pno": 7, "rect": (70, 568, 525, 775)},
    {"id": "item_13", "pno": 8, "rect": (70, 115, 525, 320)},

    # Act 3: La invasió de les meduses (pno 9 a 12)
    {"id": "context_act3_intro", "pno": 9, "rect": (70, 90, 525, 780)},
    {"id": "item_14", "pno": 10, "rect": (70, 115, 525, 270)},
    {"id": "item_15", "pno": 10, "rect": (70, 272, 525, 430)},
    {"id": "item_16", "pno": 10, "rect": (70, 432, 525, 675)},
    {"id": "item_17", "pno": 11, "rect": (70, 115, 525, 370)},
    {"id": "item_18", "pno": 11, "rect": (70, 372, 525, 570)},
    {"id": "item_19", "pno": 12, "rect": (70, 115, 525, 420)},

    # Act 4: Impressió en 3D (pno 13 a 16)
    {"id": "context_act4_intro", "pno": 13, "rect": (70, 90, 525, 780)},
    {"id": "item_20", "pno": 14, "rect": (70, 115, 525, 370)},
    {"id": "item_21", "pno": 14, "rect": (70, 372, 525, 570)},
    {"id": "item_22", "pno": 14, "rect": (70, 572, 525, 775)},
    {"id": "item_23", "pno": 15, "rect": (70, 115, 525, 520)},
    {"id": "item_24", "pno": 15, "rect": (70, 522, 525, 745)},
    {"id": "item_25", "pno": 16, "rect": (70, 115, 525, 700)},
]

if __name__ == "__main__":
    print("=== GENERANT CROPS NETS 4ESO CTE 2025 ===")
    render_crops(
        "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2025_CTE_prova.pdf",
        CROPS_CTE_2025,
        "scratch/crops_4eso_cte_2025_clean"
    )

    print("\n=== GENERANT CROPS NETS 4ESO CTE 2024 ===")
    render_crops(
        "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2024_CTE_prova.pdf",
        CROPS_CTE_2024,
        "scratch/crops_4eso_cte_2024_clean"
    )
