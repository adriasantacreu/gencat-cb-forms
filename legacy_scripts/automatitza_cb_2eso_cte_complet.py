#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatitzador mestre per generar captures, estructures i formularis de 2ESO CTE 2025 i 2024.
Institut Escola Sant Pol de Mar — Adrià Santacreu
"""

import os
import sys
import json
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
        cropped = autocrop_tight(img, pad=6)
        cv2.imwrite(str(out_dir / f"{c['id']}.png"), cropped)
    print(f"✓ Generats {len(crops)} crops a {out_dir}")

# -------------------------------------------------------------------------
# 2ESO CTE 2025
# -------------------------------------------------------------------------
CROPS_2025 = [
    # Act 1: Les begudes isotòniques
    {"id": "context_act1_intro", "pno": 1, "rect": (70, 90, 530, 520)},
    {"id": "item_1", "pno": 2, "rect": (70, 115, 530, 268)},
    {"id": "item_2", "pno": 2, "rect": (70, 270, 530, 420)},
    {"id": "item_3", "pno": 2, "rect": (70, 422, 530, 555)},
    {"id": "item_4", "pno": 2, "rect": (70, 556, 530, 785)},
    {"id": "item_5", "pno": 3, "rect": (70, 115, 530, 785)},
    {"id": "item_6", "pno": 4, "rect": (70, 115, 530, 785)},
    {"id": "item_7", "pno": 5, "rect": (70, 115, 530, 405)},
    {"id": "item_8", "pno": 5, "rect": (70, 410, 530, 785)},

    # Act 2: La cursa més ràpida de la història
    {"id": "context_act2_intro", "pno": 6, "rect": (70, 90, 530, 785)},
    {"id": "item_9", "pno": 7, "rect": (70, 115, 530, 248)},
    {"id": "item_10", "pno": 7, "rect": (70, 250, 530, 785)},
    {"id": "item_11", "pno": 8, "rect": (70, 115, 530, 345)},
    {"id": "item_12", "pno": 8, "rect": (70, 348, 530, 785)},
    {"id": "item_13", "pno": 9, "rect": (70, 115, 530, 310)},
    {"id": "item_14", "pno": 9, "rect": (70, 312, 530, 785)},
    {"id": "item_15", "pno": 10, "rect": (70, 115, 530, 290)},
    {"id": "item_16", "pno": 10, "rect": (70, 292, 530, 442)},
    {"id": "item_17", "pno": 10, "rect": (70, 445, 530, 600)},
    {"id": "item_18", "pno": 10, "rect": (70, 602, 530, 785)},

    # Act 3: Bàsquet App
    {"id": "context_act3_intro", "pno": 11, "rect": (70, 90, 530, 620)},
    {"id": "item_19", "pno": 11, "rect": (70, 630, 530, 785)},
    {"id": "item_20", "pno": 12, "rect": (70, 115, 530, 785)},
    {"id": "item_21", "pno": 13, "rect": (70, 115, 530, 450)},
    {"id": "item_22", "pno": 13, "rect": (70, 452, 530, 785)},
    {"id": "item_23", "pno": 14, "rect": (70, 115, 530, 540)},
    {"id": "item_24", "pno": 14, "rect": (70, 542, 530, 785)},
    {"id": "item_25", "pno": 15, "rect": (70, 115, 530, 785)},
]

# -------------------------------------------------------------------------
# 2ESO CTE 2024
# -------------------------------------------------------------------------
CROPS_2024 = [
    # Act 1: L'escalfament global
    {"id": "context_act1_intro", "pno": 1, "rect": (70, 90, 530, 785)},
    {"id": "item_1", "pno": 2, "rect": (70, 115, 530, 325)},
    {"id": "item_2", "pno": 2, "rect": (70, 328, 530, 478)},
    {"id": "item_3", "pno": 2, "rect": (70, 480, 530, 785)},
    {"id": "item_4", "pno": 3, "rect": (70, 115, 530, 500)},
    {"id": "item_5", "pno": 3, "rect": (70, 505, 530, 665)},
    {"id": "item_6", "pno": 3, "rect": (70, 668, 530, 785)},

    # Act 2: Construïm un hivernacle
    {"id": "context_act2_intro", "pno": 4, "rect": (70, 90, 530, 295)},
    {"id": "item_7", "pno": 4, "rect": (70, 298, 530, 640)},
    {"id": "item_8", "pno": 4, "rect": (70, 642, 530, 785)},
    {"id": "item_9", "pno": 5, "rect": (70, 115, 530, 355)},
    {"id": "item_10", "pno": 5, "rect": (70, 360, 530, 605)},
    {"id": "item_11", "pno": 5, "rect": (70, 608, 530, 785)},
    {"id": "item_12", "pno": 6, "rect": (70, 115, 530, 785)},

    # Act 3: Investiguem al laboratori
    {"id": "context_act3_intro", "pno": 7, "rect": (70, 90, 530, 515)},
    {"id": "item_13", "pno": 7, "rect": (70, 518, 530, 658)},
    {"id": "item_14", "pno": 7, "rect": (70, 660, 530, 785)},
    {"id": "item_15", "pno": 8, "rect": (70, 115, 530, 302)},
    {"id": "item_16", "pno": 8, "rect": (70, 305, 530, 515)},
    {"id": "item_17", "pno": 8, "rect": (70, 518, 530, 785)},
    {"id": "item_18", "pno": 9, "rect": (70, 115, 530, 785)},

    # Act 4: Camina, fes salut!
    {"id": "context_act4_intro", "pno": 10, "rect": (70, 90, 530, 255)},
    {"id": "item_19", "pno": 10, "rect": (70, 258, 530, 360)},
    {"id": "item_20", "pno": 10, "rect": (70, 362, 530, 480)},
    {"id": "item_21", "pno": 10, "rect": (70, 482, 530, 785)},
    {"id": "context_act4_taula", "pno": 11, "rect": (70, 90, 530, 268)},
    {"id": "item_22", "pno": 11, "rect": (70, 115, 530, 268)},
    {"id": "item_23", "pno": 11, "rect": (70, 270, 530, 420)},
    {"id": "item_24", "pno": 11, "rect": (70, 422, 530, 582)},
    {"id": "item_25", "pno": 11, "rect": (70, 585, 530, 785)},
]

if __name__ == "__main__":
    pdf_2025 = "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2025_CTE_prova.pdf"
    out_2025 = "scratch/crops_2eso_cte_2025_clean"
    render_crops(pdf_2025, CROPS_2025, out_2025)

    pdf_2024 = "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2024_CTE_prova.pdf"
    out_2024 = "scratch/crops_2eso_cte_2024_clean"
    render_crops(pdf_2024, CROPS_2024, out_2024)
