"""Mòdul d'auditoria estricta de captures: comprovació de marges i OCR Tesseract."""

from pathlib import Path
import re
import cv2
import numpy as np
import pytesseract


def check_margins(img_path: Path, max_margin: int = 15, white_thresh: int = 248) -> dict:
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return {"ok": False, "error": "No es pot carregar la imatge"}

    h, w = img.shape
    non_white = np.where(img < white_thresh)
    if len(non_white[0]) == 0:
        return {"ok": False, "error": "Imatge completament blanca"}

    y0, y1 = int(np.min(non_white[0])), int(np.max(non_white[0]))
    x0, x1 = int(np.min(non_white[1])), int(np.max(non_white[1]))

    m_top = y0
    m_bottom = h - 1 - y1
    m_left = x0
    m_right = w - 1 - x1

    bad = []
    if m_top > max_margin:
        bad.append(f"top={m_top}px")
    if m_bottom > max_margin:
        bad.append(f"bottom={m_bottom}px")
    if m_left > max_margin:
        bad.append(f"left={m_left}px")
    if m_right > max_margin:
        bad.append(f"right={m_right}px")

    return {
        "ok": len(bad) == 0,
        "margins": (m_top, m_right, m_bottom, m_left),
        "details": ", ".join(bad) if bad else "OK",
    }


def check_context_contamination(img_path: Path) -> dict:
    img = cv2.imread(str(img_path))
    if img is None:
        return {"ok": False, "error": "No es pot carregar la imatge"}

    try:
        text = pytesseract.image_to_string(img, lang="cat")
    except Exception as e:
        text = pytesseract.image_to_string(img)

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    contaminated_lines = []
    item_pattern = re.compile(r"^\s*([0-9]{1,2})\.\s+([A-ZÀ-Ú][a-zà-ú]+)")

    for ln in lines:
        m = item_pattern.match(ln)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 45:
                contaminated_lines.append(ln)

    return {
        "ok": len(contaminated_lines) == 0,
        "contaminated_lines": contaminated_lines,
        "lines_sample": lines[:3],
    }


def audit_crop_directory(crops_dir: Path, expected_items: int) -> bool:
    print(f"\n🔍 INICIANT AUDITORIA ESTRICTA A: {crops_dir}")
    all_ok = True

    crop_files = list(crops_dir.glob("*.png"))
    if not crop_files:
        print(f"❌ Error: Cap captura trobada a {crops_dir}")
        return False

    item_files = [f for f in crop_files if f.stem.startswith("item_")]
    context_files = [f for f in crop_files if f.stem.startswith("context_")]

    print(
        f"📊 Total captures: {len(crop_files)} ({len(item_files)} ítems, {len(context_files)} contextos)"
    )

    # 1. Comprovació d'ítems esperats
    found_nums = set()
    for f in item_files:
        stem = f.stem.replace("item_", "")
        if "_" in stem:
            stem = stem.split("_")[0]
        if stem.isdigit():
            found_nums.add(int(stem))

    missing = [i for i in range(1, expected_items + 1) if i not in found_nums]
    if missing:
        print(f"❌ Falten els ítems següents: {missing}")
        all_ok = False
    else:
        print(f"✓ Tots els ítems de l'1 al {expected_items} estan presents.")

    # 2. Comprovació de marges blancs
    margin_errors = 0
    for f in crop_files:
        res = check_margins(f)
        if not res["ok"]:
            margin_errors += 1
            print(f"  ⚠ Marge excessiu a {f.name}: {res['details']}")
    if margin_errors == 0:
        print(f"✓ 100% de les captures tenen marges blancs impecables (<15px).")
    else:
        all_ok = False

    # 3. Detecció de contaminació en contextos via OCR
    contamination_errors = 0
    for f in context_files:
        res = check_context_contamination(f)
        if not res["ok"]:
            contamination_errors += 1
            print(f"  ❌ Contaminació d'enunciat a {f.name}: {res['contaminated_lines']}")
    if contamination_errors == 0:
        print(f"✓ 100% de les imatges de context estan netes d'enunciats d'ítem.")
    else:
        all_ok = False

    if all_ok:
        print("🎉 AUDITORIA SUPERADA AMB ÈXIT (100% PASS)!\n")
    else:
        print("❌ S'han detectat problemes que cal corregir.\n")

    return all_ok
