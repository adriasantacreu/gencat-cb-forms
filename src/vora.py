"""Captures tallades a la vora: detecta tinta tocant la vora d'una captura i, amb el PDF d'origen, n'ajusta el límit inferior (cb vora [--aplica])."""
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from catalog import CB_DIR, WORKSPACE, connect

POS = Path(__file__).resolve().parents[1] / "data" / "posicions.json"  # caché: captura → pàgina, x, y (al zoom de la prova)
PEU = 808
ZOOMS = (2.0, 200 / 72, 3.0, 1.5)
MARGE = 6            # px blancs que es deixen sota l'última tinta


def tinta_vora(g: np.ndarray, franja: int = 12) -> dict:
    """Tinta a la vora inferior/superior d'una imatge en gris, sense comptar línies contínues (regles, vores de caixa)."""
    out = {}
    for costat, z in (("baix", g[::-1]), ("dalt", g)):
        s = z[:franja] < 200
        vert = s.sum(axis=0) >= franja - 2          # columnes amb ratlla vertical contínua
        fila = s[:2].copy()
        fila[:, vert] = False
        amplada = (z[0] < 200).mean()
        out[costat] = 0 if amplada > 0.7 else int(fila.sum())   # fila 0 = regla horitzontal → vora neta
    return out


def _pagines(pdf: Path, z: float):
    import pymupdf
    d = pymupdf.open(str(pdf))
    ims = []
    for p in d:
        pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
        ims.append(a)
    return d, ims


def _pdfs() -> dict:
    return {p.name: p for p in (WORKSPACE / "docencia/materials/competencies_basiques").rglob("*.pdf")}


def localitza() -> dict:
    """Troba cada captura dins la pàgina del seu PDF (template matching). Retorna {prova: {zoom, fitxers:{nom:[pag,x,y,h,w,score]}}}."""
    con, pdfs = connect(), _pdfs()
    font = {r[0]: r[1] for r in con.execute("SELECT prova, font_pdf FROM items GROUP BY prova")}
    res = {}
    for prova, pdf in sorted(font.items()):
        fitxers = sorted((CB_DIR / "crops" / prova).glob("*.png"))
        millor = None
        for z in ZOOMS:
            d, ims = _pagines(pdfs[pdf], z)
            grays = [cv2.cvtColor(a, cv2.COLOR_RGB2GRAY) for a in ims]
            pos, ok = {}, 0
            for f in fitxers:
                t = cv2.imread(str(f), 0)
                h, w = t.shape
                best = (-1, None)
                for n, g in enumerate(grays):
                    if g.shape[0] < h or g.shape[1] < w:
                        continue
                    _, mv, _, ml = cv2.minMaxLoc(cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED))
                    if mv > best[0]:
                        best = (mv, (n, ml))
                if best[0] > 0.93:
                    n, (x, y) = best[1]
                    pos[f.name] = [n, x, y, h, w, round(float(best[0]), 3)]
                    ok += 1
            if millor is None or ok > millor[0]:
                millor = (ok, z, pos)
            if ok >= 0.95 * len(fitxers):
                break
        res[prova] = {"zoom": millor[1], "fitxers": millor[2], "total": len(fitxers)}
        print(f"{prova}: {millor[0]}/{len(fitxers)} localitzades (zoom {millor[1]:.2f})", flush=True)
    POS.write_text(json.dumps(res, indent=0))
    return res


def _logo_y(page) -> float:
    """Límit superior (pt) del logo/peu de pàgina, si n'hi ha, sota el contingut."""
    ys = [b["bbox"][1] for b in page.get_image_info() if b["bbox"][1] > 740 and (b["bbox"][2] - b["bbox"][0]) < 200 and b["bbox"][3] > 800]
    ys += [b[1] for b in page.get_text("blocks") if b[1] > 740 and re.search(r"consell superior|avaluaci", b[4], re.I)]
    return min(ys) if ys else PEU


def nou_limit(gris, pos, altres, z, logo_pt, permet_encongir=False) -> tuple:
    """(nova_alçada, motiu) d'una captura: fins a l'inici de la captura següent o fins on acaba el contingut contigu."""
    pag, x, y, h, w = pos[:5]
    sota = [a for a in altres if a[0] > y + 0.3 * h and a[0] >= y + 40 and min(x + w, a[1] + a[2]) - max(x, a[1]) > 0.5 * min(w, a[2])]
    T = min((a[0] for a in sota), default=None)
    F = int(min(PEU, logo_pt - 4) * z)
    L = min(F, T - 4) if T else F
    lim = max(L, y + 40)
    zona = gris[y:lim, x:x + w] < 200
    if zona.size == 0:
        return h, "sense zona"
    frac = zona.mean(axis=1)
    tinta = np.where(frac > 0)[0]
    if len(tinta) == 0:
        return h, "sense tinta"
    # segments de tinta separats per buits; un segment fet només de regla (>70% fila) és una separació, no contingut
    buit = int(12 * z / 2)
    segs, ini, prev = [], tinta[0], tinta[0]
    for r in tinta[1:]:
        if r - prev > buit:
            segs.append((ini, prev)); ini = r
        prev = r
    segs.append((ini, prev))
    segs = [s for s in segs if not (frac[s[0]:s[1] + 1] > 0.7).all()]
    if not segs:
        return h, "només regles"
    # sense captura veïna: parar al primer buit gran després de l'alçada actual (logo/peu)
    gran = int(28 * z / 2)
    fi = segs[0][1]
    for a, b in segs[1:]:
        if T is None and a - fi > gran and a > h:
            break
        fi = b
    nova = min(fi + 1 + MARGE, lim - y)
    return max(nova, 10), ("fins a la següent" if T else "fins al contingut")


def _emblanqueix(a, blocs, z):
    """Emblanquina cada bloc «NO ESCRIGUIS AQUEST ESPAI» / «Respon a la PART 2» (icona inclosa), un per un: mai el text d'entremig."""
    for b in blocs:
        a[max(int((b[1] - 2) * z), 0):int((b[3] + 2) * z), max(int((b[0] - 14) * z), 0):int((b[2] + 4) * z)] = 255


def _net(g, x, w, y0, y1):
    """Files (y0..y1) de la pàgina sense tinta dins l'amplada de la captura, ignorant ratlles verticals contínues (vores de caixa)."""
    z = g[max(y0, 0):y1, x:x + w] < 200
    if z.size == 0:
        return np.zeros(0, bool)
    vert = z.mean(axis=0) > 0.85
    z[:, vert] = False
    return ~z.any(axis=1)


def _cos(g, x, w, bnd, z, radi=220, context=False):
    """Costura entre dues captures adjacents. Retorna (None, True) si la frontera ja és en una franja en blanc ampla (separació d'ítems),
    (franja, True) si la mou a la franja en blanc ampla més propera (una línia o un paràgraf tallats), o (None, False) si no n'hi ha cap."""
    mins = int((4 if context else 14) * z / 2)   # un context acaba sempre en un límit net (caixa): només es mou si talla tinta
    # (ítems: 14 = més ample que l'interlineat, és una separació real)
    lo0 = max(bnd - radi, 0)
    net = _net(g, x, w, lo0, bnd + radi)
    if len(net) == 0:
        return None, False
    c = bnd - lo0
    if net[c]:
        i = j = c
        while i > 0 and net[i - 1]:
            i -= 1
        while j < len(net) - 1 and net[j + 1]:
            j += 1
        if j - i + 1 >= mins:
            return None, True
    def cerca(pas):
        i, run = c, 0
        while 0 <= i < len(net):
            run = run + 1 if net[i] else 0
            if run >= mins:
                return (i - run + 1, i, abs(i - c)) if pas > 0 else (i, i + run - 1, abs(i - c))
            i += pas
        return None
    cand = [r for r in (cerca(1), cerca(-1)) if r]
    if not cand:
        return None, False
    ini, fi, _ = min(cand, key=lambda r: r[2])
    return (lo0 + ini, lo0 + fi), True


def ancora_titols(cs, page, z):
    """Un ítem ha de començar al seu número («12.»). Si la captura comença sota el número, hi puja i retalla la captura de sobre (context o ítem)."""
    paraules = page.get_text("words")
    for c in cs:
        m = re.fullmatch(r"item_(\d+)\.png", c["nom"])
        if not m:
            continue
        cand = [b for b in paraules if b[4] == m.group(1) + "." and c["x"] / z - 40 <= b[0] <= c["x"] / z + 90
                and c["y0"] - 420 * z / 2 < b[1] * z < c["y0"] - 3]
        if not cand:
            continue
        ny = int(max(cand, key=lambda b: b[1])[1] * z) - int(6 * z / 2)
        for a in cs:
            if a is not c and a["y0"] < ny - 40 and a["y1"] > ny and min(a["x"] + a["w"], c["x"] + c["w"]) - max(a["x"], c["x"]) > 0.5 * min(a["w"], c["w"]):
                a["y1"] = ny - 2
        c["y0"] = ny


def arregla(aplica: bool, cartes: Path, copia: Path, exclou=()) -> int:
    pos = json.loads(POS.read_text()) if POS.exists() else localitza()
    con, pdfs = connect(), _pdfs()
    font = {r[0]: r[1] for r in con.execute("SELECT prova, font_pdf FROM items GROUP BY prova")}
    cartes.mkdir(parents=True, exist_ok=True)
    canvis, revisar = [], []
    for prova, info in sorted(pos.items()):
        if prova in exclou:
            continue
        z = info["zoom"]
        d, ims = _pagines(pdfs[font[prova]], z)
        pags = defaultdict(list)
        for nom, (n, x, y, h, w, _) in info["fitxers"].items():
            pags[n].append({"nom": nom, "x": x, "w": w, "y0": y, "y1": y + h, "o0": y, "o1": y + h})
        for n, cs in pags.items():
            a = ims[n].copy()
            blocs = [b for b in d[n].get_text("blocks") if re.search(r"no escriguis|respon a la part", b[4], re.I)]
            _emblanqueix(a, blocs, z)
            g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
            cs.sort(key=lambda c: c["y0"])
            if "MAT" in prova:                # 0) ítems que comencen després del seu número: puja la capçalera (el PDF de MAT té text fiable)
                ancora_titols(cs, d[n], z)
                cs.sort(key=lambda c: c["y0"])
            veina = {}
            for A, B in zip(cs, cs[1:]):      # 1) costures entre captures adjacents
                if min(A["x"] + A["w"], B["x"] + B["w"]) - max(A["x"], B["x"]) < 0.5 * min(A["w"], B["w"]):
                    continue
                if -15 <= B["y0"] - A["y1"] <= 12:
                    r, ok = _cos(g, A["x"], A["w"], (A["y1"] + B["y0"]) // 2, z, context=A["nom"].startswith("context_"))
                    veina[A["nom"]] = ok
                    if r:
                        ini, fi = r
                        m = min(MARGE, (fi - ini) // 2)
                        A["y1"], B["y0"] = ini + m + 1, fi - m
            logo = _logo_y(d[n])
            for c in cs:                      # 2) cap sense veïna: allarga fins al contingut (o encongeix si en conté una altra)
                altres = [(o["y0"], o["x"], o["w"]) for o in cs if o is not c]
                p = [n, c["x"], c["y0"], c["y1"] - c["y0"], c["w"]]
                dins = [o for o in altres if c["y0"] + 40 < o[0] < c["y1"] - 3 and not c["nom"].startswith("context_")
                        and min(c["x"] + c["w"], o[1] + o[2]) - max(c["x"], o[1]) > 0.5 * min(c["w"], o[2])]
                if c["y1"] > int(logo * z) - 2 and c["y0"] < int(logo * z) - 40:     # 0) la captura s'ha colat al logo del peu
                    nova, _ = nou_limit(g, p, altres, z, logo, permet_encongir=True)
                    if nova < p[3]:
                        c["y1"] = c["y0"] + nova
                        continue
                if any(c["y0"] < b[1] * z < c["y1"] < (b[3] + 2) * z for b in blocs) and tinta_vora(cv2.imread(str(CB_DIR / "crops" / prova / c["nom"]), 0))["baix"] > 0:   # 0b) el límit travessa un «NO ESCRIGUIS»: acaba on s'acaba el contingut
                    nova, _ = nou_limit(g, p, altres, z, logo)
                    if 40 < nova < p[3]:
                        c["y1"] = c["y0"] + nova
                        continue
                vora = tinta_vora(g[c["y0"]:c["y1"], c["x"]:c["x"] + c["w"]])["baix"]
                if veina.get(c["nom"]) or (vora <= 0 and not dins):
                    continue
                nova, _ = nou_limit(g, p, altres, z, logo)
                if not dins:
                    nova = max(nova, p[3])
                c["y1"] = c["y0"] + nova
        for n, cs in pags.items():
            g = None
            for c in cs:
                if (c["y0"], c["y1"]) == (c["o0"], c["o1"]):
                    v = tinta_vora(cv2.cvtColor(cv2.imread(str(CB_DIR / "crops" / prova / c["nom"])), cv2.COLOR_BGR2GRAY))
                    if v["baix"] > 0:
                        revisar.append((prova, c["nom"], c["o1"] - c["o0"], "tinta a la vora inferior, sense canvi"))
                    continue
                canvis.append((prova, c["nom"], f'{c["o0"]}-{c["o1"]}', f'{c["y0"]}-{c["y1"]}'))
                # imatge de la pàgina amb el «NO ESCRIGUIS» emblanquinat (mateixa pàgina que s'ha analitzat)
                a = ims[n].copy()
                blocs = [b for b in d[n].get_text("blocks") if re.search(r"no escriguis|respon a la part", b[4], re.I)]
                _emblanqueix(a, blocs, z)
                sortida = a[c["y0"]:c["y1"], c["x"]:c["x"] + c["w"]]
                cols = np.where((cv2.cvtColor(sortida, cv2.COLOR_RGB2GRAY) < 200).any(axis=0))[0]
                if len(cols):                 # ajusta els costats al contingut (el «NO ESCRIGUIS»/logo eren els qui allargaven l'amplada)
                    x0, x1 = max(cols[0] - 8, 0), min(cols[-1] + 9, sortida.shape[1])
                    if x0 > 7 or sortida.shape[1] - x1 > 7:
                        c["x"], c["w"] = c["x"] + x0, x1 - x0
                        sortida = sortida[:, x0:x1]
                sortida = np.ascontiguousarray(sortida[:, :, ::-1])
                cv2.imwrite(str(cartes / f"{prova}__{c['nom']}"), sortida)
                if aplica:
                    f = CB_DIR / "crops" / prova / c["nom"]
                    cp = copia / prova / c["nom"]
                    cp.parent.mkdir(parents=True, exist_ok=True)
                    if not cp.exists():
                        shutil.copy2(f, cp)
                    cv2.imwrite(str(f), sortida)
                    pr = info["fitxers"][c["nom"]]
                    info["fitxers"][c["nom"]] = [n, c["x"], c["y0"], c["y1"] - c["y0"], c["w"], pr[5]]
    for c in canvis:
        print("canvi", *c)
    for r in revisar:
        print("REVISAR", *r)
    print(f"{len(canvis)} canvis{' aplicats' if aplica else ' (simulació)'} · {len(revisar)} per revisar")
    if aplica:
        POS.write_text(json.dumps(pos, indent=0, default=int))
    return 0


def retalla_marges(aplica: bool = True) -> int:
    """Retalla el blanc sobrant (>15 px) de les vores de cada captura fins a 8 px: deixa net el que `cb check` (g-marges) demana."""
    n = 0
    for f in sorted((CB_DIR / "crops").glob("*/*.png")):
        im = cv2.imread(str(f))
        ink = im.min(axis=2) < 248        # mateix criteri que auditor.check_margins
        ys, xs = np.where(ink.any(axis=1))[0], np.where(ink.any(axis=0))[0]
        if len(ys) == 0:
            continue
        h, w = ink.shape
        y0, y1, x0, x1 = max(ys[0] - 8, 0), min(ys[-1] + 9, h), max(xs[0] - 8, 0), min(xs[-1] + 9, w)
        if ys[0] > 15 or h - 1 - ys[-1] > 15 or xs[0] > 15 or w - 1 - xs[-1] > 15:
            n += 1
            print("marges", f.parent.name, f.name)
            if aplica:
                cv2.imwrite(str(f), im[y0:y1, x0:x1])
    print(f"{n} captures retallades")
    return 0


def main(args):
    if args and args[0] == "localitza":
        localitza()
        return 0
    if args and args[0] == "marges":
        return retalla_marges("--simula" not in args)
    aplica = "--aplica" in args
    tmp = Path(os.environ.get("VORA_TMP", "/tmp/vora"))
    exclou = [a.split("=", 1)[1] for a in args if a.startswith("--exclou=")]
    return arregla(aplica, tmp / "previews", tmp / "copia", exclou)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
