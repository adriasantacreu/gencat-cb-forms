import argparse
from pathlib import Path
import sys

# Assegurar que el directori arrel del paquet és al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from src.downloader import download_exam
    from src.segmenter import segment_pdf
    from src.auditor import audit_crop_directory
    from src.answers_registry import ANSWERS, STRUCTURES
    from src.forms_builder import get_google_services, build_google_form
except ImportError:
    from downloader import download_exam
    from segmenter import segment_pdf
    from auditor import audit_crop_directory
    from answers_registry import ANSWERS, STRUCTURES
    from forms_builder import get_google_services, build_google_form


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline per transformar proves oficials de Competències Bàsiques a Google Forms."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomanda download
    p_down = subparsers.add_parser("download", help="Descarrega els PDFs oficials de Gencat")
    p_down.add_argument("--curs", required=True, choices=["4ESO", "2ESO"], help="Nivell educatiu")
    p_down.add_argument("--materia", required=True, choices=["MAT", "CTE"], help="Matèria")
    p_down.add_argument("--any", required=True, type=int, help="Any de la prova")
    p_down.add_argument("--out", default="downloads", help="Carpeta de descàrrega")

    # Subcomanda segment
    p_seg = subparsers.add_parser("segment", help="Segmenta automàticament el PDF en captures")
    p_seg.add_argument("--pdf", required=True, help="Ruta al PDF de la prova")
    p_seg.add_argument("--out", required=True, help="Carpeta de sortida per a les captures")
    p_seg.add_argument("--dpi", type=int, default=200, help="Resolució DPI")

    # Subcomanda audit
    p_aud = subparsers.add_parser("audit", help="Audita marges blancs i absència de contaminació OCR")
    p_aud.add_argument("--crops", required=True, help="Carpeta amb les captures PNG")
    p_aud.add_argument("--items", required=True, type=int, help="Nombre total d'ítems esperats")

    # Subcomanda build
    p_bld = subparsers.add_parser("build", help="Crea el formulari a Google Forms")
    p_bld.add_argument("--curs", required=True, choices=["4ESO", "2ESO"])
    p_bld.add_argument("--materia", required=True, choices=["MAT", "CTE"])
    p_bld.add_argument("--any", required=True, type=int)
    p_bld.add_argument("--crops", required=True, help="Carpeta amb les captures validades")
    p_bld.add_argument("--credentials", default="credentials.json", help="OAuth credentials de Google")
    p_bld.add_argument("--drive-folder", default="", help="ID de la carpeta a Drive")
    p_bld.add_argument("--assets-folder", required=True, help="ID de la carpeta d'imatges a Drive")
    p_bld.add_argument("--editor", default=None, help="Correu d'editor addicional")

    args = parser.parse_args()

    if args.command == "download":
        out_dir = Path(args.out)
        res = download_exam(args.curs, args.materia, args.any, out_dir)
        print(f"✓ Descàrrega completada:\n  Prova: {res['prova']}\n  Criteris: {res['criteris']}")

    elif args.command == "segment":
        segment_pdf(Path(args.pdf), Path(args.out), dpi=args.dpi)

    elif args.command == "audit":
        ok = audit_crop_directory(Path(args.crops), expected_items=args.items)
        sys.exit(0 if ok else 1)

    elif args.command == "build":
        key = (args.curs, args.materia, args.any)
        answers = ANSWERS.get(key)
        structure = STRUCTURES.get(key)
        if not answers or not structure:
            print(f"❌ Error: No hi ha clau ni estructura registrada per a {key}")
            sys.exit(1)

        m_nom = "Matemàtiques" if args.materia == "MAT" else "Ciència i Tecnologia"
        c_nom = "4t d'ESO" if args.curs == "4ESO" else "2n d'ESO"
        tipus = "Competències bàsiques" if args.curs == "4ESO" else "Avaluació de diagnòstic"

        title = f"{c_nom} · {m_nom} {args.any} · Prova oficial {tipus}"
        description = (
            f"Prova oficial d'avaluació de {tipus} del Departament d'Educació de la Generalitat de Catalunya.\n"
            f"Curs escolar corresponent: {args.any-1}/{args.any}."
        )

        forms_s, drive_s = get_google_services(Path(args.credentials))
        build_google_form(
            forms_service=forms_s,
            drive_service=drive_s,
            title=title,
            description=description,
            structure=structure,
            answers=answers,
            crops_dir=Path(args.crops),
            drive_folder_id=args.drive_folder,
            assets_folder_id=args.assets_folder,
            editor_email=args.editor,
        )


if __name__ == "__main__":
    main()
