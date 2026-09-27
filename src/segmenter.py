"""Segmentador geomètric automàtic per a proves de la Generalitat de Catalunya."""

from pathlib import Path
import re
import cv2
import numpy as np
import pymupdf


def autocrop_tight(img, pad: int = 6, white_thresh: int = 248):
    """Elimina completament qualsevol marge blanc residual mitjançant llindar d'intensitat."""
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
    return img[max(0, y0 - pad) : min(h, y1 + pad + 1), max(0, x0 - pad) : min(w, x1 + pad + 1)]


def pixmap_to_cv2(pix):
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    elif pix.n == 1:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def detect_page_elements(page):
    """
    Detecta automàticament la posició del context i dels ítems a una pàgina.
    Regla geomètrica fonamental de Gencat: Els ítems principals comencen a x0 <= 88.0 pt.
    """
    blocks = page.get_text("blocks")

    act_header = None
    no_write_boxes = []
    item_starts = []

    for b in blocks:
        x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4].strip()
        if y1 < 85:  # Capçalera de pàgina
            continue
        if y0 > 795:  # Peu de pàgina
            continue
        if "no escriguis" in txt.lower() or "respon a la part 2" in txt.lower():
            no_write_boxes.append(y0)
            continue

        m_act = re.search(r"ACTIVITAT\s+([0-9]+)[:\s]+([^\n]+)", txt, re.I)
        if m_act and not act_header:
            act_header = (int(m_act.group(1)), y0, y1)

        # Un ítem vàlid de Gencat comença a x0 <= 88.0 pt amb dígit seguit de punt, tab o espai
        if x0 <= 88.0:
            m_item = re.match(r"^([0-9]{1,2})[\s\t\.\)]+(.*)", txt)
            if m_item:
                num = int(m_item.group(1))
                if 1 <= num <= 50:
                    item_starts.append((num, y0))

    item_starts.sort(key=lambda x: x[1])
    crops = []

    # Context d'activitat si n'hi ha i hi ha ítems a sota
    if act_header and item_starts:
        first_item_y0 = item_starts[0][1]
        if first_item_y0 - act_header[1] > 35:
            crops.append(
                {
                    "id": f"context_act{act_header[0]}_intro",
                    "rect": (70, max(90, act_header[1] - 5), 530, first_item_y0 - 6),
                }
            )
    elif act_header and not item_starts:
        crops.append(
            {
                "id": f"context_act{act_header[0]}_intro",
                "rect": (70, max(90, act_header[1] - 5), 530, 785),
            }
        )
    elif not act_header and item_starts:
        first_item_y0 = item_starts[0][1]
        if first_item_y0 > 140:
            crops.append(
                {
                    "id": f"context_extra_p{page.number+1}",
                    "rect": (70, 90, 530, first_item_y0 - 6),
                }
            )

    # Rectangles per a cada ítem
    for i, (num, y0) in enumerate(item_starts):
        crop_y0 = max(90, y0 - 6)
        if i + 1 < len(item_starts):
            next_y0 = item_starts[i + 1][1]
            boxes_between = [by for by in no_write_boxes if crop_y0 < by < next_y0]
            if boxes_between:
                crop_y1 = min(boxes_between) - 5
            else:
                crop_y1 = next_y0 - 6
        else:
            boxes_after = [by for by in no_write_boxes if by > crop_y0]
            if boxes_after:
                crop_y1 = min(boxes_after) - 5
            else:
                crop_y1 = 785

        crops.append({"id": f"item_{num}", "rect": (70, crop_y0, 530, crop_y1)})

    return crops


def segment_pdf(pdf_path: Path, out_dir: Path, dpi: int = 200) -> list[Path]:
    """Segmenta automàticament tot el PDF i desa les captures netes a out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf_path))
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)

    generated = []
    for pno in range(len(doc)):
        page = doc[pno]
        page_crops = detect_page_elements(page)
        for c in page_crops:
            rect = pymupdf.Rect(c["rect"])
            pix = page.get_pixmap(matrix=mat, clip=rect)
            img = pixmap_to_cv2(pix)
            cropped = autocrop_tight(img, pad=6)
            out_file = out_dir / f"{c['id']}.png"
            cv2.imwrite(str(out_file), cropped)
            generated.append(out_file)

    print(f"✓ Generades {len(generated)} captures a {out_dir}")
    return generated
