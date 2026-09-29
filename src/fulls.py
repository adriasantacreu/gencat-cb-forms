"""`cb fulls`: PDF de miniatures per prova (context | captura de l'ítem + clau) per a la revisió visual."""
import io
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import pymupdf
from PIL import Image

from catalog import CB_DIR, connect

W, H, M = 595, 842, 24
ROWS = 4
ROW_H = (H - 2 * M - 14) / ROWS
COL_W = (W - 2 * M - 8) / 2


def _thumb(path: Path, max_w: int = 520) -> bytes:
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=60)
    return buf.getvalue()


def make_fulls(out: Path, prova: Optional[str] = None) -> Path:
    con = connect()
    q = "SELECT i.*, a.titol FROM items i JOIN activitats a ON a.id=i.activitat_id" + (" WHERE i.prova=?" if prova else "") + " ORDER BY i.prova, i.activitat_id, i.numero, i.sub"
    groups: "OrderedDict[tuple, list]" = OrderedDict()
    for r in con.execute(q, (prova,) if prova else ()):
        groups.setdefault((r["prova"], r["activitat_id"], r["enunciat_img"], r["context_img"]), []).append(dict(r))
    doc, page, slot, cur = pymupdf.open(), None, ROWS, None
    for (pv, aid, img, ctx), rs in groups.items():
        if slot == ROWS or cur != pv:
            page, slot, cur = doc.new_page(width=W, height=H), 0, pv
            page.insert_text((M, M - 8), f"{pv} — context | ítem", fontsize=8)
        y0 = M + 4 + slot * ROW_H
        keys = ", ".join(f"{r['numero']}{'.' + r['sub'] if r['sub'] else ''}={r['resposta'] or 'oberta'}" for r in rs)
        page.insert_text((M, y0 + 8), f"{aid.split('_A')[-1] and 'A' + aid.split('_A')[-1]} · {rs[0]['titol'][:40]} · ítems {keys}"[:120], fontsize=6.5)
        for c, col in enumerate((ctx, img)):
            rect = pymupdf.Rect(M + c * (COL_W + 8), y0 + 11, M + c * (COL_W + 8) + COL_W, y0 + ROW_H - 3)
            f = CB_DIR / col if col else None
            if f and f.exists():
                page.insert_image(rect, stream=_thumb(f), keep_proportion=True)
            else:
                page.insert_textbox(rect, "SENSE CAPTURA", fontsize=9, color=(0.8, 0, 0))
            page.draw_rect(rect, color=(0.8, 0.8, 0.8), width=0.3)
        slot += 1
    doc.save(str(out), deflate=True)
    return out
