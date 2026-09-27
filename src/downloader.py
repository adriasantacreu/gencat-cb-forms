"""Mòdul de descàrrega oficial de proves de l'Agència d'Avaluació i Prospectiva de l'Educació (Gencat)."""

from pathlib import Path
import requests

BASE_URL = "https://avaluacioeducativa.gencat.cat/content/dam/avaluacioeducativa/avaluacio-educativa/avaluacions"

CATALOG = {
    # 4t d'ESO Matemàtiques
    ("4ESO", "MAT", 2026, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2025-2026/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2026, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2025-2026/guia/competencia-matematica.pdf",
    ("4ESO", "MAT", 2025, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2024-2025/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2025, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2024-2025/guia/competencia-matematica.pdf",
    ("4ESO", "MAT", 2024, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2023-2024/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2024, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2023-2024/guia/competencia-matematica.pdf",
    ("4ESO", "MAT", 2023, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2022-2023/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2023, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2022-2023/guia/competencia-matematica.pdf",
    ("4ESO", "MAT", 2022, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2021-2022/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2022, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2021-2022/guia/competencia-matematica.pdf",
    ("4ESO", "MAT", 2021, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2020-2021/quaderns/competencia-matematica.pdf",
    ("4ESO", "MAT", 2021, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2020-2021/guia/competencia-matematica.pdf",
    # 4t d'ESO Ciència i Tecnologia
    ("4ESO", "CTE", 2026, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2025-2026/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2026, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2025-2026/guia/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2025, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2024-2025/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2025, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2024-2025/guia/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2024, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2023-2024/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2024, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2023-2024/guia/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2023, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2022-2023/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2023, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2022-2023/guia/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2022, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2021-2022/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2022, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2021-2022/guia/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2021, "prova"): f"{BASE_URL}/final-etapa/quart-eso/curs-2020-2021/quaderns/competencia-cientifico-tecnologica.pdf",
    ("4ESO", "CTE", 2021, "criteris"): f"{BASE_URL}/final-etapa/quart-eso/curs-2020-2021/guia/competencia-cientifico-tecnologica.pdf",
    # 2n d'ESO Avaluació Diagnòstica Matemàtiques
    ("2ESO", "MAT", 2026, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2025-2026/quaderns/competencia-matematica.pdf",
    ("2ESO", "MAT", 2026, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2025-2026/guia/competencia-matematica.pdf",
    ("2ESO", "MAT", 2025, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2024-2025/quaderns/competencia-matematica.pdf",
    ("2ESO", "MAT", 2025, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2024-2025/guia/competencia-matematica.pdf",
    ("2ESO", "MAT", 2024, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2023-2024/quaderns/competencia-matematica.pdf",
    ("2ESO", "MAT", 2024, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2023-2024/guia/competencia-matematica.pdf",
    # 2n d'ESO Avaluació Diagnòstica Ciència i Tecnologia
    ("2ESO", "CTE", 2026, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2025-2026/quaderns/competencia-cientifico-tecnologica.pdf",
    ("2ESO", "CTE", 2026, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2025-2026/guia/competencia-cientifico-tecnologica.pdf",
    ("2ESO", "CTE", 2025, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2024-2025/quaderns/competencia-cientifico-tecnologica.pdf",
    ("2ESO", "CTE", 2025, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2024-2025/guia/competencia-cientifico-tecnologica.pdf",
    ("2ESO", "CTE", 2024, "prova"): f"{BASE_URL}/diagnostic/segon-eso/curs-2023-2024/quaderns/competencia-cientifico-tecnologica.pdf",
    ("2ESO", "CTE", 2024, "criteris"): f"{BASE_URL}/diagnostic/segon-eso/curs-2023-2024/guia/competencia-cientifico-tecnologica.pdf",
}


def download_file(url: str, dest_path: Path) -> bool:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        print(f"  ✓ Ja existeix: {dest_path.name}")
        return True
    print(f"  ↓ Descarregant: {url}")
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            dest_path.write_bytes(r.content)
            print(f"  ✓ Descarregat: {dest_path.name} ({len(r.content) // 1024} KB)")
            return True
        else:
            print(f"  ✗ Error HTTP {r.status_code} per a {url}")
            return False
    except Exception as e:
        print(f"  ✗ Error en descarregar {url}: {e}")
        return False


def download_exam(curs: str, materia: str, any_curs: int, out_dir: Path) -> dict:
    prova_url = CATALOG.get((curs, materia, any_curs, "prova"))
    criteris_url = CATALOG.get((curs, materia, any_curs, "criteris"))
    if not prova_url or not criteris_url:
        raise ValueError(f"No hi ha URLs catalogades per a {curs} {materia} {any_curs}")

    prova_path = out_dir / f"{curs}_{materia}_{any_curs}_prova.pdf"
    criteris_path = out_dir / f"{curs}_{materia}_{any_curs}_criteris.pdf"

    download_file(prova_url, prova_path)
    download_file(criteris_url, criteris_path)

    return {"prova": prova_path, "criteris": criteris_path}
