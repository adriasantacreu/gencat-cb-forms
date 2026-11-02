#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Retall Vectorial Perfecte per a Competències Bàsiques i Avaluacions Diagnòstiques.
Calcula les coordenades reals dels elements (contextos, enunciats, figures, opcions),
aplica autocrop morfològic amb OpenCV per eliminar tot blanc inútil, i garanteix
zero contaminació creuada entre contexts i preguntes.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
import cv2
import numpy as np
import pymupdf

def autocrop_tight(img, pad=10, white_thresh=248):
    """
    Retalla una imatge BGR/escala de grisos exactament al contorn del contingut (ink),
    eliminant tot marge blanc inútil superior, inferior i lateral, afegint un padding estètic net.
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    non_white = np.where(gray < white_thresh)
    if len(non_white[0]) == 0:
        return img  # imatge tota blanca
    
    y0, y1 = int(np.min(non_white[0])), int(np.max(non_white[0]))
    x0, x1 = int(np.min(non_white[1])), int(np.max(non_white[1]))
    
    h, w = gray.shape
    y0 = max(0, y0 - pad)
    y1 = min(h, y1 + pad + 1)
    x0 = max(0, x0 - pad)
    x1 = min(w, x1 + pad + 1)
    
    return img[y0:y1, x0:x1]

def pixmap_to_cv2(pix):
    """Converteix un pixmap de PyMuPDF a imatge OpenCV BGR."""
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif pix.n == 1:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img

def render_and_crop(page, rect, pad=10, dpi=200):
    """Renderitza un clip de pàgina del PDF i l'ajusta amb autocrop_tight."""
    pix = page.get_pixmap(dpi=dpi, clip=rect)
    img = pixmap_to_cv2(pix)
    return autocrop_tight(img, pad=pad)

print("Mòdul de retall llest.")
