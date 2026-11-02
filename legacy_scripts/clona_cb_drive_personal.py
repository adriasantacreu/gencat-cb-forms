#!/usr/bin/env python3
"""Clona els 18 formularis de Competències Bàsiques i Diagnòstiques al compte de Google Drive personal."""

import json
import subprocess
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

WS = Path(__file__).resolve().parent.parent
SECRET = str(WS / "scripts" / "secret")
TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/drive"]

FORMULARIS = [
    # 4ESO MAT
    {"curs": "4ESO", "materia": "MAT", "any": 2026, "id": "1W2y_rWOy4aHeerESMNATtjH8cjFyqeBrJZfsG5rS1Ao", "subfolder": "01_4ESO_Matematiques"},
    {"curs": "4ESO", "materia": "MAT", "any": 2025, "id": "1S8R0GAGAumzls4G5dYpadIx-IO0Tk0lfCnZapf2htwg", "subfolder": "01_4ESO_Matematiques"},
    {"curs": "4ESO", "materia": "MAT", "any": 2024, "id": "1e7x0jiJTRfRF4GvldK2n-zKb7fd740DG_viV_jtZW8I", "subfolder": "01_4ESO_Matematiques"},
    {"curs": "4ESO", "materia": "MAT", "any": 2023, "id": "1TKJ-0VO6E2L8Acwgh1Tin5ROZhcjVc7wrGknEkSNRkk", "subfolder": "01_4ESO_Matematiques"},
    {"curs": "4ESO", "materia": "MAT", "any": 2022, "id": "1Vc5Ac5JqmDgpCtsYLFEnxUkrTnDcoVG3_g14WA-TD8Q", "subfolder": "01_4ESO_Matematiques"},
    {"curs": "4ESO", "materia": "MAT", "any": 2021, "id": "1PrB7WbruWFsbaZf36ghpndK41Y1Vq1PECmGNdNN95JA", "subfolder": "01_4ESO_Matematiques"},

    # 4ESO CTE
    {"curs": "4ESO", "materia": "CTE", "any": 2026, "id": "1GxWihmZzn9ihk1xAlMw8IsMLwlYPrGweRFnY4g58VCI", "subfolder": "02_4ESO_Ciencia_Tecnologia"},
    {"curs": "4ESO", "materia": "CTE", "any": 2025, "id": "1jyodOIRqJElQhtMALa6A2_O2N08zz0H8nuzuUoF36lQ", "subfolder": "02_4ESO_Ciencia_Tecnologia"},
    {"curs": "4ESO", "materia": "CTE", "any": 2024, "id": "1bCpK0riVGr98dpSjM8eXJX-NBx7-73nzXR4dXAKVTXg", "subfolder": "02_4ESO_Ciencia_Tecnologia"},
    {"curs": "4ESO", "materia": "CTE", "any": 2023, "id": "1lNYaiNpFn-cB36ECtcY-4Fvlyqv6aSdmFO6D5kE8IM8", "subfolder": "02_4ESO_Ciencia_Tecnologia"},
    {"curs": "4ESO", "materia": "CTE", "any": 2022, "id": "1GXxvajRfJK4NvGnPrAJuJrjSzHuaaTpVKafB-RyP65M", "subfolder": "02_4ESO_Ciencia_Tecnologia"},
    {"curs": "4ESO", "materia": "CTE", "any": 2021, "id": "1Ot8U3tEA1fVoZ04pVNQAEIDqGvkVscoG8GIm_rIxX9U", "subfolder": "02_4ESO_Ciencia_Tecnologia"},

    # 2ESO MAT
    {"curs": "2ESO", "materia": "MAT", "any": 2026, "id": "1nAnrxjz3tC_-7O_2nmPOW8P4IdYJAFJY3rFsHCqCn6k", "subfolder": "03_2ESO_Matematiques"},
    {"curs": "2ESO", "materia": "MAT", "any": 2025, "id": "15LBzQDA42CSyEBwGODGUnyeiHCjTLI9flRbYghyCZDs", "subfolder": "03_2ESO_Matematiques"},
    {"curs": "2ESO", "materia": "MAT", "any": 2024, "id": "1w5BZVZ33xz7HwCqbScONBQBhBIB398PFaR5t1gncHaY", "subfolder": "03_2ESO_Matematiques"},

    # 2ESO CTE
    {"curs": "2ESO", "materia": "CTE", "any": 2026, "id": "1IqwDm94mpsb8wAx3v-8VZ67D2pCczqlVzn2kw_Q5zXU", "subfolder": "04_2ESO_Ciencia_Tecnologia"},
    {"curs": "2ESO", "materia": "CTE", "any": 2025, "id": "1qRu8ENWkrUSMr5VRHcSIYmEll9xKMj5MpZquctJg1t8", "subfolder": "04_2ESO_Ciencia_Tecnologia"},
    {"curs": "2ESO", "materia": "CTE", "any": 2024, "id": "1L8_ZWCAFzYpl7ckruCIKBcNaLoahUpz_h-61QHfp6ns", "subfolder": "04_2ESO_Ciencia_Tecnologia"},
]


def get_secret(name):
    r = subprocess.run([SECRET, "get", name], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Error obtenint secret {name}: {r.stderr.strip()}")
    return r.stdout.strip()


def get_personal_drive():
    cid = get_secret("GOOGLE_OAUTH_CLIENT_ID")
    csec = get_secret("GOOGLE_OAUTH_CLIENT_SECRET")
    tok = json.loads(get_secret("GOOGLE_TOKEN_PERSONAL"))
    creds = Credentials(
        None,
        refresh_token=tok["refresh_token"],
        token_uri=TOKEN_URI,
        client_id=cid,
        client_secret=csec,
        scopes=SCOPES,
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_or_create_folder(drive_svc, name, parent_id="root"):
    query = f"mimeType = 'application/vnd.google-apps.folder' and name = '{name}' and trashed = false and '{parent_id}' in parents"
    res = drive_svc.files().list(q=query, fields="files(id, name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    f = drive_svc.files().create(body=meta, fields="id").execute()
    print(f"📁 Creada carpeta: {name} (ID: {f['id']})")
    return f["id"]


def main():
    print("🚀 Connectant a Google Drive personal...")
    drive_p = get_personal_drive()

    # 1. Carpeta arrel al Drive personal
    root_folder_name = "Competències bàsiques i diagnòstiques (Portafoli)"
    root_id = find_or_create_folder(drive_p, root_folder_name, parent_id="root")

    # Fer la carpeta arrel pública de lectura
    try:
        drive_p.permissions().create(fileId=root_id, body={"role": "reader", "type": "anyone"}).execute()
    except Exception:
        pass

    # 2. Subcarpetes
    subfolders = {}
    for sf in ["01_4ESO_Matematiques", "02_4ESO_Ciencia_Tecnologia", "03_2ESO_Matematiques", "04_2ESO_Ciencia_Tecnologia"]:
        sf_id = find_or_create_folder(drive_p, sf, parent_id=root_id)
        try:
            drive_p.permissions().create(fileId=sf_id, body={"role": "reader", "type": "anyone"}).execute()
        except Exception:
            pass
        subfolders[sf] = sf_id

    # 3. Clonar formularis
    print(f"\n📋 Clonant 18 formularis a {root_folder_name}...")
    cloned_records = []

    for item in FORMULARIS:
        orig_id = item["id"]
        sf_name = item["subfolder"]
        dest_folder_id = subfolders[sf_name]

        # Obtenir metadades originals
        orig_meta = drive_p.files().get(fileId=orig_id, fields="name").execute()
        title = orig_meta.get("name", f"{item['curs']} {item['materia']} {item['any']}")

        # Comprovar si ja existeix a la subcarpeta de destí
        q_check = f"name = '{title}' and trashed = false and '{dest_folder_id}' in parents"
        check_res = drive_p.files().list(q=q_check, fields="files(id, name)").execute()
        existing = check_res.get("files", [])

        if existing:
            new_id = existing[0]["id"]
            print(f"  ✓ Ja existent al personal: {title} (ID: {new_id})")
        else:
            # Fer la còpia des del compte personal (passa a ser de la seva propietat!)
            copy_body = {
                "name": title,
                "parents": [dest_folder_id],
            }
            new_file = drive_p.files().copy(fileId=orig_id, body=copy_body, fields="id, name").execute()
            new_id = new_file["id"]

            # Donar permisos públics de lectura
            drive_p.permissions().create(
                fileId=new_id,
                body={"role": "reader", "type": "anyone"}
            ).execute()
            print(f"  🎉 Copiat al personal: {title} (ID: {new_id})")

        cloned_records.append({
            "curs": item["curs"],
            "materia": item["materia"],
            "any": item["any"],
            "title": title,
            "orig_id": orig_id,
            "personal_id": new_id,
            "edit_url": f"https://docs.google.com/forms/d/{new_id}/edit",
            "responder_url": f"https://docs.google.com/forms/d/e/{new_id}/viewform",
        })

    # Guardar registre
    out_json = WS / "config" / "cb_formularis_personal.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "root_folder_id": root_id,
            "subfolders": subfolders,
            "forms": cloned_records,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Completat! Desat registre a {out_json}")
    print(f"Enllaç carpeta arrel personal: https://drive.google.com/drive/folders/{root_id}")


if __name__ == "__main__":
    main()
