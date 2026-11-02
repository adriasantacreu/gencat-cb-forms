#!/usr/bin/env python3
"""
Descarregador oficial de proves de Competències Bàsiques i Avaluacions Diagnòstiques (Generalitat de Catalunya).
Font: Agència d'Avaluació i Prospectiva de l'Educació (avaluacioeducativa.gencat.cat).

Ús:
  python3 scripts/descarrega_cb.py
"""

import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
BASE_DIR = WORKSPACE / "docencia" / "materials" / "competencies_basiques"

BASE_URL = "https://avaluacioeducativa.gencat.cat"

# Llista canònica de documents de Matemàtiques i Ciència-Tecnologia (4t i 2n d'ESO)
DOCUMENTS = [
    # ── 4t d'ESO (Final d'etapa · Matemàtiques) ─────────────────────────────
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2025-2026",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2026_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2025-2026/matematica/A4S-26-MAT.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2025-2026",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2026_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2025-2026/matematica/A4S-26-MAT-Descripció_prova_Especificacions_Clau_respostes.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2024-2025",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2025_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2024-2025/matematica/prova-matematica-a4s2025.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2024-2025",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2025_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2024-2025/matematica/criteris-correccio-matematica-a4s2025.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2023-2024",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2024_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2023-2024/matematica/prova-matematica-a4s2024.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2023-2024",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2024_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2023-2024/matematica/criteris-correccio-matematica-a4s2024.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2022-2023",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2023_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2022-2023/matematica/prova-matematica-a4s2023.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2022-2023",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2023_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2022-2023/matematica/criteris-correccio-matematica-a4s2023.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2021-2022",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2022_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2021-2022/matematica/prova-matematica-a4s2022.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2021-2022",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2022_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2021-2022/matematica/criteris-correccio-matematica-a4s2022.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2020-2021",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2021_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2020-2021/matematica/prova-matematica-a4s2021.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "matematiques",
        "any": "2020-2021",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2021_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2020-2021/matematica/criteris-correccio-matematica-a4s2021.pdf"
    },

    # ── 4t d'ESO (Ciència, Tecnologia i Enginyeria · CTE) ───────────────────
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2025-2026",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2026_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2025-2026/ciencia/A4S-26-CTE.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2025-2026",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2026_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2025-2026/ciencia/A4S-26-CTE-Descripció_prova_Especificacions_Clau_respostes.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2024-2025",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2025_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2024-2025/ciencia/prova-ciencia-a4s2025.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2024-2025",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2025_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2024-2025/ciencia/criteris-correccio-ciencia-a4s2025.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2023-2024",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2024_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2023-2024/ciencia/prova-ciencia-a4s2024.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2023-2024",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2024_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2023-2024/ciencia/criteris-correccio-ciencia-a4s2024.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2022-2023",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2023_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2022-2023/ciencia/prova-ciencia-a4s2023.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2022-2023",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2023_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2022-2023/ciencia/criteris-correccio-ciencia-a4s2023.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2021-2022",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2022_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2021-2022/ciencia/prova-ciencia-a4s2022.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2021-2022",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2022_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2021-2022/ciencia/criteris-correccio-ciencia-a4s2022.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2020-2021",
        "tipus": "prova",
        "fitxer": "4ESO_CB_2021_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2020-2021/ciencia/prova-ciencia-a4s2021.pdf"
    },
    {
        "etapa": "4ESO",
        "materia": "ciencia_tecnologia",
        "any": "2020-2021",
        "tipus": "criteris",
        "fitxer": "4ESO_CB_2021_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/final-etapa/quart-eso/2020-2021/ciencia/criteris-correccio-ciencia-a4s2021.pdf"
    },

    # ── 2n d'ESO (Avaluació diagnòstica · Matemàtiques) ─────────────────────
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2025-2026",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2026_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2025-2026/matematiques/AD2S-26-MAT.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2025-2026",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2026_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2025-2026/matematiques/AD2S-26-MAT-Descripció%20prova_Especificacions%20ítems_Clau%20de%20respostes.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2024-2025",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2025_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2024-2025/quaderns-proves/ad2s2025-mat.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2024-2025",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2025_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2024-2025/solucionari-ad2s-24-25.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2023-2024",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2024_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2023-2024/quaderns-proves/ad2s2024-matematiques-ac.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "matematiques",
        "any": "2023-2024",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2024_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2023-2024/solucionari-ad2s-23-24.pdf"
    },

    # ── 2n d'ESO (Avaluació diagnòstica · Ciència i Tecnologia · CIE/CTE) ───
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2025-2026",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2026_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2025-2026/ciencia/AD2S-26-CIE.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2025-2026",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2026_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2025-2026/ciencia/AD2S-26-CIE-Descripcio%20prova_Especificacions%20ítems_Clau_de_respostes.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2024-2025",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2025_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2024-2025/quaderns-proves/ad2s2025-cie.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2024-2025",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2025_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2024-2025/solucionari-ad2s-24-25.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2023-2024",
        "tipus": "prova",
        "fitxer": "2ESO_AD_2024_CTE_prova.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2023-2024/quaderns-proves/ad2s2024-cte-ac.pdf"
    },
    {
        "etapa": "2ESO",
        "materia": "ciencia_tecnologia",
        "any": "2023-2024",
        "tipus": "criteris",
        "fitxer": "2ESO_AD_2024_CTE_criteris.pdf",
        "url": "/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions/diagnostic/segon-eso/2023-2024/solucionari-ad2s-23-24.pdf"
    },
]


def descarrega():
    headers = {"User-Agent": "Mozilla/5.0"}
    descarregats = 0
    errors = 0

    for doc in DOCUMENTS:
        materia = doc.get("materia", "matematiques")
        dest_dir = BASE_DIR / doc["etapa"] / materia
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / doc["fitxer"]

        if dest_path.exists() and dest_path.stat().st_size > 1000:
            print(f"✓ Ja existeix: {doc['etapa']}/{materia}/{doc['fitxer']}")
            continue

        raw_url = BASE_URL + doc["url"]
        url_parts = raw_url.split("://", 1)
        scheme = url_parts[0]
        rest = url_parts[1]
        domain, path = rest.split("/", 1)
        encoded_path = urllib.parse.quote(path, safe="/%_.-")
        final_url = f"{scheme}://{domain}/{encoded_path}"

        print(f"↓ Descarregant {doc['fitxer']}...")
        try:
            req = urllib.request.Request(final_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                dest_path.write_bytes(data)
                print(f"  ✓ Desat ({len(data) // 1024} KB)")
                descarregats += 1
        except Exception as e:
            print(f"  ✗ Error descarregant {final_url}: {e}")
            errors += 1

    print(f"\nFinalitzat: {descarregats} nous descarregats, {errors} errors.")


if __name__ == "__main__":
    descarrega()
