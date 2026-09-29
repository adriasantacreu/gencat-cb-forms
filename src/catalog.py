"""BD de Competències Bàsiques (SQLite + FTS5): activitats (context) i ítems, amb l'esquema comú de PAU."""
import sqlite3
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
CB_DIR = WORKSPACE / "docencia/materials/competencies_basiques/cb_catalog"
DB_PATH = CB_DIR / "cb_catalog.db"
CROPS = CB_DIR / "crops"

SCHEMA = """
CREATE TABLE activitats (
    id TEXT PRIMARY KEY,          -- CB4ESO_MAT_2026_A1
    prova TEXT NOT NULL,          -- CB4ESO_MAT_2026
    numero INTEGER NOT NULL,
    titol TEXT,
    descripcio TEXT,
    context_img TEXT,             -- primera imatge de context (ruta relativa a cb_catalog/)
    context_text TEXT             -- OCR de tots els contextos de l'activitat
);
CREATE TABLE items (
    id TEXT PRIMARY KEY,          -- CB4ESO_MAT_2026_I7 · sub-pregunta: …_I6_1
    prova TEXT NOT NULL,
    etapa TEXT NOT NULL,          -- CB4ESO, CB2ESO
    materia TEXT NOT NULL,        -- mat, cte
    any INTEGER NOT NULL,
    convocatoria TEXT NOT NULL,   -- CB (4t) o AD (2n: avaluació de diagnòstic)
    activitat_id TEXT NOT NULL,
    numero INTEGER NOT NULL,
    sub TEXT,                     -- '1' a la pregunta 6.1
    pare TEXT,                    -- id de grup (…_I6) de les sub-preguntes
    tipus TEXT NOT NULL,          -- opcio | oberta
    punts REAL,
    bloc TEXT,
    tema TEXT,
    enunciat_text TEXT,           -- OCR de la captura de l'ítem (compartit entre sub-preguntes)
    solucio_text TEXT,            -- clau del registre («b» o «b. Sí»)
    resposta TEXT,
    enunciat_img TEXT,
    context_img TEXT,
    context_text TEXT,
    font_pdf TEXT
);
CREATE VIRTUAL TABLE items_fts USING fts5(
    id UNINDEXED, enunciat_text, solucio_text, context_text, titol, tema,
    tokenize = 'unicode61 remove_diacritics 2'
);
CREATE INDEX idx_it_prova ON items(prova);
CREATE INDEX idx_it_act ON items(activitat_id);
"""


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def reset(path: Path = DB_PATH) -> sqlite3.Connection:
    if path.exists():
        path.unlink()
    con = connect(path)
    con.executescript(SCHEMA)
    return con


def insert_fts(con: sqlite3.Connection, row: dict, titol: str) -> None:
    con.execute("INSERT INTO items_fts(id,enunciat_text,solucio_text,context_text,titol,tema) VALUES (?,?,?,?,?,?)",
                (row["id"], row["enunciat_text"], row["solucio_text"], row["context_text"], titol, row["tema"] or ""))
