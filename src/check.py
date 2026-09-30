"""`cb check`: la BD de CCBB és completa i les captures són netes (recompte = registre, 0 duplicats, marges, contexts sense enunciats)."""
import csv

import cv2
import hashlib
import re
from collections import defaultdict
from pathlib import Path

from answers_registry import STRUCTURES
from auditor import check_margins
from catalog import CB_DIR, connect
from vora import tinta_vora
from indexer import ETAPA, OCR_CACHE, prova_id

EXCEPCIONS = Path(__file__).resolve().parents[1] / "data" / "excepcions.csv"
ITEM_RE = re.compile(r"^\s*([0-9]{1,2})\.\s+([A-ZÀ-Ú][a-zà-ú]+)")  # mateix patró que auditor.check_context_contamination


def excepcions() -> set:
    if not EXCEPCIONS.exists():
        return set()
    with open(EXCEPCIONS, newline="", encoding="utf-8") as f:
        return {(r["id"], r["check"]) for r in csv.DictReader(f)}


def run() -> int:
    import json
    con, exc = connect(), excepcions()
    rows = [dict(r) for r in con.execute("SELECT * FROM items")]
    acts = {r["id"]: dict(r) for r in con.execute("SELECT * FROM activitats")}
    ocr = json.loads(OCR_CACHE.read_text()) if OCR_CACHE.exists() else {}
    fails = defaultdict(list)

    def bad(check, id_, msg):
        if (id_, check) not in exc:
            fails[check].append(f"{id_}: {msg}")

    # a. recompte per prova = registre (ítems amb clau + oberts)
    by = defaultdict(int)
    for r in rows:
        by[r["prova"]] += 1
    for k, s in STRUCTURES.items():
        n = sum(1 for e in s["elements"] if e["kind"] in ("item", "open_item"))
        if by[prova_id(k)] != n:
            bad("a-recompte", prova_id(k), f"BD {by[prova_id(k)]} ≠ registre {n}")
    # b–d. captura, text i clau de cada ítem
    hashes = defaultdict(set)
    for r in rows:
        f = CB_DIR / r["enunciat_img"] if r["enunciat_img"] else None
        if not f or not f.exists():
            bad("b-captura", r["id"], "sense captura")
            continue
        hashes[hashlib.sha1(f.read_bytes()).hexdigest()].add((r["pare"] or r["id"]))
        if len((r["enunciat_text"] or "").strip()) < 15:
            bad("c-text", r["id"], "text d'enunciat buit")
        if r["tipus"] == "opcio" and not r["solucio_text"]:
            bad("d-clau", r["id"], "sense resposta del registre")
        c = CB_DIR / r["context_img"] if r["context_img"] else None
        if not c or not c.exists():
            bad("e-context", r["id"], "sense context")
    # f. 0 captures repetides entre ítems diferents (les sub-preguntes comparteixen la del pare)
    for h, grp in hashes.items():
        if len(grp) > 1:
            bad("f-duplicat", sorted(grp)[0], f"mateixa captura per a {sorted(grp)}")
    # g. marges ≤ 15 px a totes les captures; i. cap tinta a la vora inferior; h. cap context conté un enunciat d'ítem (text OCR ja calculat)
    for png in sorted((CB_DIR / "crops").glob("*/*.png")):
        m = check_margins(png)
        if not m["ok"]:
            bad("g-marges", f"{png.parent.name}/{png.name}", m.get("details") or m.get("error"))
        v = tinta_vora(cv2.cvtColor(cv2.imread(str(png)), cv2.COLOR_BGR2GRAY))
        if v["baix"] > 0:   # tinta tocant la vora inferior = captura tallada per sota (ratlles contínues no compten)
            bad("i-vora", f"{png.parent.name}/{png.name}", f"tinta a la vora inferior ({v['baix']} px): captura tallada? (cb vora)")
        if png.stem.startswith("context_"):
            t = ocr.get(hashlib.sha1(png.read_bytes()).hexdigest(), "")
            cont = [ln for ln in t.splitlines() if (mm := ITEM_RE.match(ln)) and 1 <= int(mm.group(1)) <= 45]
            if cont:
                bad("h-context-net", f"{png.parent.name}/{png.name}", f"conté {cont[:2]}")
    n_fail = sum(len(v) for v in fails.values())
    checks = ["a-recompte", "b-captura", "c-text", "d-clau", "e-context", "f-duplicat", "g-marges", "h-context-net", "i-vora"]
    for c in checks:
        print(f"{'✓' if not fails[c] else '✗'} {c}: {len(fails[c])} errors")
        for m in fails[c][:8]:
            print("    ", m)
    print(f"{len(rows)} ítems, {len(acts)} activitats, {len(exc)} excepcions · {'VERD' if not n_fail else f'{n_fail} ERRORS'}")
    return 1 if n_fail else 0
