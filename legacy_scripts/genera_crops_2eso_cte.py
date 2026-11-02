#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de talls nets per a 2n d'ESO Ciència i Tecnologia (CTE 2026).
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

CROPS_2ESO_CTE_2026 = [
    # Act 1: L'etiqueta d'eficiència energètica (pàgines 1 a 4)
    {"id": "context_act1_intro", "pno": 1, "rect": (70, 90, 530, 525)},
    {"id": "item_1", "pno": 1, "rect": (70, 530, 530, 680)},
    {"id": "item_2", "pno": 1, "rect": (70, 685, 530, 795)},
    {"id": "item_3", "pno": 2, "rect": (70, 115, 530, 248)},
    {"id": "item_4", "pno": 2, "rect": (70, 250, 530, 405)},
    {"id": "item_5", "pno": 2, "rect": (70, 410, 530, 785)},
    {"id": "item_6", "pno": 3, "rect": (70, 115, 530, 360)},
    {"id": "item_7", "pno": 3, "rect": (70, 365, 530, 500)},
    {"id": "item_8", "pno": 4, "rect": (70, 115, 530, 780)},

    # Act 2: La desaparició de les abelles (pàgines 5 a 11)
    {"id": "context_act2_intro", "pno": 5, "rect": (70, 90, 530, 420)},
    {"id": "item_9", "pno": 5, "rect": (70, 425, 530, 785)},
    {"id": "item_10", "pno": 6, "rect": (70, 115, 530, 785)},
    {"id": "item_11", "pno": 7, "rect": (70, 115, 530, 785)},
    {"id": "item_12", "pno": 8, "rect": (70, 115, 530, 415)},
    {"id": "item_13", "pno": 8, "rect": (70, 420, 530, 785)},
    {"id": "item_14", "pno": 9, "rect": (70, 115, 530, 575)},
    {"id": "item_15", "pno": 9, "rect": (70, 580, 530, 785)},
    {"id": "item_16", "pno": 10, "rect": (70, 115, 530, 355)},
    {"id": "item_17", "pno": 10, "rect": (70, 360, 530, 785)},
    {"id": "item_18", "pno": 11, "rect": (70, 115, 530, 785)},

    # Act 3: Les estacions meteorològiques (pàgines 12 a 15)
    {"id": "context_act3_intro", "pno": 12, "rect": (70, 90, 530, 430)},
    {"id": "item_19", "pno": 12, "rect": (70, 435, 530, 785)},
    {"id": "item_20", "pno": 13, "rect": (70, 115, 530, 550)},
    {"id": "item_21", "pno": 13, "rect": (70, 555, 530, 785)},
    {"id": "item_22", "pno": 14, "rect": (70, 115, 530, 485)},
    {"id": "item_23", "pno": 14, "rect": (70, 488, 530, 785)},
    {"id": "context_act3_climograma", "pno": 15, "rect": (70, 90, 530, 480)},
    {"id": "item_24", "pno": 15, "rect": (70, 485, 530, 605)},
    {"id": "item_25", "pno": 15, "rect": (70, 608, 530, 785)},
]

if __name__ == "__main__":
    pdf_2026 = "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2026_CTE_prova.pdf"
    out_dir_2026 = "scratch/crops_2eso_cte_2026_clean"
    render_crops(pdf_2026, CROPS_2ESO_CTE_2026, out_dir_2026)
