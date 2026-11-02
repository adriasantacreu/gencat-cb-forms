#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de formulari autocorregible pilot per a 4t d'ESO (Matemàtiques 2025).
Pulla captures d'alta resolució al Google Drive i genera el Google Form via API v1.
"""

import json
import time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants de carpetes Drive
FOLDER_IMAGES = "1e-aQDMb3auBx1dQYIU24n5cYJnKRVrUf"       # _Assets_Imatges
FOLDER_TARGET = "1lLddb6TLWxYwKHfZWSHfgy206oOnVBzg"       # 01_4ESO_Matematiques

# Clau de respostes oficial de 4ESO 2025
ANSWERS_2025 = {
    1: 'a', 2: 'b', 3: 'c', 4: 'b', 5: 'c', 6: 'a', 7: 'd', 8: 'd',
    9: 'c', 10: 'b', 11: 'c', 12: 'c', 13: 'a', 14: 'd', 15: 'a', 16: 'c', 17: 'c', 18: 'd',
    19: 'b', 20: 'd', 21: 'c',
    22: 'd', 23: 'b', 24: 'd', 25: 'b', 26: 'c', 27: 'a', 28: 'a',
    29: 'a', 30: 'c', 31: 'b', 32: 'd', 33: 'a'
}

def get_services():
    creds_path = "/home/ubuntu/.google_workspace_mcp/institut/adria.santacreu@iesantpol.cat.json"
    with open(creds_path) as f:
        d = json.load(f)
    creds = Credentials(
        d["token"],
        refresh_token=d["refresh_token"],
        token_uri=d["token_uri"],
        client_id=d["client_id"],
        client_secret=d["client_secret"],
        scopes=d["scopes"]
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    forms = build("forms", "v1", credentials=creds, cache_discovery=False)
    return drive, forms

def upload_image(drive, local_path, filename):
    media = MediaFileUpload(str(local_path), mimetype="image/png")
    # Comprovar si ja existeix
    q = f"'{FOLDER_IMAGES}' in parents and name='{filename}' and trashed=false"
    res = drive.files().list(q=q, fields="files(id)").execute().get("files", [])
    if res:
        file_id = res[0]["id"]
    else:
        file_meta = {"name": filename, "parents": [FOLDER_IMAGES]}
        f = drive.files().create(body=file_meta, media_body=media, fields="id").execute()
        file_id = f["id"]
        # Permís públic
        drive.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()
    
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def upload_pdf_if_needed(drive):
    pdf_path = Path("docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2025_prova.pdf")
    q = f"'{FOLDER_TARGET}' in parents and name='4ESO_CB_2025_prova.pdf' and trashed=false"
    res = drive.files().list(q=q, fields="files(id,webViewLink)").execute().get("files", [])
    if res:
        return res[0]["webViewLink"]
    media = MediaFileUpload(str(pdf_path), mimetype="application/pdf")
    meta = {"name": "4ESO_CB_2025_prova.pdf", "parents": [FOLDER_TARGET]}
    f = drive.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
    drive.permissions().create(fileId=f["id"], body={"role": "reader", "type": "anyone"}).execute()
    return f["webViewLink"]

def main():
    drive, forms = get_services()
    print("✓ Connexió amb Google Drive i Forms establerta.")

    pdf_link = upload_pdf_if_needed(drive)
    print(f"✓ PDF oficial al Drive: {pdf_link}")

    crops_dir = Path("scratch/crops_4eso_2025_v2")
    images_urls = {}

    print("↓ Pujant captures a Google Drive (_Assets_Imatges)...")
    for img_path in sorted(crops_dir.glob("*.png")):
        fn = f"4eso_2025_{img_path.name}"
        url = upload_image(drive, img_path, fn)
        images_urls[img_path.name] = url
    print(f"✓ {len(images_urls)} imatges disponibles amb enllaç directe.")

    # Crear Formulari
    title = "4t d’ESO · Competència matemàtica 2025 · Prova oficial CB"
    desc = (
        "Avaluació de final d’etapa — Competència matemàtica (Curs 2024-2025)\n"
        "Institut Escola Sant Pol de Mar\n\n"
        "Prova oficial autocorregible de 33 preguntes (1 punt per ítem, total 33 punts).\n"
        f"Podeu consultar el quadern complet oficial en PDF aquí: {pdf_link}"
    )

    form_body = {
        "info": {
            "title": title,
            "documentTitle": "4ESO-MAT_CB-2025_prova-autocorregible"
        }
    }
    created_form = forms.forms().create(body=form_body).execute()
    form_id = created_form["formId"]
    print(f"✓ Formulari buit creat: {form_id}")

    # Moure el formulari a la carpeta de destinació
    drive.files().update(
        fileId=form_id,
        addParents=FOLDER_TARGET,
        removeParents="root",
        fields="id,parents"
    ).execute()
    print(f"✓ Formulari mogut a la carpeta 01_4ESO_Matematiques.")

    # Construir els requests de batchUpdate
    requests = [
        # 1. Update settings: Quiz mode
        {
            "updateSettings": {
                "settings": {
                    "quizSettings": {
                        "isQuiz": True
                    }
                },
                "updateMask": "quizSettings.isQuiz"
            }
        },
        # 2. Update description
        {
            "updateFormInfo": {
                "info": {
                    "description": desc
                },
                "updateMask": "description"
            }
        }
    ]

    # Estructura del formulari per activitats
    elements = [
        # Secció 1
        {"kind": "section", "title": "Activitat 1. El medicament", "desc": "Ítems de l'1 al 8. Situació inicial: febre d'en Mario i tractament mèdic."},
        {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: registre de temperatura"},
        {"kind": "item", "num": 1},
        {"kind": "item", "num": 2},
        {"kind": "item", "num": 3},
        {"kind": "item", "num": 4},
        {"kind": "image", "file": "context_act1_formula.png", "title": "Context per als ítems 5, 6 i 7: dosi diària del xarop"},
        {"kind": "item", "num": 5},
        {"kind": "item", "num": 6},
        {"kind": "item", "num": 7},
        {"kind": "item", "num": 8},

        # Secció 2
        {"kind": "section", "title": "Activitat 2. La reforma del mercat", "desc": "Ítems del 9 al 18. Situació: obres de millora, accessibilitat, logotip i enquesta."},
        {"kind": "image", "file": "context_act2_intro.png", "title": "Context: accessos (escala i rampa)"},
        {"kind": "item", "num": 9},
        {"kind": "item", "num": 10},
        {"kind": "item", "num": 11},
        {"kind": "item", "num": 12},
        {"kind": "item", "num": 13},
        {"kind": "item", "num": 14},
        {"kind": "image", "file": "context_act2_enquesta.png", "title": "Context per als ítems 15, 16 i 17: enquesta d'usuaris del mercat"},
        {"kind": "item", "num": 15},
        {"kind": "item", "num": 16},
        {"kind": "item", "num": 17},
        {"kind": "item", "num": 18},

        # Secció 3
        {"kind": "section", "title": "Activitat 3. Un joc de cartes", "desc": "Ítems del 19 al 21. Situació: joc d'estratègia amb baralla de 36 cartes."},
        {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: regles de la baralla"},
        {"kind": "item", "num": 19},
        {"kind": "item", "num": 20},
        {"kind": "item", "num": 21},

        # Secció 4
        {"kind": "section", "title": "Activitat 4. Lloguer de para-sols", "desc": "Ítems del 22 al 28. Situació: empresa de platja, tarifes, geometria i ombres."},
        {"kind": "image", "file": "context_act4_intro.png", "title": "Context: tarifes de lloguer"},
        {"kind": "item", "num": 22},
        {"kind": "item", "num": 23},
        {"kind": "item", "num": 24},
        {"kind": "item", "num": 25},
        {"kind": "image", "file": "context_act4_octogon.png", "title": "Context per als ítems 26 i 27: geometria del para-sol"},
        {"kind": "item", "num": 26},
        {"kind": "item", "num": 27},
        {"kind": "item", "num": 28},

        # Secció 5
        {"kind": "section", "title": "Activitat 5. El viatge de 4t d’ESO", "desc": "Ítems del 29 al 33. Situació: organització, votacions i finançament del viatge."},
        {"kind": "image", "file": "context_act5_intro.png", "title": "Context: votació de destinació"},
        {"kind": "item", "num": 29},
        {"kind": "item", "num": 30},
        {"kind": "image", "file": "context_act5_paperetes.png", "title": "Context per als ítems 31 i 32: rifa i venda de paperetes"},
        {"kind": "item", "num": 31},
        {"kind": "item", "num": 32},
        {"kind": "item", "num": 33},
    ]

    item_index = 0
    for el in elements:
        if el["kind"] == "section":
            # Si és el primer element, no cal afegir pageBreak (ja és la primera pàgina)
            if item_index > 0:
                requests.append({
                    "createItem": {
                        "item": {
                            "title": el["title"],
                            "description": el["desc"],
                            "pageBreakItem": {}
                        },
                        "location": {"index": item_index}
                    }
                })
                item_index += 1
        elif el["kind"] == "image":
            img_url = images_urls.get(el["file"])
            if img_url:
                requests.append({
                    "createItem": {
                        "item": {
                            "title": el["title"],
                            "imageItem": {
                                "image": {
                                    "sourceUri": img_url,
                                    "properties": {"alignment": "CENTER"}
                                }
                            }
                        },
                        "location": {"index": item_index}
                    }
                })
                item_index += 1
        elif el["kind"] == "item":
            num = el["num"]
            correct_key = ANSWERS_2025[num]
            img_file = f"item_{num}.png"
            img_url = images_urls.get(img_file)
            
            question_dict = {
                "required": True,
                "grading": {
                    "pointValue": 1,
                    "correctAnswers": {"answers": [{"value": correct_key}]}
                },
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [
                        {"value": "a"},
                        {"value": "b"},
                        {"value": "c"},
                        {"value": "d"}
                    ],
                    "shuffle": False
                }
            }

            item_dict = {
                "title": f"Pregunta {num}",
                "questionItem": {
                    "question": question_dict
                }
            }
            if img_url:
                item_dict["questionItem"]["image"] = {
                    "sourceUri": img_url,
                    "properties": {"alignment": "CENTER"}
                }

            requests.append({
                "createItem": {
                    "item": item_dict,
                    "location": {"index": item_index}
                }
            })
            item_index += 1

    print(f"↓ Enviant {len(requests)} peticions de creació a Forms API...")
    # Executem en blocs si cal o d'un sol cop
    # Google Forms API suporta fins a ~100 requests per crida
    res = forms.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    print("✓ Formulari actualitzat amb èxit!")

    # Recuperem els enllaços finals
    form_info = forms.forms().get(formId=form_id).execute()
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    responder_url = form_info.get("responderUri", f"https://docs.google.com/forms/d/e/{form_id}/viewform")

    print("\n" + "="*60)
    print("🎉 FORMULARI PILOT CREAT I CONFIGURAT CORRECTAMENT!")
    print("="*60)
    print(f"• Títol: {title}")
    print(f"• Puntuació total: 33 punts (33 ítems x 1 punt)")
    print(f"• Enllaç d'edició (professor): {edit_url}")
    print(f"• Enllaç de resposta (alumnes): {responder_url}")
    print("="*60)

if __name__ == "__main__":
    main()
