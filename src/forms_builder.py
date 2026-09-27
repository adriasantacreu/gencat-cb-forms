"""Mòdul constructor de formularis a Google Forms API v1."""

from pathlib import Path
import time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    InstalledAppFlow = None

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
]


def get_google_services(credentials_path: Path = Path("credentials.json"), token_path: Path = Path("token.json")):
    """Obté els clients autenticats de Forms i Drive v3."""
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"Cal un fitxer de credencials OAuth de Google a: {credentials_path}\n"
                    "Descarrega'l des de Google Cloud Console (APIs & Services > Credentials)."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    forms_service = build("forms", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return forms_service, drive_service


def upload_image_to_drive(drive_service, file_path: Path, folder_id: str) -> str:
    """Puja una imatge a Google Drive i retorna el seu file ID amb lectura pública."""
    file_metadata = {
        "name": file_path.name,
        "parents": [folder_id],
    }
    media = MediaFileUpload(str(file_path), mimetype="image/png", resumable=True)
    f = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    file_id = f.get("id")

    # Permís de lectura pública perquè Forms la pugui descarregar
    drive_service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()

    return file_id


def build_google_form(
    forms_service,
    drive_service,
    title: str,
    description: str,
    structure: list,
    answers: dict,
    crops_dir: Path,
    drive_folder_id: str,
    assets_folder_id: str,
    editor_email: str = None,
) -> dict:
    """Crea el formulari, puja les imatges i construeix els ítems del test."""
    print(f"\n🚀 CREANT FORMULARI: {title}")

    # 1. Pujada d'imatges a Drive
    print("↓ Pujant captures a Google Drive...")
    crop_files = list(crops_dir.glob("*.png"))
    image_catalog = {}
    for cf in crop_files:
        fid = upload_image_to_drive(drive_service, cf, assets_folder_id)
        image_catalog[cf.stem] = fid
    print(f"✓ {len(image_catalog)} captures preparades a Drive.")

    # 2. Creació del formulari buit
    form_res = forms_service.forms().create(body={"info": {"title": title}}).execute()
    form_id = form_res["formId"]
    print(f"✓ Formulari creat (ID: {form_id})")

    # 3. Moure a la carpeta destí i configurar permisos
    if drive_folder_id:
        drive_service.files().update(
            fileId=form_id,
            addParents=drive_folder_id,
            fields="id, parents",
        ).execute()

    drive_service.permissions().create(
        fileId=form_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()

    if editor_email:
        drive_service.permissions().create(
            fileId=form_id,
            body={"role": "writer", "type": "user", "emailAddress": editor_email},
        ).execute()

    # 4. Construcció de peticions batchUpdate
    requests_list = [
        # Activar mode Quiz
        {
            "updateSettings": {
                "settings": {"quizSettings": {"isQuiz": True}},
                "updateMask": "quizSettings.isQuiz",
            }
        },
        # Descripció del formulari
        {
            "updateFormInfo": {
                "info": {"description": description},
                "updateMask": "description",
            }
        },
    ]

    item_idx = 0
    total_points = 0

    for elem in structure:
        etype = elem.get("type")

        if etype == "context":
            cid = elem.get("id")
            fid = image_catalog.get(cid)
            if fid:
                requests_list.append({
                    "createItem": {
                        "item": {
                            "title": elem.get("title", "Context"),
                            "description": elem.get("description", ""),
                            "imageItem": {
                                "image": {
                                    "sourceUri": f"https://drive.google.com/uc?export=download&id={fid}",
                                    "properties": {"alignment": "CENTER", "width": 650},
                                }
                            },
                        },
                        "location": {"index": item_idx},
                    }
                })
                item_idx += 1

        elif etype == "item":
            iid = elem.get("id")
            num = elem.get("num")
            points = elem.get("points", 1)
            total_points += points
            fid = image_catalog.get(iid)

            image_prop = {}
            if fid:
                image_prop = {
                    "image": {
                        "sourceUri": f"https://drive.google.com/uc?export=download&id={fid}",
                        "properties": {"alignment": "CENTER", "width": 650},
                    }
                }

            is_open = elem.get("is_open", False)
            if is_open:
                # Pregunta oberta de desenvolupament
                requests_list.append({
                    "createItem": {
                        "item": {
                            "title": f"Pregunta {num} (Desenvolupament - {points} punts)",
                            "description": "Escriu la teva justificació, passos o resultat.",
                            "questionItem": {
                                "question": {
                                    "required": False,
                                    "grading": {
                                        "pointValue": points,
                                        "generalFeedback": {
                                            "text": f"Rúbrica oficial de correcció:\n{elem.get('rubric', 'Consultar guia oficial.')}"
                                        },
                                    },
                                    "textQuestion": {"paragraph": True},
                                },
                                **(image_prop if fid else {}),
                            },
                        },
                        "location": {"index": item_idx},
                    }
                })
            else:
                # Pregunta tancada tipus test
                correct_letter = answers.get(num, "").lower()
                opt_labels = elem.get("opt_labels", ["a", "b", "c", "d"])

                options = []
                for opt in opt_labels:
                    is_correct = (opt.lower() == correct_letter)
                    options.append({"value": opt, "isCorrect": is_correct})

                requests_list.append({
                    "createItem": {
                        "item": {
                            "title": f"Pregunta {num}",
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "grading": {
                                        "pointValue": points,
                                        "correctAnswers": {"answers": [{"value": correct_letter}]},
                                    },
                                    "choiceQuestion": {
                                        "type": "RADIO",
                                        "options": options,
                                        "shuffle": False,
                                    },
                                },
                                **(image_prop if fid else {}),
                            },
                        },
                        "location": {"index": item_idx},
                    }
                })
            item_idx += 1

    # Enviament del batchUpdate
    print(f"↓ Enviant {len(requests_list)} peticions a Forms API...")
    forms_service.forms().batchUpdate(formId=form_id, body={"requests": requests_list}).execute()

    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    resp_url = form_res.get("responderUri", f"https://docs.google.com/forms/d/{form_id}/viewform")

    print(f"🎉 FORMULARI ENLLESTIT: {title}")
    print(f"• Puntuació: {total_points} punts")
    print(f"• Enllaç edició: {edit_url}")
    print(f"• Enllaç resposta: {resp_url}\n")

    return {
        "form_id": form_id,
        "edit_url": edit_url,
        "responder_url": resp_url,
        "points": total_points,
    }
