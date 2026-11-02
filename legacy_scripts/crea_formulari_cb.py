#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador modular de formularis Google Forms autocorregibles per a Competències Bàsiques i Avaluacions Diagnòstiques.
Crea el formulari via API Forms v1, allotja imatges a Google Drive amb permisos públics i configura l'avaluació (Quiz).
"""

import sys
import json
import time
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Carpetes de destí a Google Drive
DRIVE_FOLDERS = {
    "IMAGES": "1e-aQDMb3auBx1dQYIU24n5cYJnKRVrUf",           # _Assets_Imatges
    "4ESO_MAT": "1lLddb6TLWxYwKHfZWSHfgy206oOnVBzg",         # 01_4ESO_Matematiques
    "4ESO_CTE": "1n5qtJOrWNiH0pJr0-xbVMngDEGZBTa5L",         # 02_4ESO_Ciencia_Tecnologia
    "2ESO_MAT": "1wUKJFi0MUTTpXjaImvETLvQnEGMsOMRl",         # 03_2ESO_Matematiques
    "2ESO_CTE": "1Ggi78ZJtaXgxvWB9rMM9eQy8bFUk_seX",         # 04_2ESO_Ciencia_Tecnologia
}

PERSONAL_EMAIL = "adriasantacreu@gmail.com"

# Claus de correcció oficials 100% verificades de les pautes del Departament
ANSWERS = {
    ("4ESO", "MAT", 2026): {
        1: 'c', 2: 'c', 3: 'd', 4: 'c', 5: 'a', 6: 'd', 7: 'a', 8: 'b',
        9: 'a', 10: 'd', 11: 'b', 12: 'c', 13: 'd',
        14: 'a', 15: 'c', 16: 'a', 17: 'c', 18: 'b', 19: 'a', 20: 'a', 21: 'd',
        22: 'c', 23: 'b', 24: 'b', 25: 'b', 26: 'a', 27: 'd', 28: 'c', 29: 'd', 30: 'a', 31: 'b', 32: 'b'
    },
    ("4ESO", "MAT", 2025): {
        1: 'a', 2: 'b', 3: 'c', 4: 'b', 5: 'c', 6: 'a', 7: 'd', 8: 'd',
        9: 'c', 10: 'b', 11: 'c', 12: 'c', 13: 'a', 14: 'd', 15: 'a', 16: 'c', 17: 'c', 18: 'd',
        19: 'b', 20: 'd', 21: 'c',
        22: 'd', 23: 'b', 24: 'd', 25: 'b', 26: 'c', 27: 'a', 28: 'a',
        29: 'a', 30: 'c', 31: 'b', 32: 'd', 33: 'a'
    },
    ("4ESO", "MAT", 2024): {
        1: 'd', 2: 'c', 3: 'c', 4: 'b', 5: 'd', 6: 'd', 7: 'a', 8: 'c',
        9: 'd', 10: 'c', 11: 'c', 12: 'b', 13: 'b', 14: 'a', 15: 'b',
        16: 'b', 17: 'd', 18: 'a', 19: 'b', 20: 'b',
        21: 'd', 22: 'c', 23: 'd', 24: 'c', 25: 'a', 26: 'b', 27: 'a',
        28: 'c', 29: 'a', 30: 'b', 31: 'a', 32: 'c'
    },
    ("2ESO", "MAT", 2026): {
        1: 'c', 2: 'd', 3: 'a', 4: 'c', 5: 'c', 6: 'a', 7: 'c', 8: 'b', 9: 'b', 10: 'd',
        11: 'a', "12_1": 'Verdadera', "12_2": 'Falsa', 13: 'b', 14: 'c', 15: 'a', 16: 'd', 17: 'b',
        18: 'b', 19: 'd', 20: 'd', 21: 'b', 22: 'd', 23: 'c', 24: 'c', 25: 'a', 26: 'a',
        27: 'a', 28: 'd', 29: 'c', 30: 'b'
    },
    ("2ESO", "MAT", 2025): {
        1: 'd', 2: 'b', 3: 'c', 4: 'd', 6: 'b', 7: 'a',
        10: 'c', 12: 'a', 14: 'c', 15: 'd',
        17: 'd', 19: 'a', 21: 'd', 22: 'c', 23: 'a', 24: 'b', 25: 'd',
        26: 'a', 27: 'c', 28: 'b', 29: 'd', 30: 'c'
    },
    ("2ESO", "MAT", 2024): {
        1: 'a', 2: 'd', 4: 'c',
        7: 'b', 8: 'c', 9: 'a', 10: 'a', 11: 'c', 12: 'b',
        13: 'a', 15: 'd', 18: 'd', 19: 'c',
        20: 'b', 21: 'b', 22: 'c'
    },
    ("4ESO", "CTE", 2026): {
        1: 'a',
        "2_1": 'Avantatge', "2_2": 'Inconvenient', "2_3": 'Inconvenient', "2_4": 'Avantatge',
        3: 'c',
        "4_1": 'Passiu', "4_2": 'Actiu', "4_3": 'Actiu', "4_4": 'Passiu',
        5: 'b', 6: 'd', 7: 'a',
        8: 'a', 9: 'a', 10: 'a', 11: 'd', 12: 'a', 13: 'd', 14: 'd', 15: 'd', 16: 'c', 17: 'd',
        "18_1": 'D', "18_2": 'A', "18_3": 'C', "18_4": 'B',
        19: 'c', 20: 'c', 21: 'b', 22: 'b',
        "23_1": 'Positiu', "23_2": 'Negatiu', "23_3": 'Negatiu', "23_4": 'Positiu',
        "24_1": 'SÍ', "24_2": 'NO', "24_3": 'SÍ', "24_4": 'NO',
        25: 'b'
    },
    ("4ESO", "CTE", 2025): {
        1: 'b', 2: 'd', 3: 'a', 4: 'b',
        "5_1": 'B', "5_2": 'C', "5_3": 'D', "5_4": 'A',
        6: 'c', 7: 'b',
        8: 'b',
        "9_1": 'C', "9_2": 'A', "9_3": 'B', "9_4": 'D',
        10: 'd', 11: 'd', 12: 'c',
        "13_1": 'SÍ', "13_2": 'SÍ', "13_3": 'SÍ', "13_4": 'NO',
        14: 'c',
        15: 'b', 16: 'a', 17: 'd', 18: 'd',
        "19_1": 'SÍ', "19_2": 'NO', "19_3": 'SÍ', "19_4": 'NO',
        20: 'a', 21: 'b', 22: 'd',
        "23_1": 'SÍ', "23_2": 'SÍ', "23_3": 'NO', "23_4": 'NO',
        24: 'c', 25: 'a'
    },
    ("4ESO", "CTE", 2024): {
        1: 'c', 2: 'b', 3: 'a',
        "4_1": 'SÍ', "4_2": 'NO', "4_3": 'NO', "4_4": 'SÍ',
        5: 'b', 6: 'd',
        "7_1": 'V', "7_2": 'V', "7_3": 'F', "7_4": 'F',
        8: 'c',
        "9_1": 'F', "9_2": 'V', "9_3": 'F', "9_4": 'V',
        10: 'a', 11: 'c', 12: 'a', 13: 'd',
        14: 'd', 15: 'c', 16: 'c', 17: 'b', 18: 'c',
        "19_1": 'Conseqüència', "19_2": 'Conseqüència', "19_3": 'Causa', "19_4": 'Causa',
        "20_1": 'C', "20_2": 'A', "20_3": 'D', "20_4": 'B',
        "21_1": 'F', "21_2": 'V', "21_3": 'F', "21_4": 'V',
        22: 'a',
        "23_1": 'F', "23_2": 'F', "23_3": 'V', "23_4": 'V',
        24: 'c',
        "25_1": 'D', "25_2": 'A', "25_3": 'C', "25_4": 'B'
    },
    ("2ESO", "CTE", 2026): {
        1: 'c', 2: 'c', 3: 'c', 4: 'a',
        "5_1": 'E', "5_2": 'A', "5_3": 'B', "5_4": 'D',
        6: 'b', 7: 'b',
        "8_1": 'B', "8_2": 'C', "8_3": 'A', "8_4": 'E',
        9: 'd',
        "10_1": 'D', "10_2": 'B', "10_3": 'E', "10_4": 'A',
        11: 'a', 12: 'd', 13: 'c',
        "14_1": 'E', "14_2": 'C', "14_3": 'A', "14_4": 'D',
        15: 'd', 16: 'b', 17: 'a',
        "18_1": 'NO', "18_2": 'NO', "18_3": 'SÍ', "18_4": 'SÍ',
        "19_1": 'SÍ', "19_2": 'NO', "19_3": 'SÍ', "19_4": 'NO',
        20: 'b', 21: 'b', 22: 'a', 23: 'a', 24: 'b', 25: 'c'
    },
    ("2ESO", "CTE", 2025): {
        1: 'a', 2: 'b', 3: 'a', 4: 'b',
        "5_1": 'D', "5_2": 'A', "5_3": 'C', "5_4": 'B',
        "6_1": 'C', "6_2": 'A', "6_3": 'B', "6_4": 'D',
        9: 'c',
        "10_1": 'SÍ', "10_2": 'SÍ', "10_3": 'SÍ', "10_4": 'NO',
        "12_1": 'C', "12_2": 'D', "12_3": 'B', "12_4": 'A',
        13: 'a', 14: 'd', 15: 'd', 16: 'b', 17: 'a',
        19: 'b', 20: 'b',
        "21_1": 'SÍ', "21_2": 'NO', "21_3": 'NO', "21_4": 'SÍ',
        "22_1": 'B', "22_2": 'C', "22_3": 'D', "22_4": 'A',
        23: 'd', 24: 'c',
        "25_1": 'NO', "25_2": 'NO', "25_3": 'SÍ', "25_4": 'SÍ'
    },
    ("2ESO", "CTE", 2024): {
        "1_1": 'F', "1_2": 'V', "1_3": 'F',
        "2_1": 'F', "2_2": 'V', "2_3": 'V',
        "3_1": 'B', "3_2": 'A', "3_3": 'C',
        "4_1": 'SÍ', "4_2": 'NO', "4_3": 'NO',
        "7_1": 'C', "7_2": 'A', "7_3": 'B',
        8: 'b', 11: 'c',
        "12_1": '1', "12_2": '3', "12_3": '2',
        13: 'd', 14: 'd', 15: 'c', 16: 'a',
        "17_1": 'NO', "17_2": 'SÍ', "17_3": 'SÍ',
        18: 'c',
        19: 'b', 20: 'c', 21: 'b', 22: 'b', 23: 'c'
    }
}

# Estructures de formularis per activitat i contingut
STRUCTURES = {
    ("4ESO", "MAT", 2026): {
        "title": "4t d’ESO · Competència matemàtica 2026 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2026_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2025-2026)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 32 preguntes (1 punt per ítem, total 32 punts).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2026_prova.pdf",
        "crops_dir": "scratch/crops_4eso_2026_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. L'ascensor", "desc": "Ítems de l'1 al 8. Situació: funcionament de l'ascensor, càrrega màxima, velocitat i escales."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: característiques de l’ascensor"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "context_act1_temps.png", "title": "Context per als ítems 5 i 6: velocitat i aturades"},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "image", "file": "context_act1_escales.png", "title": "Context per als ítems 7 i 8: trams d’escala i esglaons"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},

            {"kind": "section", "title": "Activitat 2. Els paquets de llaunes", "desc": "Ítems del 9 al 13. Situació: envasat de llaunes amb anelles de cartró i sèries geomètriques."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: anelles de cartró i simetria"},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "image", "file": "context_act2_serie.png", "title": "Context per als ítems 11, 12 i 13: sèrie de figures"},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},

            {"kind": "section", "title": "Activitat 3. L'hotel", "desc": "Ítems del 14 al 21. Situació: ocupació de places, ingressos setmanals, habitacions i piscines tèrmiques."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context: ocupació de places i ingressos"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "item", "num": 18},
            {"kind": "image", "file": "context_act3_temp.png", "title": "Context per als ítems 19, 20 i 21: temperatures Celsius i Fahrenheit"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},

            {"kind": "section", "title": "Activitat 4. Botons", "desc": "Ítems del 22 al 32. Situació: fabricació, mides, combinatòria, tints de colors i control de qualitat."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context: colors de botons per al jersei"},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "image", "file": "context_act4_barra.png", "title": "Context per als ítems 24 i 25: barra cilíndrica de polièster"},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25},
            {"kind": "item", "num": 26},
            {"kind": "image", "file": "context_act4_tints.png", "title": "Context per als ítems 27 i 28: mescla de tints"},
            {"kind": "item", "num": 27},
            {"kind": "item", "num": 28},
            {"kind": "item", "num": 29},
            {"kind": "image", "file": "context_act4_control.png", "title": "Context per als ítems 30, 31 i 32: control de qualitat i defectes"},
            {"kind": "item", "num": 30},
            {"kind": "item", "num": 31},
            {"kind": "item", "num": 32},
        ]
    },
    ("4ESO", "MAT", 2025): {
        "title": "4t d’ESO · Competència matemàtica 2025 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2025_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2024-2025)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 33 preguntes (1 punt per ítem, total 33 punts).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2025_prova.pdf",
        "crops_dir": "scratch/crops_4eso_2025_clean",
        "elements": [
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

            {"kind": "section", "title": "Activitat 3. Un joc de cartes", "desc": "Ítems del 19 al 21. Situació: joc d'estratègia amb baralla de 36 cartes."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: regles de la baralla"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},

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

            {"kind": "section", "title": "Activitat 5. El viatge de 4t d’ESO", "desc": "Ítems del 29 al 33. Situació: organització, votacions i finançament del viatge."},
            {"kind": "image", "file": "context_act5_intro.png", "title": "Context: votació de destinació"},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
            {"kind": "image", "file": "context_act5_paperetes.png", "title": "Context per als ítems 31 i 32: rifa i venda de paperetes"},
            {"kind": "item", "num": 31},
            {"kind": "item", "num": 32},
            {"kind": "item", "num": 33},
        ]
    },
    ("4ESO", "MAT", 2024): {
        "title": "4t d’ESO · Competència matemàtica 2024 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2024_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2023-2024)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 32 preguntes (1 punt per ítem, total 32 punts).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2024_prova.pdf",
        "crops_dir": "scratch/crops_4eso_2024_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Venda per internet", "desc": "Ítems de l'1 al 8. Situació: botiga de roba per internet, vendes mensuals, estalvi i valoracions de clients."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: vendes mensuals de roba"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "context_act1_valoracions.png", "title": "Context per als ítems 5, 6, 7 i 8: valoracions de satisfacció"},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},

            {"kind": "section", "title": "Activitat 2. Els cornets de gelat", "desc": "Ítems del 9 al 15. Situació: combinatòria de gustos, cons de galeta, volums i cons de paper."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: capsa de cornets de gelat"},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "image", "file": "context_act2_cons.png", "title": "Context per als ítems 13, 14 i 15: mides i volums de cons"},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},

            {"kind": "section", "title": "Activitat 3. Plegant paper", "desc": "Ítems del 16 al 20. Situació: papiroflèxia, àrees de figures geomètriques, sèries i mosaic mural."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: plecs sobre paper quadrat"},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "image", "file": "context_act3_serie.png", "title": "Context per als ítems 18 i 19: sèrie de figures"},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},

            {"kind": "section", "title": "Activitat 4. Gimnàs i abonaments", "desc": "Ítems del 21 al 27. Situació: tarifes d'abonament, models lineals, màquina de córrer i desnivells."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context: tarifes del gimnàs"},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "context_act4_tarifes_rep.png", "title": "Context per als ítems 23 i 24: taula de tarifes"},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "image", "file": "context_act4_correr.png", "title": "Context per als ítems 25, 26 i 27: gràfics de córrer i desnivell"},
            {"kind": "item", "num": 25},
            {"kind": "item", "num": 26},
            {"kind": "item", "num": 27},

            {"kind": "section", "title": "Activitat 5. Làmpada octaèdrica", "desc": "Ítems del 28 al 32. Situació: políedres regulars, desenvolupament pla, arestes i models de llum."},
            {"kind": "image", "file": "context_act5_intro.png", "title": "Context inicial: octàedre regular de pergamí"},
            {"kind": "item", "num": 28},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
            {"kind": "image", "file": "context_act5_models.png", "title": "Context per als ítems 31 i 32: models de paper retallat"},
            {"kind": "item", "num": 31},
            {"kind": "item", "num": 32},
        ]
    },
    ("2ESO", "MAT", 2026): {
        "title": "2n d’ESO · Competència matemàtica 2026 · Avaluació diagnòstica",
        "docTitle": "2ESO-MAT_AD-2026_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Competència matemàtica (Curs 2025-2026)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 31 preguntes (1 punt per ítem, total 31 punts).",
        "target_folder": "2ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/matematiques/2ESO_AD_2026_prova.pdf",
        "crops_dir": "scratch/crops_2eso_2026_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. La festa d’aniversari", "desc": "Ítems de l'1 al 10. Situació: regals, compra de berenar, pastís al forn i despeses compartides."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: regals per a la festa d’aniversari"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "image", "file": "context_act1_pica_pica.png", "title": "Context per als ítems 3 i 4: compra d’olives i patates"},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "context_act1_pastis.png", "title": "Context per als ítems 5 i 6: recepta del pastís"},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "image", "file": "context_act1_forn.png", "title": "Context per als ítems 7 i 8: escalfament del forn"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "image", "file": "context_act1_despeses.png", "title": "Context per a l'ítem 10: despeses compartides"},
            {"kind": "item", "num": 10},

            {"kind": "section", "title": "Activitat 2. Rajoles quadrades", "desc": "Ítems de l'11 al 17. Situació: rajoles cartabó i llises, sèries, girs i simetries."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: tipus de rajoles (cartabó i llises)"},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": "12_1", "label": "Pregunta 12.1", "options": ["Verdadera", "Falsa"]},
            {"kind": "item", "num": "12_2", "label": "Pregunta 12.2", "options": ["Verdadera", "Falsa"]},
            {"kind": "image", "file": "context_act2_serie.png", "title": "Context per als ítems 13, 14 i 15: sèrie de figures"},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "image", "file": "context_act2_moviments.png", "title": "Context per a l'ítem 16: girs i simetries"},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},

            {"kind": "section", "title": "Activitat 3. La bicicletada popular", "desc": "Ítems del 18 al 26. Situació: socis del club ciclista, taules d'inscrits, mapes de rutes i velocitats."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: participants i socis del club"},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "context_act3_mapa.png", "title": "Context per als ítems 23 i 24: mapa de les rutes"},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "image", "file": "context_act3_velocitats.png", "title": "Context per als ítems 25 i 26: velocitats en pla, pujada i baixada"},
            {"kind": "item", "num": 25},
            {"kind": "item", "num": 26},

            {"kind": "section", "title": "Activitat 4. Recollim l’aigua de la pluja", "desc": "Ítems del 27 al 30. Situació: recollida d'aigua pluvial a l'institut, canalització, mitjana de pluja i hort escolar."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: recollida d’aigua a l’institut"},
            {"kind": "item", "num": 27},
            {"kind": "item", "num": 28},
            {"kind": "image", "file": "context_act4_pluja.png", "title": "Context per als ítems 29 i 30: dades de pluja d’abril"},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
        ]
    },
    ("2ESO", "MAT", 2025): {
        "title": "2n d’ESO · Competència matemàtica 2025 · Avaluació diagnòstica",
        "docTitle": "2ESO-MAT_AD-2025_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Competència matemàtica (Curs 2024-2025)\nInstitut Escola Sant Pol de Mar\n\nProva oficial combinada: preguntes tancades autocorregibles (PART 1) i preguntes de desenvolupament de resposta oberta (PART 2). Total 31 punts.",
        "target_folder": "2ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/matematiques/2ESO_AD_2025_prova.pdf",
        "crops_dir": "scratch/crops_2eso_2025_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. El projecte del pati", "desc": "Ítems de l'1 al 8. Situació: votació dels projectes de transformació del pati, espais, mides i taules de ping-pong."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: projectes A i B i resultats de votacions per curs"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "open_item", "num": 5, "label": "Pregunta 5 (Resposta oberta - PART 2)", "desc": "Completa la taula i el gràfic de barres seguint els passos descrits a la imatge."},
            {"kind": "image", "file": "context_act1_espai.png", "title": "Context per als ítems 6 i 7: plànol i mides de l'espai del pati"},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},
            {"kind": "image", "file": "context_act1_taules.png", "title": "Context per a l'ítem 8: taules de ping-pong i taulell d'escacs"},
            {"kind": "open_item", "num": 8, "label": "Pregunta 8 (Resposta oberta - PART 2)", "desc": "Descriu la situació i distribució a escala de les dues taules de ping-pong i el taulell d'escacs sobre el plànol."},

            {"kind": "section", "title": "Activitat 2. El joc de la diana", "desc": "Ítems del 9 al 16. Situació: llançament de dards, diana amb nombres enters positius i negatius, probabilitats i partides."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: sectors de la diana, doble puntuació central i exemples"},
            {"kind": "open_item", "num": 9, "label": "Pregunta 9 (Resposta oberta - PART 2)", "desc": "Escriu pas a pas les operacions que has fet per obtenir la puntuació dels llançaments de l'Èrica."},
            {"kind": "item", "num": 10},
            {"kind": "open_item", "num": "11_1", "img_file": "item_11_1.png", "label": "Pregunta 11.1 (Resposta oberta - PART 2)", "desc": "Indica si l'afirmació 1 és Verdadera o Falsa i explica detalladament els teus raonaments."},
            {"kind": "open_item", "num": "11_2", "img_file": "item_11_2.png", "label": "Pregunta 11.2 (Resposta oberta - PART 2)", "desc": "Indica si l'afirmació 2 és Verdadera o Falsa i explica detalladament els teus raonaments."},
            {"kind": "image", "file": "context_act2_formes10.png", "title": "Context: maneres d'obtenir puntuacions llançant tres dards"},
            {"kind": "item", "num": 12},
            {"kind": "open_item", "num": 13, "label": "Pregunta 13 (Resposta oberta - PART 2)", "desc": "Troba quatre maneres diferents d'aconseguir 15 punts llançant tres dards a la diana."},
            {"kind": "image", "file": "context_act2_partides.png", "title": "Context per als ítems 14, 15 i 16: partides entre en Leo i en Nil"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "open_item", "num": 16, "label": "Pregunta 16 (Resposta oberta - PART 2)", "desc": "Tria un dels dos nois (en Leo o en Nil) i justifica qui ho ha fet millor amb els teus càlculs i raonaments."},

            {"kind": "section", "title": "Activitat 3. Programem un robot", "desc": "Ítems del 17 al 25. Situació: ordres de moviment en graella, instrucció REPETEIX(M), consum de bateria i gràfics temporals."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: ordres del robot (AVANÇA, GIRA_DRETA, GIRA_ESQUERRA)"},
            {"kind": "item", "num": 17},
            {"kind": "open_item", "num": 18, "label": "Pregunta 18 (Resposta oberta - PART 2)", "desc": "Escriu el programa amb el mínim d'ordres possibles perquè el robot passi per totes les caselles marcades."},
            {"kind": "image", "file": "context_act3_repeteix.png", "title": "Context: funcionament de la instrucció REPETEIX(M)"},
            {"kind": "item", "num": 19},
            {"kind": "open_item", "num": 20, "label": "Pregunta 20 (Resposta oberta - PART 2)", "desc": "Escriu un programa utilitzant REPETEIX(3) perquè el robot passi per totes les caselles de la graella."},
            {"kind": "image", "file": "context_act3_consum.png", "title": "Context per als ítems 21 i 22: consum de bateria en unitats de càrrega (UC)"},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "context_act3_grafic.png", "title": "Context per als ítems 23, 24 i 25: gràfic temporal de descàrrega de bateria"},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25},

            {"kind": "section", "title": "Activitat 4. Capses de cartró", "desc": "Ítems del 26 al 30. Situació: desenvolupament pla de capses cúbiques, volum, probabilitat, combinatòria i recompte tridimensional."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: capses cúbiques amb tapa per a joguines"},
            {"kind": "item", "num": 26},
            {"kind": "item", "num": 27},
            {"kind": "item", "num": 28},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30}
        ]
    },
    ("2ESO", "MAT", 2024): {
        "title": "2n d’ESO · Competència matemàtica 2024 · Avaluació diagnòstica",
        "docTitle": "2ESO-MAT_AD-2024_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Competència matemàtica (Curs 2023-2024)\nInstitut Escola Sant Pol de Mar\n\nProva oficial combinada: preguntes tancades autocorregibles (PART 1) i preguntes de desenvolupament de resposta oberta (PART 2). Total 24 punts.",
        "target_folder": "2ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/matematiques/2ESO_AD_2024_prova.pdf",
        "crops_dir": "scratch/crops_2eso_2024_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Com anem a l'institut / L'aparcament de l'institut", "desc": "Ítems de l'1 al 6. Situació: mobilitat, enquesta a l'alumnat, mitjans de transport i ampliació de l'aparcament de bicis i patinets."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: enquesta sobre hàbits de mobilitat i gràfic d'alumnat per curs"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "open_item", "num": 3, "label": "Pregunta 3 (Resposta oberta - PART 2)", "desc": "Escriu els càlculs i explica els raonaments per determinar si s'ha aconseguit l'objectiu en cadascun dels cursos."},
            {"kind": "image", "file": "context_act1_transports.png", "title": "Context: gràfics de mitjans de transport i temps si anessin caminant"},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "context_act1_transports_rep.png", "title": "Context: dades dels gràfics per a les afirmacions 1 i 2"},
            {"kind": "open_item", "num": 5, "label": "Pregunta 5 (Resposta oberta - PART 2)", "desc": "Digues si cadascuna de les dues afirmacions és vertadera o falsa i explica els teus raonaments."},
            {"kind": "image", "file": "context_act1_ampliacio.png", "title": "Context per a l'ítem 6: dades d'ampliació de l'aparcament"},
            {"kind": "open_item", "num": "6_1", "img_file": "item_6_1.png", "label": "Pregunta 6.1 (Resposta oberta - PART 2)", "desc": "Calcula quantes bicis i patinets han de cabre a l'aparcament ampliat explicant els teus càlculs i raonaments."},
            {"kind": "open_item", "num": "6_2", "img_file": "item_6_2.png", "label": "Pregunta 6.2 (Resposta oberta - PART 2)", "desc": "Calcula la superfície que ha de tenir l'aparcament ampliat i explica el raonament a escala."},

            {"kind": "section", "title": "Activitat 2. El bus escolar", "desc": "Ítems del 7 al 12. Situació: municipis de la vall Plana, distàncies per carretera, velocitat mitjana i rutes òptimes."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: pobles de la vall Plana i distàncies per carretera"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "image", "file": "context_act2_lluc.png", "title": "Context per als ítems 10, 11 i 12: trajectes diaris d'en Lluc en bus escolar"},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},

            {"kind": "section", "title": "Activitat 3. El barri de la Lídia i el Marc", "desc": "Ítems del 13 al 19. Situació: plànol de la ciutat, illes de cases, codificació amb punts cardinals i mesures del parc."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: plànol de la ciutat amb les cases de la Lídia, el Marc, l'institut i la biblioteca"},
            {"kind": "item", "num": 13},
            {"kind": "open_item", "num": 14, "label": "Pregunta 14 (Resposta oberta - PART 2)", "desc": "Explica per què el camí triat és el més curt i descriu el recorregut."},
            {"kind": "image", "file": "context_act3_codificacio.png", "title": "Context: codificació de trajectes amb punts cardinals (N, S, E, O)"},
            {"kind": "item", "num": 15},
            {"kind": "open_item", "num": 16, "label": "Pregunta 16 (Resposta oberta - PART 2)", "desc": "Utilitza la codificació (N, S, E, O) per escriure tots els trajectes possibles de 4 costats d'illa."},
            {"kind": "image", "file": "context_act3_parc.png", "title": "Context per als ítems 17, 18 i 19: plànol i mides del parc"},
            {"kind": "open_item", "num": 17, "label": "Pregunta 17 (Resposta oberta - PART 2)", "desc": "Calcula quants metres quadrats té el parc i escriu els càlculs i raonaments."},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},

            {"kind": "section", "title": "Activitat 4. Bitllets de metro", "desc": "Ítems del 20 al 23. Situació: xarxa de metro, tarifes de bitllets (senzill, abonament 8 viatges, abonament mensual) i optimització de despesa."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: preus i característiques dels tipus de bitllets de metro"},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "open_item", "num": 23, "label": "Pregunta 23 (Resposta oberta - PART 2)", "desc": "Digues quina combinació de bitllets és la més barata per al curs de teatre explicant detalladament càlculs i raonaments."}
        ]
    },
    ("4ESO", "CTE", 2026): {
        "title": "4t d’ESO · Ciència, tecnologia i enginyeria 2026 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2026_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència en ciència, tecnologia i enginyeria (Curs 2025-2026)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 25 preguntes (40 ítems avaluats, total 40 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2026_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2026_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. L’hidrogen verd", "desc": "Ítems de l'1 al 7. Situació: obtenció d'hidrogen verd per electròlisi, energies renovables, avantatges/inconvenients, vàlvules de seguretat actives i passives, transport i desenvolupament sostenible."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: característiques de l’hidrogen molecular i autobús d'hidrogen"},
            {"kind": "item", "num": 1},
            {"kind": "image", "file": "item_2.png", "title": "Pregunta 2: Característiques de l'hidrogen"},
            {"kind": "item", "num": "2_1", "img_file": None, "label": "Pregunta 2.1: En la combustió de l’hidrogen no s’allibera diòxid de carboni.", "options": ["Avantatge", "Inconvenient"]},
            {"kind": "item", "num": "2_2", "img_file": None, "label": "Pregunta 2.2: La producció d’hidrogen requereix un consum elevat d’energia.", "options": ["Avantatge", "Inconvenient"]},
            {"kind": "item", "num": "2_3", "img_file": None, "label": "Pregunta 2.3: L’hidrogen és un gas que requereix condicions especials d’emmagatzematge.", "options": ["Avantatge", "Inconvenient"]},
            {"kind": "item", "num": "2_4", "img_file": None, "label": "Pregunta 2.4: Es pot produir hidrogen a partir d’energies renovables, reduint la dependència dels combustibles fòssils.", "options": ["Avantatge", "Inconvenient"]},
            {"kind": "image", "file": "context_act1_grafic.png", "title": "Context per a la pregunta 3: previsió de producció global anual d'hidrogen verd (2025-2030)"},
            {"kind": "item", "num": 3},
            {"kind": "image", "file": "item_4.png", "title": "Pregunta 4: Sistemes de seguretat actius i passius en dipòsits d'hidrogen"},
            {"kind": "item", "num": "4_1", "img_file": None, "label": "Pregunta 4.1: Una molla es deforma en arribar a nivells alts de pressió.", "options": ["Actiu", "Passiu"]},
            {"kind": "item", "num": "4_2", "img_file": None, "label": "Pregunta 4.2: Un cristall piezoelèctric capta nivells massa alts de pressió.", "options": ["Actiu", "Passiu"]},
            {"kind": "item", "num": "4_3", "img_file": None, "label": "Pregunta 4.3: Un electroimant s’activa en detectar temperatures perilloses.", "options": ["Actiu", "Passiu"]},
            {"kind": "item", "num": "4_4", "img_file": None, "label": "Pregunta 4.4: Un tap fet d’un cert material es fon en arribar a la temperatura perillosa.", "options": ["Actiu", "Passiu"]},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},

            {"kind": "section", "title": "Activitat 2. Donar sang és donar vida", "desc": "Ítems del 8 al 18. Situació: components de la sang, requisits mèdics per donar sang, anàlisis de laboratori, conservació, compatibilitat sanguínia AB0/Rh i recerca científica."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: campanyes de donació de sang i cèl·lules sanguínies"},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "image", "file": "context_act2_compatibilitat.png", "title": "Context per als ítems 15 i 16: quadre de compatibilitat sanguínia (sistema AB0 i factor Rh)"},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "image", "file": "item_18_intro.png", "title": "Pregunta 18: Donació de sang altruista (introducció)"},
            {"kind": "image", "file": "item_18.png", "title": "Pregunta 18: Arguments a favor de la donació altruista de sang"},
            {"kind": "item", "num": "18_1", "img_file": None, "label": "Pregunta 18.1: Evita la discriminació econòmica.", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "18_2", "img_file": None, "label": "Pregunta 18.2: Millora la confiança en el sistema sanitari.", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "18_3", "img_file": None, "label": "Pregunta 18.3: Garanteix la seguretat i qualitat de la sang.", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "18_4", "img_file": None, "label": "Pregunta 18.4: Fomenta la solidaritat i la responsabilitat social.", "options": ["A", "B", "C", "D", "E"]},

            {"kind": "section", "title": "Activitat 3. Observació de la fauna salvatge", "desc": "Ítems del 19 al 25. Situació: paranys fotogràfics, sensors d'infrarojos, mètode científic, impactes ambientals positius/negatius i anàlisi de registres de fauna."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: paranys fotogràfics i característiques tècniques"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "item_23.png", "title": "Pregunta 23: Impactes mediambientals dels paranys fotogràfics"},
            {"kind": "item", "num": "23_1", "img_file": None, "label": "Pregunta 23.1: Aporten dades que ajuden a combatre la sobrepoblació d’algunes espècies.", "options": ["Positiu", "Negatiu"]},
            {"kind": "item", "num": "23_2", "img_file": None, "label": "Pregunta 23.2: Incrementen la presència de persones en els espais naturals protegits.", "options": ["Positiu", "Negatiu"]},
            {"kind": "item", "num": "23_3", "img_file": None, "label": "Pregunta 23.3: Quan deixen de funcionar, poden convertir-se en residus si no es reciclen adequadament.", "options": ["Positiu", "Negatiu"]},
            {"kind": "item", "num": "23_4", "img_file": None, "label": "Pregunta 23.4: Permeten fer el seguiment d’animals en vies d’extinció i contribueixen a protegir-los.", "options": ["Positiu", "Negatiu"]},
            {"kind": "image", "file": "item_24.png", "title": "Pregunta 24: Registre d'observacions dels dos paranys fotogràfics"},
            {"kind": "item", "num": "24_1", "img_file": None, "label": "Pregunta 24.1: El porc senglar es desplaça en grups.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "24_2", "img_file": None, "label": "Pregunta 24.2: Totes les espècies observades són mamífers.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "24_3", "img_file": None, "label": "Pregunta 24.3: El cérvol mostra activitat a primeres hores del matí.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "24_4", "img_file": None, "label": "Pregunta 24.4: El teixó restringeix la seva activitat a la zona propera al parany 1.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 25}
        ]
    },
    ("4ESO", "CTE", 2025): {
        "title": "4t d’ESO · Ciència, tecnologia i enginyeria 2025 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2025_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència en ciència, tecnologia i enginyeria (Curs 2024-2025)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 25 preguntes (40 ítems avaluats, total 40 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2025_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2025_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. La qualitat de l’aire a l’aula", "desc": "Ítems de l'1 al 7. Situació: mesura i control del CO2 a les aules, ventilació creuada, sensors infrarojos (IR) i concentracions màximes recomanades."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: renovació d'aire i concentració de CO2 a les aules"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "image", "file": "context_act1_grafic.png", "title": "Context per a la pregunta 3: evolució de la concentració de CO2 durant la jornada escolar"},
            {"kind": "item", "num": 3},
            {"kind": "image", "file": "context_act1_fig2.png", "title": "Context per a la pregunta 4: canvi de volum d'aire per ventilació creuada"},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "item_5.png", "title": "Pregunta 5: Esquema simplificat d'un sensor infraroig (IR) de CO2"},
            {"kind": "item", "num": "5_1", "img_file": None, "label": "Pregunta 5.1: Cambra", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_2", "img_file": None, "label": "Pregunta 5.2: Detector", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_3", "img_file": None, "label": "Pregunta 5.3: Filtre òptic", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_4", "img_file": None, "label": "Pregunta 5.4: Làmpada IR", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},

            {"kind": "section", "title": "Activitat 2. L’ecolocalització en els dofins", "desc": "Ítems del 8 al 14. Situació: emissió i recepció d'ultrasons en cetacis, velocitat de propagació del so en diferents medis, fisiologia marina i contaminació acústica."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: ecolocalització dels dofins per a l'orientació i la caça"},
            {"kind": "item", "num": 8},
            {"kind": "image", "file": "item_9.png", "title": "Pregunta 9: Etapes del sistema d'ecolocalització dels dofins"},
            {"kind": "item", "num": "9_1", "img_file": None, "label": "Pregunta 9.1: Etapa 1", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "9_2", "img_file": None, "label": "Pregunta 9.2: Etapa 2", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "9_3", "img_file": None, "label": "Pregunta 9.3: Etapa 3", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "9_4", "img_file": None, "label": "Pregunta 9.4: Etapa 4", "options": ["A", "B", "C", "D"]},
            {"kind": "image", "file": "context_act2_taula2.png", "title": "Context per a la pregunta 10: velocitat de propagació del so en diversos medis"},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "image", "file": "context_act2_fig3.png", "title": "Context per a la pregunta 12: freqüències i espectre sonor de l'ecolocalització"},
            {"kind": "item", "num": 12},
            {"kind": "image", "file": "item_13.png", "title": "Pregunta 13: Conseqüències de la contaminació acústica en els dofins"},
            {"kind": "item", "num": "13_1", "img_file": None, "label": "Pregunta 13.1: Provocar la desorientació dels dofins.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "13_2", "img_file": None, "label": "Pregunta 13.2: Afectar la comunicació entre els dofins.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "13_3", "img_file": None, "label": "Pregunta 13.3: Dificultar l'obtenció d'aliment per part dels dofins.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "13_4", "img_file": None, "label": "Pregunta 13.4: Augmentar la quantitat de residus en l'hàbitat dels dofins.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 14},

            {"kind": "section", "title": "Activitat 3. Centrals hidroelèctriques reversibles", "desc": "Ítems del 15 al 19. Situació: generació hidroelèctrica per bombeig, integració amb fonts renovables (eòlica, solar fotovoltaica, nuclear), gestió de la xarxa elèctrica i corbes de demanda horària."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: esquema d'una central hidroelèctrica reversible"},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "image", "file": "context_act3_fig2.png", "title": "Context per als ítems 17, 18 i 19: balanç horari de demanda i producció elèctrica"},
            {"kind": "item", "num": 17},
            {"kind": "item", "num": 18},
            {"kind": "image", "file": "item_19.png", "title": "Pregunta 19: Anàlisi de la demanda i fonts de generació elèctrica"},
            {"kind": "item", "num": "19_1", "img_file": None, "label": "Pregunta 19.1: Ha fet més vent a la tarda que al migdia.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_2", "img_file": None, "label": "Pregunta 19.2: Les tres fonts d'energia han produït electricitat durant tot el dia.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_3", "img_file": None, "label": "Pregunta 19.3: Les hores vall de demanda elèctrica s'han situat principalment durant la matinada.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_4", "img_file": None, "label": "Pregunta 19.4: Es genera potència elèctrica d'origen nuclear només durant les hores punta de demanda elèctrica.", "options": ["SÍ", "NO"]},

            {"kind": "section", "title": "Activitat 4. Aigua al planeta Mart", "desc": "Ítems del 20 al 25. Situació: condicions atmosfèriques de Mart, obtenció d'oxigen i hidrogen mitjançant l'electròlisi de l'aigua, reaccions químiques, muntatge experimental i balanç de masses."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: presència d'aigua i característiques atmosfèriques de Mart"},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "context_act4_electrolisi.png", "title": "Context per a la pregunta 23: muntatge experimental per a l'electròlisi de l'aigua"},
            {"kind": "image", "file": "item_23.png", "title": "Pregunta 23: Condicions i característiques de l'electròlisi de l'aigua"},
            {"kind": "item", "num": "23_1", "img_file": None, "label": "Pregunta 23.1: S'aplica un corrent elèctric continu.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "23_2", "img_file": None, "label": "Pregunta 23.2: S'afegeix una mica d'àcid a l'aigua.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "23_3", "img_file": None, "label": "Pregunta 23.3: S'utilitzen elèctrodes fets de materials aïllants.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "23_4", "img_file": None, "label": "Pregunta 23.4: S'obté el mateix volum d'oxigen gasós que d'hidrogen gasós.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25}
        ]
    },
    ("4ESO", "CTE", 2024): {
        "title": "4t d’ESO · Ciència, tecnologia i enginyeria 2024 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2024_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència en ciència, tecnologia i enginyeria (Curs 2023-2024)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 25 preguntes (45 ítems avaluats, total 45 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2024_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2024_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Sense gluten", "desc": "Ítems de l'1 al 6. Situació: celiaquia, composició nutricional dels cereals, etiquetatge d'aliments, contaminació creuada i mètodes de prevenció."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: farines, gluten i reacció autoimmune"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "image", "file": "item_4.png", "title": "Pregunta 4: Mesures per evitar la contaminació creuada per gluten"},
            {"kind": "item", "num": "4_1", "img_file": None, "label": "Pregunta 4.1: Utilitzar els mateixos estris per cuinar tots els aliments.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "4_2", "img_file": None, "label": "Pregunta 4.2: Guardar el menjar sense gluten a la nevera dins d'un envàs tancat.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "4_3", "img_file": None, "label": "Pregunta 4.3: Netejar les superfícies de treball de la cuina utilitzant paper d'un sol ús.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "4_4", "img_file": None, "label": "Pregunta 4.4: Fregir un aliment sense gluten aprofitant l'oli utilitzat per cuinar altres aliments.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},

            {"kind": "section", "title": "Activitat 2. Calderes de biomassa", "desc": "Ítems del 7 al 13. Situació: biomassa forestal com a font d'energia tèrmica, gestió forestal sostenible, poder calorífic, cicle del carboni i components tècnics d'una caldera."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: calderes d'estella forestal i gestió dels boscos"},
            {"kind": "image", "file": "item_7.png", "title": "Pregunta 7: Propietats de la biomassa forestal"},
            {"kind": "item", "num": "7_1", "img_file": None, "label": "Pregunta 7.1: És una font d'energia renovable.", "options": ["V", "F"]},
            {"kind": "item", "num": "7_2", "img_file": None, "label": "Pregunta 7.2: Permet reduir el consum de combustibles fòssils.", "options": ["V", "F"]},
            {"kind": "item", "num": "7_3", "img_file": None, "label": "Pregunta 7.3: S'utilitza com a font d'energia des de fa poc temps.", "options": ["V", "F"]},
            {"kind": "item", "num": "7_4", "img_file": None, "label": "Pregunta 7.4: Només s'utilitza per escalfar aigua destinada a les aixetes i a la calefacció.", "options": ["V", "F"]},
            {"kind": "item", "num": 8},
            {"kind": "image", "file": "item_9.png", "title": "Pregunta 9: Factors que influeixen en el poder calorífic de l'estella"},
            {"kind": "item", "num": "9_1", "img_file": None, "label": "Pregunta 9.1: De les dimensions de la caldera.", "options": ["V", "F"]},
            {"kind": "item", "num": "9_2", "img_file": None, "label": "Pregunta 9.2: Del grau d'humitat que tingui l'estella.", "options": ["V", "F"]},
            {"kind": "item", "num": "9_3", "img_file": None, "label": "Pregunta 9.3: De la quantitat total d'estella que es cremi.", "options": ["V", "F"]},
            {"kind": "item", "num": "9_4", "img_file": None, "label": "Pregunta 9.4: Del tipus de fusta a partir del qual s'obtingui l'estella.", "options": ["V", "F"]},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},

            {"kind": "section", "title": "Activitat 3. La invasió de les meduses", "desc": "Ítems del 14 al 19. Situació: proliferació de meduses a la costa mediterrània, factors biològics i ecològics, xarxa tròfica marina, cicle de vida i relacions causa-efecte."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: proliferació de meduses al litoral i canvi global"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "item", "num": 18},
            {"kind": "image", "file": "item_19.png", "title": "Pregunta 19: Causes i conseqüències de l'augment de meduses"},
            {"kind": "item", "num": "19_1", "img_file": None, "label": "Pregunta 19.1: Perjudicis econòmics al sector turístic.", "options": ["Causa", "Conseqüència"]},
            {"kind": "item", "num": "19_2", "img_file": None, "label": "Pregunta 19.2: Increment del nombre de visites mèdiques per atendre picades de medusa.", "options": ["Causa", "Conseqüència"]},
            {"kind": "item", "num": "19_3", "img_file": None, "label": "Pregunta 19.3: Augment de la quantitat de nutrients en l'aigua del mar degut als abocaments de residus orgànics.", "options": ["Causa", "Conseqüència"]},
            {"kind": "item", "num": "19_4", "img_file": None, "label": "Pregunta 19.4: Disminució del nombre de depredadors naturals de les meduses, com ara les tortugues marines o les tonyines.", "options": ["Causa", "Conseqüència"]},

            {"kind": "section", "title": "Activitat 4. Impressió en 3D", "desc": "Ítems del 20 al 25. Situació: impressora 3D de filament fos (FDM), eixos de moviment, transformacions d'energia, farciment estructural (infill) i propietats dels polímers (PLA, ABS, PET, TPU)."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: tecnologia d'impressió 3D per filament fos (FDM)"},
            {"kind": "image", "file": "item_20.png", "title": "Pregunta 20: Moviments dels components d'una impressora 3D"},
            {"kind": "item", "num": "20_1", "img_file": None, "label": "Pregunta 20.1: Moviment circular.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "20_2", "img_file": None, "label": "Pregunta 20.2: Moviment amunt o avall.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "20_3", "img_file": None, "label": "Pregunta 20.3: Moviment cap a la dreta o esquerra.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "20_4", "img_file": None, "label": "Pregunta 20.4: Moviment endavant o endarrere.", "options": ["A", "B", "C", "D"]},
            {"kind": "image", "file": "item_21.png", "title": "Pregunta 21: Transformacions d'energia en una impressora 3D"},
            {"kind": "item", "num": "21_1", "img_file": None, "label": "Pregunta 21.1: D’energia mecànica a energia elèctrica en l’extrusor.", "options": ["V", "F"]},
            {"kind": "item", "num": "21_2", "img_file": None, "label": "Pregunta 21.2: D’energia elèctrica a energia mecànica en els motors.", "options": ["V", "F"]},
            {"kind": "item", "num": "21_3", "img_file": None, "label": "Pregunta 21.3: D’energia tèrmica a energia elèctrica en la plataforma.", "options": ["V", "F"]},
            {"kind": "item", "num": "21_4", "img_file": None, "label": "Pregunta 21.4: D’energia elèctrica a energia tèrmica en el capçal calent.", "options": ["V", "F"]},
            {"kind": "item", "num": 22},
            {"kind": "image", "file": "item_23.png", "title": "Pregunta 23: Efectes del percentatge de farciment (infill) en objectes impresos"},
            {"kind": "item", "num": "23_1", "img_file": None, "label": "Pregunta 23.1: Fa més soroll si el sacsegem.", "options": ["V", "F"]},
            {"kind": "item", "num": "23_2", "img_file": None, "label": "Pregunta 23.2: Es fon a una temperatura més baixa si l’escalfem.", "options": ["V", "F"]},
            {"kind": "item", "num": "23_3", "img_file": None, "label": "Pregunta 23.3: Sura més fàcilment si el submergim en un líquid.", "options": ["V", "F"]},
            {"kind": "item", "num": "23_4", "img_file": None, "label": "Pregunta 23.4: Es trenca més fàcilment si el sotmetem a grans esforços.", "options": ["V", "F"]},
            {"kind": "item", "num": 24},
            {"kind": "image", "file": "item_25.png", "title": "Pregunta 25: Elecció del material plàstic de filament segons requisits tècnics"},
            {"kind": "item", "num": "25_1", "img_file": None, "label": "Pregunta 25.1: Molt resistent als cops.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "25_2", "img_file": None, "label": "Pregunta 25.2: Respectuós amb el medi ambient.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "25_3", "img_file": None, "label": "Pregunta 25.3: Que les capes d’impressió quedin ben adherides.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "25_4", "img_file": None, "label": "Pregunta 25.4: Que es pugui submergir en aigua a punt de bullir sense que es faci malbé.", "options": ["A", "B", "C", "D"]}
        ]
    },
    ("2ESO", "CTE", 2026): {
        "title": "2n d’ESO · Ciències experimentals i tecnologia 2026 · Prova oficial AD",
        "docTitle": "2ESO-CTE_AD-2026_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Ciències experimentals i tecnologia (Curs 2025-2026)\nInstitut Escola Sant Pol de Mar\n\nProva oficial autocorregible de 25 preguntes (40 ítems avaluats, total 40 punts).",
        "target_folder": "2ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2026_CTE_prova.pdf",
        "crops_dir": "scratch/crops_2eso_cte_2026_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. L’etiqueta d’eficiència energètica", "desc": "Ítems de l'1 al 8. Situació: consum elèctric, etiquetatge energètic d'electrodomèstics, transformacions d'energia i gestió de residus."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: normativa de l'etiqueta d'eficiència energètica"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "item_5.png", "title": "Pregunta 5: Receptors d'una rentadora i transformació d'energia"},
            {"kind": "item", "num": "5_1", "img_file": None, "label": "Pregunta 5.1: Díode LED", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "5_2", "img_file": None, "label": "Pregunta 5.2: Avisador acústic", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "5_3", "img_file": None, "label": "Pregunta 5.3: Resistència que escalfa l'aigua", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "5_4", "img_file": None, "label": "Pregunta 5.4: Motor del tambor de centrifugat", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},
            {"kind": "image", "file": "item_8.png", "title": "Pregunta 8: Gestió dels electrodomèstics vells al final de la seva vida útil"},
            {"kind": "item", "num": "8_1", "img_file": None, "label": "Pregunta 8.1: Recollida i lliurament", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "8_2", "img_file": None, "label": "Pregunta 8.2: Desballestament i separació de materials", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "8_3", "img_file": None, "label": "Pregunta 8.3: Reciclatge i reutilització", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "8_4", "img_file": None, "label": "Pregunta 8.4: Eliminació segura", "options": ["A", "B", "C", "D", "E"]},

            {"kind": "section", "title": "Activitat 2. La desaparició de les abelles", "desc": "Ítems del 9 al 18. Situació: pol·linització, taxonomia, paràsits (Varroa destructor), pesticides i robòtica aplicada."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: procés de pol·linització i rusc d'abelles"},
            {"kind": "item", "num": 9},
            {"kind": "image", "file": "item_10.png", "title": "Pregunta 10: Fases del procés de pol·linització"},
            {"kind": "item", "num": "10_1", "img_file": None, "label": "Pregunta 10.1: Fase 1", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "10_2", "img_file": None, "label": "Pregunta 10.2: Fase 2", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "10_3", "img_file": None, "label": "Pregunta 10.3: Fase 3", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "10_4", "img_file": None, "label": "Pregunta 10.4: Fase 4", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},
            {"kind": "image", "file": "item_14.png", "title": "Pregunta 14: Causes de la reducció de la població d'abelles"},
            {"kind": "item", "num": "14_1", "img_file": None, "label": "Pregunta 14.1: Canvi climàtic", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "14_2", "img_file": None, "label": "Pregunta 14.2: Pèrdua i fragmentació d'hàbitats", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "14_3", "img_file": None, "label": "Pregunta 14.3: Ús excessiu de pesticides", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": "14_4", "img_file": None, "label": "Pregunta 14.4: Espècies invasores", "options": ["A", "B", "C", "D", "E"]},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "image", "file": "item_18.png", "title": "Pregunta 18: Prototip de robot pol·linitzador per a hivernacles"},
            {"kind": "item", "num": "18_1", "img_file": None, "label": "Pregunta 18.1: L'objectiu és substituir totalment les abelles als ecosistemes naturals.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "18_2", "img_file": None, "label": "Pregunta 18.2: És una mesura que resol la causa principal de la disminució d'abelles.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "18_3", "img_file": None, "label": "Pregunta 18.3: Permet garantir la pol·linització dels conreus en entorns tancats.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "18_4", "img_file": None, "label": "Pregunta 18.4: És una solució tecnològica complementària a la conservació d'espècies.", "options": ["SÍ", "NO"]},

            {"kind": "section", "title": "Activitat 3. Les estacions meteorològiques", "desc": "Ítems del 19 al 25. Situació: instruments de mesura atmosfèrica, ubicació d'estacions, sensors de temperatura i pressió, i anàlisi de climogrames."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: equipament d'una estació meteorològica"},
            {"kind": "image", "file": "item_19.png", "title": "Pregunta 19: Condicions d'instal·lació d'una estació meteorològica"},
            {"kind": "item", "num": "19_1", "img_file": None, "label": "Pregunta 19.1: S'ha de situar en un terreny obert, lliure d'obstacles propers.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_2", "img_file": None, "label": "Pregunta 19.2: Els sensors han d'estar directament exposats al sol sense cap protecció.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_3", "img_file": None, "label": "Pregunta 19.3: La garita meteorològica ha d'estar pintada de blanc per reflectir la radiació.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "19_4", "img_file": None, "label": "Pregunta 19.4: S'ha de col·locar sobre una superfície d'asfalt per mesurar millor la calor.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "image", "file": "context_act3_climograma.png", "title": "Context per als ítems 24 i 25: climograma de precipitacions i temperatures"},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25}
        ]
    },
    ("2ESO", "CTE", 2025): {
        "title": "2n d’ESO · Ciències experimentals 2025 · Prova oficial AD",
        "docTitle": "2ESO-CTE_AD-2025_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Ciències experimentals (Curs 2024-2025)\nInstitut Escola Sant Pol de Mar\n\nProva oficial mixta (21 preguntes autocorregibles de test + 4 ítems de resposta oberta PART 2).",
        "target_folder": "2ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2025_CTE_prova.pdf",
        "crops_dir": "scratch/crops_2eso_cte_2025_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Les begudes isotòniques", "desc": "Ítems de l'1 al 8. Situació: composició de sals i sucres, hidratació, mesura amb instruments de laboratori, reducció d'envasos plàstics i sostenibilitat."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: característiques de les begudes isotòniques"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "image", "file": "item_5.png", "title": "Pregunta 5: Instruments de laboratori per preparar la beguda"},
            {"kind": "item", "num": "5_1", "img_file": None, "label": "Pregunta 5.1: Matràs aforat", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_2", "img_file": None, "label": "Pregunta 5.2: Probeta graduada", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_3", "img_file": None, "label": "Pregunta 5.3: Vas de precipitats", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "5_4", "img_file": None, "label": "Pregunta 5.4: Balança digital", "options": ["A", "B", "C", "D"]},
            {"kind": "image", "file": "item_6.png", "title": "Pregunta 6: Reducció i reciclatge d'envasos de plàstic"},
            {"kind": "item", "num": "6_1", "img_file": None, "label": "Pregunta 6.1: Reduir", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "6_2", "img_file": None, "label": "Pregunta 6.2: Reutilitzar", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "6_3", "img_file": None, "label": "Pregunta 6.3: Reciclar", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "6_4", "img_file": None, "label": "Pregunta 6.4: Recuperar", "options": ["A", "B", "C", "D"]},
            {"kind": "open_item", "num": 7, "label": "Pregunta 7 (Resposta oberta - PART 2)", "desc": "Quin benefici ambiental pot comportar aquesta mesura? Raona la teva resposta."},
            {"kind": "open_item", "num": 8, "label": "Pregunta 8 (Resposta oberta - PART 2)", "desc": "Calcula el volum d'aigua i explica els càlculs i raonaments."},

            {"kind": "section", "title": "Activitat 2. La cursa més ràpida de la història", "desc": "Ítems del 9 al 18. Situació: rècord mundial de 100 metres d'Usain Bolt, càlcul de velocitat i acceleració, fases de la cursa i fisiologia muscular."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: gràfic de posició-temps i taula de velocitats de la cursa"},
            {"kind": "item", "num": 9},
            {"kind": "image", "file": "item_10.png", "title": "Pregunta 10: Acceleració en els trams de la cursa"},
            {"kind": "item", "num": "10_1", "img_file": None, "label": "Pregunta 10.1: Tram 0-20 m", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "10_2", "img_file": None, "label": "Pregunta 10.2: Tram 20-40 m", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "10_3", "img_file": None, "label": "Pregunta 10.3: Tram 40-60 m", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "10_4", "img_file": None, "label": "Pregunta 10.4: Tram 60-80 m", "options": ["SÍ", "NO"]},
            {"kind": "open_item", "num": 11, "label": "Pregunta 11 (Resposta oberta - PART 2)", "desc": "Explica detalladament el raonament a partir del gràfic i la taula."},
            {"kind": "image", "file": "item_12.png", "title": "Pregunta 12: Fases de la cursa i estructures corporals"},
            {"kind": "item", "num": "12_1", "img_file": None, "label": "Pregunta 12.1: Fase inicial", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "12_2", "img_file": None, "label": "Pregunta 12.2: Fase de màxima velocitat", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "12_3", "img_file": None, "label": "Pregunta 12.3: Fase de desacceleració", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "12_4", "img_file": None, "label": "Pregunta 12.4: Arribada a meta", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "open_item", "num": 18, "label": "Pregunta 18 (Resposta oberta - PART 2)", "desc": "Dissenya l'experiment i indica les variables controlades i independents."},

            {"kind": "section", "title": "Activitat 3. Bàsquet App", "desc": "Ítems del 19 al 25. Situació: disseny d'una aplicació esportiva mòbil, botons d'acció, anàlisi de dades estadístiques i circuits d'alimentació elèctrica."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: pantalla de l'aplicació Bàsquet App"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "image", "file": "item_21.png", "title": "Pregunta 21: Funcionalitats de l'aplicació mòbil"},
            {"kind": "item", "num": "21_1", "img_file": None, "label": "Pregunta 21.1: Permet registrar la posició exacta del llançament a la pista.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "21_2", "img_file": None, "label": "Pregunta 21.2: Enregistra automàticament la jugada sense intervenció de l'usuari.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "21_3", "img_file": None, "label": "Pregunta 21.3: Permet modificar el resultat després de finalitzar el partit.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "21_4", "img_file": None, "label": "Pregunta 21.4: Mostra estadístiques individualitzades de cada jugador/a.", "options": ["SÍ", "NO"]},
            {"kind": "image", "file": "item_22.png", "title": "Pregunta 22: Càlcul d'efectivitat de tir"},
            {"kind": "item", "num": "22_1", "img_file": None, "label": "Pregunta 22.1: Jugadora amb millor percentatge de tirs lliures.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "22_2", "img_file": None, "label": "Pregunta 22.2: Jugadora amb més tirs de 2 punts encistellats.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "22_3", "img_file": None, "label": "Pregunta 22.3: Jugadora amb menor efectivitat en tirs triples.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": "22_4", "img_file": None, "label": "Pregunta 22.4: Jugadora amb màxima puntuació total.", "options": ["A", "B", "C", "D"]},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "image", "file": "item_25.png", "title": "Pregunta 25: Característiques tècniques de la bateria"},
            {"kind": "item", "num": "25_1", "img_file": None, "label": "Pregunta 25.1: La tensió d'entrada és de corrent continu.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "25_2", "img_file": None, "label": "Pregunta 25.2: La potència màxima és de 50 W.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "25_3", "img_file": None, "label": "Pregunta 25.3: La freqüència del carregador és de 50-60 Hz.", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "25_4", "img_file": None, "label": "Pregunta 25.4: Disposa de protecció contra sobreescalfament.", "options": ["SÍ", "NO"]}
        ]
    },
    ("2ESO", "CTE", 2024): {
        "title": "2n d’ESO · Ciències experimentals 2024 · Prova oficial AD",
        "docTitle": "2ESO-CTE_AD-2024_prova-autocorregible",
        "desc_header": "Avaluació de diagnòstic — Ciències experimentals (Curs 2023-2024)\nInstitut Escola Sant Pol de Mar\n\nProva oficial mixta (17 preguntes autocorregibles de test + 6 ítems de resposta oberta PART 2).",
        "target_folder": "2ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/2ESO/ciencia_tecnologia/2ESO_AD_2024_CTE_prova.pdf",
        "crops_dir": "scratch/crops_2eso_cte_2024_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. L’escalfament global", "desc": "Ítems de l'1 al 6. Situació: composició atmosfèrica, efecte d'hivernacle natural i antropogènic, gasos emissors, absorció de radiació tèrmica i petjada de carboni."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context inicial: l'atmosfera terrestre i l'efecte d'hivernacle"},
            {"kind": "image", "file": "item_1.png", "title": "Pregunta 1: Gasos de l'atmosfera i efecte d'hivernacle"},
            {"kind": "item", "num": "1_1", "img_file": None, "label": "Pregunta 1.1: El produeixen tots els gasos presents a l’atmosfera.", "options": ["V", "F"]},
            {"kind": "item", "num": "1_2", "img_file": None, "label": "Pregunta 1.2: Ha augmentat de manera important durant les últimes dècades.", "options": ["V", "F"]},
            {"kind": "item", "num": "1_3", "img_file": None, "label": "Pregunta 1.3: És degut exclusivament a les emissions de gasos d’origen humà.", "options": ["V", "F"]},
            {"kind": "image", "file": "item_2.png", "title": "Pregunta 2: Conseqüències de l'absència d'efecte d'hivernacle"},
            {"kind": "item", "num": "2_1", "img_file": None, "label": "Pregunta 2.1: L’aire seria irrespirable per a les persones.", "options": ["V", "F"]},
            {"kind": "item", "num": "2_2", "img_file": None, "label": "Pregunta 2.2: La fotosíntesi de les plantes resultaria afectada.", "options": ["V", "F"]},
            {"kind": "item", "num": "2_3", "img_file": None, "label": "Pregunta 2.3: La temperatura mitjana de l’aire superficial de la Terra baixaria dràsticament.", "options": ["V", "F"]},
            {"kind": "image", "file": "item_3.png", "title": "Pregunta 3: Fonts d'emissió de gasos"},
            {"kind": "item", "num": "3_1", "img_file": None, "label": "Pregunta 3.1: Activitats agrícoles i ramaderes.", "options": ["A", "B", "C"]},
            {"kind": "item", "num": "3_2", "img_file": None, "label": "Pregunta 3.2: Crema de combustibles fòssils.", "options": ["A", "B", "C"]},
            {"kind": "item", "num": "3_3", "img_file": None, "label": "Pregunta 3.3: Descomposició de matèria orgànica en abocadors.", "options": ["A", "B", "C"]},
            {"kind": "image", "file": "item_4.png", "title": "Pregunta 4: Capacitat d'absorció de radiació tèrmica"},
            {"kind": "item", "num": "4_1", "img_file": None, "label": "Pregunta 4.1: Aigua (H2O)", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "4_2", "img_file": None, "label": "Pregunta 4.2: Dioxigen (O2)", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "4_3", "img_file": None, "label": "Pregunta 4.3: Dinitrogen (N2)", "options": ["SÍ", "NO"]},
            {"kind": "open_item", "num": 5, "label": "Pregunta 5 (Resposta oberta - PART 2)", "desc": "Explica com influeix l'augment de CO2 en el desglaç dels casquets polars."},
            {"kind": "open_item", "num": 6, "label": "Pregunta 6 (Resposta oberta - PART 2)", "desc": "Justifica per què consumir aliments de proximitat redueix la petjada de carboni."},

            {"kind": "section", "title": "Activitat 2. Construïm un hivernacle", "desc": "Ítems del 7 al 12. Situació: disseny i muntatge d'un hivernacle escolar, propietats tèrmiques dels materials (vidre vs plàstic), reg eficient i automatització per sensors."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context inicial: estructura i finalitat d'un hivernacle"},
            {"kind": "image", "file": "item_7.png", "title": "Pregunta 7: Etapes de disseny i construcció de l'hivernacle"},
            {"kind": "item", "num": "7_1", "img_file": None, "label": "Pregunta 7.1: Etapa 1", "options": ["A", "B", "C"]},
            {"kind": "item", "num": "7_2", "img_file": None, "label": "Pregunta 7.2: Etapa 3", "options": ["A", "B", "C"]},
            {"kind": "item", "num": "7_3", "img_file": None, "label": "Pregunta 7.3: Etapa 5", "options": ["A", "B", "C"]},
            {"kind": "item", "num": 8},
            {"kind": "open_item", "num": 9, "label": "Pregunta 9 (Resposta oberta - PART 2)", "desc": "Compara els avantatges i inconvenients del plàstic i el vidre per a la coberta."},
            {"kind": "open_item", "num": 10, "label": "Pregunta 10 (Resposta oberta - PART 2)", "desc": "Dissenya el sistema de recollida d'aigua de pluja de l'hivernacle."},
            {"kind": "item", "num": 11},
            {"kind": "image", "file": "item_12.png", "title": "Pregunta 12: Algorisme de reg automàtic"},
            {"kind": "item", "num": "12_1", "img_file": None, "label": "Pregunta 12.1: Pas A de l'algorisme", "options": ["1", "2", "3"]},
            {"kind": "item", "num": "12_2", "img_file": None, "label": "Pregunta 12.2: Pas B de l'algorisme", "options": ["1", "2", "3"]},
            {"kind": "item", "num": "12_3", "img_file": None, "label": "Pregunta 12.3: Pas C de l'algorisme", "options": ["1", "2", "3"]},

            {"kind": "section", "title": "Activitat 3. Investiguem al laboratori", "desc": "Ítems del 13 al 18. Situació: muntatge experimental per simular l'escalfament amb CO2, control de variables, lectura d'instruments i metodologia científica."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context inicial: muntatge experimental amb làmpada d'incandescència i sensors"},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "image", "file": "item_17.png", "title": "Pregunta 17: Instruments de mesura del laboratori"},
            {"kind": "item", "num": "17_1", "img_file": None, "label": "Pregunta 17.1: Balança", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "17_2", "img_file": None, "label": "Pregunta 17.2: Cronòmetre", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": "17_3", "img_file": None, "label": "Pregunta 17.3: Termòmetre", "options": ["SÍ", "NO"]},
            {"kind": "item", "num": 18},

            {"kind": "section", "title": "Activitat 4. Camina, fes salut!", "desc": "Ítems del 19 al 25. Situació: cinemàtica del trajecte a peu, gràfica posició-temps, despesa energètica en kcal i beneficis de l'activitat física."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context inicial: recorregut i gràfic posició-temps del trajecte de la Lídia"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "image", "file": "context_act4_taula.png", "title": "Context: Taula de despesa energètica segons activitat física"},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "open_item", "num": 24, "label": "Pregunta 24 (Resposta oberta - PART 2)", "desc": "Calcula les calories consumides per la Lídia en el seu recorregut."},
            {"kind": "open_item", "num": 25, "label": "Pregunta 25 (Resposta oberta - PART 2)", "desc": "Explica els beneficis per a la salut cardiovascular de caminar diàriament."}
        ]
    }
}

try:
    from config_cb_historics import ANSWERS_HISTORICS, STRUCTURES_HISTORICS
    ANSWERS.update(ANSWERS_HISTORICS)
    STRUCTURES.update(STRUCTURES_HISTORICS)
except Exception as e:
    print(f"Avís en carregar config_cb_historics: {e}")


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

def get_images_cache(drive):
    folder_id = DRIVE_FOLDERS["IMAGES"]
    res = drive.files().list(q=f"'{folder_id}' in parents and trashed=false", pageSize=1000, fields="files(id, name)").execute()
    return {f["name"]: f["id"] for f in res.get("files", [])}

def upload_image(drive, local_path, filename, cache, force_update=True):
    folder_id = DRIVE_FOLDERS["IMAGES"]
    media = MediaFileUpload(str(local_path), mimetype="image/png")
    if filename in cache:
        file_id = cache[filename]
        if force_update:
            drive.files().update(fileId=file_id, media_body=media).execute()
    else:
        file_meta = {"name": filename, "parents": [folder_id]}
        f = drive.files().create(body=file_meta, media_body=media, fields="id").execute()
        file_id = f["id"]
        drive.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()
        cache[filename] = file_id
    
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def upload_pdf_if_needed(drive, pdf_path_str, target_folder_key):
    folder_id = DRIVE_FOLDERS[target_folder_key]
    pdf_path = Path(pdf_path_str)
    filename = pdf_path.name
    q = f"'{folder_id}' in parents and name='{filename}' and trashed=false"
    res = drive.files().list(q=q, fields="files(id,webViewLink)").execute().get("files", [])
    if res:
        return res[0]["webViewLink"]
    media = MediaFileUpload(str(pdf_path), mimetype="application/pdf")
    meta = {"name": filename, "parents": [folder_id]}
    f = drive.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
    drive.permissions().create(fileId=f["id"], body={"role": "reader", "type": "anyone"}).execute()
    return f["webViewLink"]

def create_form_for_exam(curs, materia, any_prova):
    key = (curs, materia, any_prova)
    if key not in STRUCTURES or key not in ANSWERS:
        print(f"Error: configuració no disponible per a {key}")
        return None

    struct = STRUCTURES[key]
    answers_key = ANSWERS[key]
    drive, forms = get_services()

    print(f"\n============================================================")
    print(f"🚀 INICIANT CREACIÓ DE FORMULARI: {struct['title']}")
    print(f"============================================================")

    # 1. Pujar PDF oficial
    pdf_link = upload_pdf_if_needed(drive, struct["pdf_path"], struct["target_folder"])
    print(f"✓ PDF oficial enllaçat: {pdf_link}")

    # 2. Pujar imatges d'exercicis i contextos
    crops_dir = Path(struct["crops_dir"])
    images_urls = {}
    prefix = f"{curs.lower()}_{materia.lower()}_{any_prova}_"
    print(f"↓ Carregant catàleg d'imatges de Drive...")
    img_cache = get_images_cache(drive)
    print(f"↓ Pujant captures de {crops_dir} a Drive...")
    for img_path in sorted(crops_dir.glob("*.png")):
        fn = f"{prefix}{img_path.name}"
        url = upload_image(drive, img_path, fn, img_cache)
        images_urls[img_path.name] = url
    print(f"✓ {len(images_urls)} captures d'alta resolució preparades al Drive.")

    # 3. Crear el Google Form buit
    form_body = {
        "info": {
            "title": struct["title"],
            "documentTitle": struct["docTitle"]
        }
    }
    created_form = forms.forms().create(body=form_body).execute()
    form_id = created_form["formId"]
    print(f"✓ Formulari creat (ID: {form_id})")

    # 4. Moure a la carpeta corresponent i configurar permisos
    target_folder_id = DRIVE_FOLDERS[struct["target_folder"]]
    drive.files().update(
        fileId=form_id,
        addParents=target_folder_id,
        removeParents="root",
        fields="id,parents"
    ).execute()

    # Afegir permisos: públic per lectura, editor per al correu personal
    drive.permissions().create(fileId=form_id, body={"role": "reader", "type": "anyone"}).execute()
    try:
        drive.permissions().create(fileId=form_id, body={"role": "writer", "type": "user", "emailAddress": PERSONAL_EMAIL}).execute()
    except Exception as e:
        print(f"  Avís permissos personals: {e}")
    print(f"✓ Formulari mogut a la carpeta i permisos configurats (públic + editor personal).")

    # 5. Configurar Quiz i descripció
    full_desc = f"{struct['desc_header']}\n\nPodeu consultar el quadern complet oficial en PDF aquí: {pdf_link}"
    requests = [
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
        {
            "updateFormInfo": {
                "info": {
                    "description": full_desc
                },
                "updateMask": "description"
            }
        }
    ]

    # 6. Afegir elements (Seccions, Imatges i Preguntes)
    item_index = 0
    for el in struct["elements"]:
        if el["kind"] == "section":
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
            correct_key = answers_key[num]
            item_label = el.get("label", f"Pregunta {num}")
            img_file = el.get("img_file", f"item_{num}.png")
            img_url = images_urls.get(img_file)
            options = el.get("options", ["a", "b", "c", "d"])

            question_dict = {
                "required": True,
                "grading": {
                    "pointValue": 1,
                    "correctAnswers": {"answers": [{"value": str(correct_key)}]}
                },
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": [{"value": str(opt)} for opt in options],
                    "shuffle": False
                }
            }

            item_dict = {
                "title": item_label,
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
        elif el["kind"] == "open_item":
            num = el["num"]
            item_label = el.get("label", f"Pregunta {num} (Resposta oberta)")
            img_file = el.get("img_file", f"item_{num}.png")
            img_url = images_urls.get(img_file)
            points = el.get("points", 1)
            desc = el.get("desc", "Escriu aquí la teva resposta raonada, els càlculs o la justificació.")

            question_dict = {
                "required": False,
                "grading": {
                    "pointValue": points
                },
                "textQuestion": {
                    "paragraph": True
                }
            }

            item_dict = {
                "title": item_label,
                "description": desc,
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

    print(f"↓ Enviant {len(requests)} peticions de batchUpdate a Forms API...")
    forms.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    print("✓ Formulari completat amb èxit!")

    # Recuperar dades finals i verificar
    form_info = forms.forms().get(formId=form_id).execute()
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    responder_url = form_info.get("responderUri", f"https://docs.google.com/forms/d/e/{form_id}/viewform")

    total_items = sum(1 for el in struct["elements"] if el["kind"] in ("item", "open_item"))
    total_points = sum(el.get("points", 1) for el in struct["elements"] if el["kind"] in ("item", "open_item"))

    print("\n" + "-"*60)
    print(f"🎉 FORMULARI ENLLESTIT: {struct['title']}")
    print(f"• Puntuació: {total_points} punts ({total_items} ítems)")
    print(f"• Enllaç edició: {edit_url}")
    print(f"• Enllaç resposta: {responder_url}")
    print("-" * 60)

    return {
        "curs": curs,
        "materia": materia,
        "any": any_prova,
        "title": struct["title"],
        "items": total_items,
        "points": total_points,
        "edit_url": edit_url,
        "responder_url": responder_url
    }

def main():
    parser = argparse.ArgumentParser(description="Generador de formularis autocorregibles de CB")
    parser.add_argument("--curs", default="4ESO", choices=["4ESO", "2ESO"])
    parser.add_argument("--materia", default="MAT", choices=["MAT", "CTE"])
    parser.add_argument("--any", type=int, default=2026)
    parser.add_argument("--tots", action="store_true", help="Genera tots els configurats")
    args = parser.parse_args()

    if args.tots:
        for k in sorted(STRUCTURES.keys()):
            create_form_for_exam(k[0], k[1], k[2])
    else:
        create_form_for_exam(args.curs, args.materia, args.any)

if __name__ == "__main__":
    main()
