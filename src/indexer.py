"""`cb index`: registre (STRUCTURES/ANSWERS) + captures auditades → cb_catalog.db (activitats + ítems, text per OCR)."""
import hashlib
import os
import json
import re
import shutil
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ["OMP_THREAD_LIMIT"] = "1"  # Tesseract multifil + 4 processos = 100× més lent

import cv2
import pytesseract

from answers_registry import ANSWERS, STRUCTURES
from catalog import CB_DIR, CROPS, WORKSPACE, insert_fts, reset

RECUPERAT = WORKSPACE / "scratch/cb_recuperat"   # captures de 4t recuperades de Drive (_Assets_Imatges)
OCR_CACHE = CB_DIR / ".ocr_cache.json"
ETAPA = {"4ESO": "CB4ESO", "2ESO": "CB2ESO"}
CONV = {"4ESO": "CB", "2ESO": "AD"}


def prova_id(k) -> str:
    return f"{ETAPA[k[0]]}_{k[1]}_{k[2]}"


def source_dir(k) -> Path:
    """On són les captures d'una prova: la BD mateixa (crops/) si ja hi són, si no els retalls originals."""
    s = STRUCTURES[k]
    for d in (CROPS / prova_id(k), WORKSPACE / s["crops_dir"], RECUPERAT / Path(s["crops_dir"]).name):
        if d.is_dir() and any(d.glob("*.png")):
            return d
    raise FileNotFoundError(f"{prova_id(k)}: no trobo les captures ({s['crops_dir']})")


def _ocr(path: str) -> str:
    img = cv2.imread(path)
    try:
        t = pytesseract.image_to_string(img, lang="cat")
    except Exception:
        t = pytesseract.image_to_string(img)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{2,}", "\n", t)).strip()


def ocr_all(files) -> dict:
    """OCR amb memòria cau per hash (una captura idèntica no es torna a llegir)."""
    cache = json.loads(OCR_CACHE.read_text()) if OCR_CACHE.exists() else {}
    hs = {f: hashlib.sha1(Path(f).read_bytes()).hexdigest() for f in files}
    todo = sorted({f for f, h in hs.items() if h not in cache})
    if todo:
        with ProcessPoolExecutor(4) as ex:
            for f, t in zip(todo, ex.map(_ocr, todo, chunksize=4)):
                cache[hs[f]] = t
        OCR_CACHE.write_text(json.dumps(cache, ensure_ascii=False))
    return {f: cache[h] for f, h in hs.items()}


def parse(k, d: Path):
    """Recorre l'estructura d'una prova: llista d'ítems amb activitat, captura, context i clau."""
    s, ans = STRUCTURES[k], ANSWERS[k]
    acts, items = [], []
    act, ctx, last_item_img = None, None, None
    for e in s["elements"]:
        kind = e["kind"]
        if kind == "section":
            m = re.match(r"Activitat\s+(\d+)\.?\s*(.*)", e["title"])
            act = dict(numero=int(m.group(1)) if m else len(acts) + 1, titol=(m.group(2) if m else e["title"]).strip(),
                       descripcio=e.get("desc", ""), contexts=[])
            acts.append(act)
            ctx = last_item_img = None
        elif kind == "image":
            if act is None:
                act = dict(numero=0, titol="", descripcio="", contexts=[])
                acts.append(act)
            if e["file"].startswith("item_"):
                last_item_img = e["file"]
            else:
                ctx = e["file"]
                act["contexts"].append(ctx)
        elif kind in ("item", "open_item"):
            num = str(e["num"])
            lab = re.match(r"Pregunta\s+(\d+)(?:\.(\d+))?", e.get("label", ""))
            if lab:
                n, sub = int(lab.group(1)), lab.group(2)
            elif "_" in num:
                n, sub = int(num.split("_")[0]), num.split("_")[1]
            else:
                n, sub = int(num), None
            img = e.get("img_file")
            img = img if img and img != "None" else (f"item_{n}_{sub}.png" if sub and (d / f"item_{n}_{sub}.png").exists() else f"item_{n}.png")
            key = e["num"] if e["num"] in ans else (int(num) if num.isdigit() and int(num) in ans else num)
            resp = ans.get(key)
            sol = None
            if resp is not None:
                lbl = next((l for l in (e.get("opt_labels") or []) if l.lower().startswith(str(resp).lower() + ".")), None)
                sol = lbl or str(resp)
            items.append(dict(act=act, numero=n, sub=sub, img=img, ctx=ctx, tipus="oberta" if kind == "open_item" else "opcio",
                              punts=float(e["points"]) if e.get("points") else 1.0, resposta=resp, solucio=sol, desc=e.get("desc", "")))
    return acts, items


def index(verbose: bool = True) -> dict:
    con = reset()
    stats = {}
    jobs = []  # (k, sourcedir)
    for k in sorted(STRUCTURES):
        src, dst = source_dir(k), CROPS / prova_id(k)
        if src != dst:
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.glob("*.png"):
                shutil.copy2(f, dst / f.name)
        jobs.append(k)
    files = [str(f) for k in jobs for f in (CROPS / prova_id(k)).glob("*.png")]
    txt = ocr_all(files)
    for k in jobs:
        pid, d = prova_id(k), CROPS / prova_id(k)
        acts, items = parse(k, d)
        rel = lambda f: f"crops/{pid}/{f}" if f and (d / f).exists() else None
        for a in acts:
            a["id"] = f"{pid}_A{a['numero']}"
            ctxs = [c for c in a["contexts"] if (d / c).exists()]
            a["ctext"] = "\n".join(txt[str(d / c)] for c in ctxs)
            con.execute("INSERT INTO activitats VALUES (?,?,?,?,?,?,?)",
                        (a["id"], pid, a["numero"], a["titol"], a["descripcio"], rel(ctxs[0]) if ctxs else None, a["ctext"]))
        for it in items:
            a = it["act"]
            iid = f"{pid}_I{it['numero']}" + (f"_{it['sub']}" if it["sub"] else "")
            row = dict(id=iid, prova=pid, etapa=ETAPA[k[0]], materia=k[1].lower(), any=k[2], convocatoria=CONV[k[0]],
                       activitat_id=a["id"], numero=it["numero"], sub=it["sub"], pare=f"{pid}_I{it['numero']}" if it["sub"] else None,
                       tipus=it["tipus"], punts=it["punts"], bloc=None, tema=None,
                       enunciat_text=txt.get(str(d / it["img"]), "") if rel(it["img"]) else "",
                       solucio_text=it["solucio"] or "", resposta=str(it["resposta"]) if it["resposta"] is not None else None,
                       enunciat_img=rel(it["img"]), context_img=rel(it["ctx"]),
                       context_text=txt.get(str(d / it["ctx"]), "") if rel(it["ctx"]) else a["ctext"],
                       font_pdf=Path(STRUCTURES[k]["pdf_path"]).name)
            con.execute(f"INSERT INTO items ({','.join(row)}) VALUES ({','.join('?' * len(row))})", list(row.values()))
            insert_fts(con, row, a["titol"])
        stats[pid] = len(items)
        if verbose:
            print(f"  {pid}: {len(acts)} activitats, {len(items)} ítems")
    con.commit()
    con.close()
    return stats
