# -*- coding: utf-8 -*-
"""
Configuracions i estructures oficials per als 6 exàmens històrics de Competències Bàsiques (4t ESO 2021-2023).
Institut Escola Sant Pol de Mar — Adrià Santacreu
"""

# ---------------------------------------------------------------------------
# RESPOSTES CORRECTES (ANSWERS)
# ---------------------------------------------------------------------------
ANSWERS_HISTORICS = {
    # ── 4t d'ESO Matemàtiques 2023 ─────────────────────────────────────────
    ("4ESO", "MAT", 2023): {
        1: "a", 2: "d", 3: "c", 4: "c",
        5: "a", 6: "d", 7: "b", 8: "d", 9: "b", 10: "c",
        # 11: obert (2 pts)
        12: "c", 13: "b", 14: "a", 15: "d", 16: "b",
        # 17: obert (2 pts)
        18: "c", 19: "c", 20: "a",
        # 21: obert (2 pts)
        22: "b", 23: "c", 24: "d", 25: "a", 26: "c", 27: "c",
        # 28: obert (2 pts)
        29: "b", 30: "c", 31: "c"
    },

    # ── 4t d'ESO Matemàtiques 2022 ─────────────────────────────────────────
    ("4ESO", "MAT", 2022): {
        1: "d", 2: "d", 3: "b",
        # 4: obert (2 pts)
        5: "c", 6: "c", 7: "d", 8: "d", 9: "c",
        # 10: obert (2 pts)
        11: "b", 12: "b", 13: "c", 14: "b", 15: "a",
        # 16: obert (2 pts)
        17: "c", 18: "c", 19: "a",
        # 20: obert (2 pts)
        21: "a", 22: "b", 23: "b", 24: "b", 25: "c",
        26: "a", 27: "c", 28: "b", 29: "a", 30: "b", 31: "a"
    },

    # ── 4t d'ESO Matemàtiques 2021 ─────────────────────────────────────────
    ("4ESO", "MAT", 2021): {
        1: "d", 2: "c", 3: "d", 4: "a", 5: "d",
        # 6: obert (2 pts)
        7: "b", 8: "b", 9: "c", 10: "a",
        # 11: obert (2 pts)
        12: "b", 13: "c",
        # 14: obert (2 pts)
        15: "b", 16: "b", 17: "a", 18: "a", 19: "c", 20: "d", 21: "c",
        22: "b", 23: "c", 24: "d",
        # 25: obert (2 pts)
        26: "c", 27: "d", 28: "c", 29: "b", 30: "a", 31: "a"
    },

    # ── 4t d'ESO Ciència i Tecnologia 2023 ─────────────────────────────────
    ("4ESO", "CTE", 2023): {
        1: "c", 2: "b", 3: "d", 4: "c", 5: "a",
        # 6: obert (1 pt)
        7: "b", 8: "a",
        # 9: taula V/F
        91: "b", 92: "a", 93: "a",
        10: "b", 11: "c", 12: "d", 13: "c",
        14: "a", 15: "d", 16: "b", 17: "c", 18: "a",
        19: "b", 20: "c",
        # 21: taula V/F piles/bateries
        211: "a", 212: "a", 213: "a", 214: "a", 215: "b", 216: "a",
        22: "b", 23: "d", 24: "c"
        # 25: obert (1 pt)
    },

    # ── 4t d'ESO Ciència i Tecnologia 2022 ─────────────────────────────────
    ("4ESO", "CTE", 2022): {
        1: "c", 2: "a",
        # 3: obert (1 pt)
        4: "b", 5: "d", 6: "a", 7: "b",
        # 8: taula relació
        81: "d", 82: "b", 83: "c",
        9: "a", 10: "c", 11: "d", 12: "b", 13: "a",
        14: "c", 15: "b", 16: "d",
        # 17: taula V/F teories científiques
        171: "b", 172: "a", 173: "a",
        18: "a",
        # 19: obert (1 pt)
        20: "b", 21: "c", 22: "a", 23: "c", 24: "d", 25: "b"
    },

    # ── 4t d'ESO Ciència i Tecnologia 2021 ─────────────────────────────────
    ("4ESO", "CTE", 2021): {
        1: "b", 2: "d", 3: "a", 4: "c", 5: "a",
        # 6: taula Sí/No crispetes
        61: "b", 62: "a", 63: "a", 64: "a", 65: "a", 66: "b",
        7: "c", 8: "a", 9: "d",
        # 10: obert (1 pt)
        # 11: taula Sí/No aigua potable
        111: "a", 112: "b", 113: "a", 114: "b",
        12: "c",
        # 13: obert (1 pt)
        14: "d", 15: "b", 16: "a", 17: "c", 18: "d", 19: "a",
        20: "b", 21: "c", 22: "a", 23: "d", 24: "b", 25: "c"
    }
}

# ---------------------------------------------------------------------------
# ESTRUCTURES OFICIALS (STRUCTURES)
# ---------------------------------------------------------------------------
STRUCTURES_HISTORICS = {
    # ── 4t d'ESO Matemàtiques 2023 ─────────────────────────────────────────
    ("4ESO", "MAT", 2023): {
        "title": "4t d’ESO · Competència matemàtica 2023 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2023_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2022-2023)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 31 preguntes (35 punts en total: 27 ítems de test i 4 ítems de resposta oberta).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2023_prova.pdf",
        "crops_dir": "scratch/crops_4eso_mat_2023_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Internet al món", "desc": "Ítems de l'1 al 4. Situació: població mundial, connexió a Internet i telefonia mòbil."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Població i connexió a Internet arreu del món"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},

            {"kind": "section", "title": "Activitat 2. Fitxes", "desc": "Ítems del 5 a l'11. Situació: patrons visuals, creixement de figures i llenguatge algebraic."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: Figures amb fitxes"},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "image", "file": "context_act2_intro_p5.png", "title": "Context: Taula del nombre total de fitxes necessàries"},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "open_item", "num": 11, "label": "Pregunta 11 (Resposta oberta · 2 punts)", "points": 2, "desc": "Escriu la teva resolució raonada, els càlculs i quantes figures es poden construir i quantes fitxes sobren."},

            {"kind": "section", "title": "Activitat 3. Daus", "desc": "Ítems del 12 al 17. Situació: estadística de llançaments de daus, probabilitat i desplegament d'un cub."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Daus de 8, 10 i 12 cares"},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "image", "file": "context_act3_intro_p7.png", "title": "Context: Construcció de daus i desplegament pla"},
            {"kind": "item", "num": 16},
            {"kind": "open_item", "num": 17, "label": "Pregunta 17 (Resposta oberta · 2 punts)", "points": 2, "desc": "Escriu com s'han de distribuir els números en les 6 cares del desplegament del dau i justifica-ho amb càlculs."},

            {"kind": "section", "title": "Activitat 4. Fulls de paper DIN", "desc": "Ítems del 18 al 21. Situació: proporcions de la sèrie DIN, superfícies i relacions mètriques."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Format i relacions de mides dels fulls DIN"},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "open_item", "num": 21, "label": "Pregunta 21 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula la longitud del segment recte més llarg en un full DIN A2 justificant-ho amb els càlculs (Pitàgores)."},

            {"kind": "section", "title": "Activitat 5. Impressió de fotografies", "desc": "Ítems del 22 al 28. Situació: tarifes d'impressió, descomptes, sistemes d'equacions i marcs de fusta."},
            {"kind": "image", "file": "context_act5_intro.png", "title": "Context Activitat 5: Tarifes d'impressió de fotografies"},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25},
            {"kind": "image", "file": "context_act5_intro_p10.png", "title": "Context: Impressió domèstica i proporcions"},
            {"kind": "item", "num": 26},
            {"kind": "item", "num": 27},
            {"kind": "open_item", "num": 28, "label": "Pregunta 28 (Resposta oberta · 2 punts)", "points": 2, "desc": "Digues si l'afirmació de l'Anna és certa o falsa i justifica-ho comparant el preu per full de cada paquet."},

            {"kind": "section", "title": "Activitat 6. Errors de mesura", "desc": "Ítems del 29 al 31. Situació: mesurament amb regle graduat, interval d'incertesa i error acumulat."},
            {"kind": "image", "file": "context_act6_intro.png", "title": "Context Activitat 6: Errors i toleràncies en el mesurament"},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
            {"kind": "item", "num": 31}
        ]
    },

    # ── 4t d'ESO Matemàtiques 2022 ─────────────────────────────────────────
    ("4ESO", "MAT", 2022): {
        "title": "4t d’ESO · Competència matemàtica 2022 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2022_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2021-2022)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 31 preguntes (35 punts en total: 27 ítems de test i 4 ítems de resposta oberta).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2022_prova.pdf",
        "crops_dir": "scratch/crops_4eso_mat_2022_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Les rajoles", "desc": "Ítems de l'1 al 6. Situació: geometria de rajoles, àrees, optimització de compra i girs."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Rajoles quadrades i quadrat interior"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "open_item", "num": 4, "label": "Pregunta 4 (Resposta oberta · 2 punts)", "points": 2, "desc": "Escriu la combinació més econòmica de paquets per comprar almenys 342 rajoles i justifica-la amb càlculs."},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},

            {"kind": "section", "title": "Activitat 2. Objectes cilíndrics", "desc": "Ítems del 7 al 10. Situació: comparació de gots i envasos cilíndrics, volums i desenvolupament pla."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: Got de vidre i envàs de iogurt"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "open_item", "num": 10, "label": "Pregunta 10 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula l'alçada i amplada del paral·lelogram (incloent la pestanya de 2 cm) justificant la resposta."},

            {"kind": "section", "title": "Activitat 3. La memòria del mòbil", "desc": "Ítems de l'11 al 13. Situació: gestió d'emmagatzematge, sectors circulars i mitjanes de fitxers."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Capacitat i emmagatzematge del telèfon mòbil"},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},

            {"kind": "section", "title": "Activitat 4. El joc de construcció", "desc": "Ítems del 14 al 17. Situació: peces encaixables, probabilitat, successions de pisos i botons visibles."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Torre de 4 pisos amb peces encaixables"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "open_item", "num": 16, "label": "Pregunta 16 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula quants botons visibles hi hauria en el pis inferior d'una torre de 5 pisos i explica el procediment."},
            {"kind": "item", "num": 17},

            {"kind": "section", "title": "Activitat 5. Juguem a bàsquet", "desc": "Ítems del 18 al 25. Situació: estadística de tirs a cistella, gràfic temporal d'un partit i sistemes d'equacions."},
            {"kind": "image", "file": "context_act5_intro.png", "title": "Context Activitat 5: Tandes de llançaments a cistella"},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},
            {"kind": "open_item", "num": 20, "label": "Pregunta 20 (Resposta oberta · 2 punts)", "points": 2, "desc": "Compara els resultats de la Carla i la Lucía calculant la mitjana de cistelles per tanda de cadascuna."},
            {"kind": "image", "file": "context_act5_intro_p8.png", "title": "Context: Gràfic de diferència de puntuació durant el partit"},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25},

            {"kind": "section", "title": "Activitat 6. El projecte de l'aigua", "desc": "Ítems del 26 al 31. Situació: consum domèstic, fuites per degoteig i taxa d'evaporació física."},
            {"kind": "image", "file": "context_act6_intro.png", "title": "Context Activitat 6: Mesura del cabal d'aixetes i airejadors"},
            {"kind": "item", "num": 26},
            {"kind": "item", "num": 27},
            {"kind": "item", "num": 28},
            {"kind": "image", "file": "context_act6_intro_p11.png", "title": "Context: Gràfic d'evaporació d'aigua en interior i exterior"},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
            {"kind": "item", "num": 31}
        ]
    },

    # ── 4t d'ESO Matemàtiques 2021 ─────────────────────────────────────────
    ("4ESO", "MAT", 2021): {
        "title": "4t d’ESO · Competència matemàtica 2021 · Prova oficial CB",
        "docTitle": "4ESO-MAT_CB-2021_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència matemàtica (Curs 2020-2021)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 31 preguntes (35 punts en total: 27 ítems de test i 4 ítems de resposta oberta).",
        "target_folder": "4ESO_MAT",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/matematiques/4ESO_CB_2021_prova.pdf",
        "crops_dir": "scratch/crops_4eso_mat_2021_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Atletisme", "desc": "Ítems de l'1 al 7. Situació: pista d'atletisme, perímetres, llançament de disc i fossat de sorra."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Pista d'atletisme i dimensions"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "image", "file": "context_act1_intro_p3.png", "title": "Context: Llançament de disc"},
            {"kind": "item", "num": 4},
            {"kind": "item", "num": 5},
            {"kind": "open_item", "num": 6, "label": "Pregunta 6 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula el cost d'omplir el fossat de sorra justificant la resposta amb els càlculs de volum i preu."},
            {"kind": "item", "num": 7},

            {"kind": "section", "title": "Activitat 2. Artesania a la xarxa", "desc": "Ítems del 8 a l'11. Situació: venda de ninots de fusta, embalatge, mitjana de comandes i tarifes d'enviament."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: Venda de ninots de fusta per Internet"},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "open_item", "num": 11, "label": "Pregunta 11 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula la quantitat fixa per enviament i el cost per quilogram a partir del gràfic."},

            {"kind": "section", "title": "Activitat 3. Escacs", "desc": "Ítems del 12 al 17. Situació: estadístiques de partides de Magnus Carlsen, sectors circulars i gràfic d'evolució de punts."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Resultats oficials de partides d'escacs"},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},
            {"kind": "open_item", "num": 14, "label": "Pregunta 14 (Resposta oberta · 2 punts)", "points": 2, "desc": "Raona si el sector de victòries mesurarà més de 180º justificant-ho amb càlculs."},
            {"kind": "image", "file": "context_act3_intro_p7.png", "title": "Context: Puntuació acumulada en un torneig"},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},

            {"kind": "section", "title": "Activitat 4. El joc de bitlles", "desc": "Ítems del 18 al 21. Situació: tria a l'atzar, successió triangular de bitlles i relació de pes corporal."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Disposició i joc de bitlles"},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},

            {"kind": "section", "title": "Activitat 5. Producció i preu", "desc": "Ítems del 22 al 25. Situació: evolució de la producció mensual, preus unitaris i notació científica."},
            {"kind": "image", "file": "context_act5_intro.png", "title": "Context Activitat 5: Gràfics de producció i preu"},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "open_item", "num": 25, "label": "Pregunta 25 (Resposta oberta · 2 punts)", "points": 2, "desc": "Calcula el preu mínim per unitat al maig perquè els ingressos no siguin inferiors als de l'abril."},

            {"kind": "section", "title": "Activitat 6. Màgia", "desc": "Ítems del 26 al 31. Situació: plecs d'un bitllet, potències de dos, probabilitat amb baralles de cartes i teorema de Pitàgores."},
            {"kind": "image", "file": "context_act6_intro.png", "title": "Context Activitat 6: Trucs de màgia i bitllets plegats"},
            {"kind": "item", "num": 26},
            {"kind": "item", "num": 27},
            {"kind": "item", "num": 28},
            {"kind": "item", "num": 29},
            {"kind": "item", "num": 30},
            {"kind": "item", "num": 31}
        ]
    },

    # ── 4t d'ESO Ciència i Tecnologia 2023 ─────────────────────────────────
    ("4ESO", "CTE", 2023): {
        "title": "4t d’ESO · Competència cientificotecnològica 2023 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2023_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència cientificotecnològica (Curs 2022-2023)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 25 preguntes amb subapartats de vertader/fals i preguntes obertes (total 33 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2023_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2023_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Leds i salut", "desc": "Ítems de l'1 al 6. Situació: il·luminació led, espectre electromagnètic, ritme circadiari i hemograma."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Tecnologia led i emissions de llum"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "item", "num": 5},
            {"kind": "open_item", "num": 6, "label": "Pregunta 6 (Resposta oberta · 1 punt)", "points": 1, "desc": "Interpreta els resultats de l'anàlisi de sang (hemoglobina, hematies, hematòcrit) i argumenta si cal visitar el centre mèdic."},

            {"kind": "section", "title": "Activitat 2. Tornem a la Lluna", "desc": "Ítems del 7 al 13. Situació: exploració lunar, gravetat, experiment de caiguda de cossos i òrbites."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: El programa lunar i la missió Artemis"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 91, "img_file": "item_9.png", "label": "Pregunta 9.1: Martell i ploma van quedar flotant sense caure per manca total de gravetat", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 92, "img_file": "item_9.png", "label": "Pregunta 9.2: Martell i ploma van caure més lentament que a la Terra per la menor gravetat", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 93, "img_file": "item_9.png", "label": "Pregunta 9.3: Martell i ploma van arribar alhora en no haver-hi fregament d'aire", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},

            {"kind": "section", "title": "Activitat 3. L'acidificació dels oceans", "desc": "Ítems del 14 al 18. Situació: absorció de CO2, escala de pH, calcificació marina i cadenes tròfiques."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Impacte del canvi climàtic i acidificació marina"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "item", "num": 18},

            {"kind": "section", "title": "Activitat 4. Piles i bateries", "desc": "Ítems del 19 al 25. Situació: electroquímica, piles primàries i acumuladors, i gestió mediambiental."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Funcionament de piles i acumuladors"},
            {"kind": "item", "num": 19},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 211, "img_file": "item_21.png", "label": "Pregunta 21.1: Piles tenen dos elèctrodes (ànode i càtode)", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 212, "img_file": "item_21.png", "label": "Pregunta 21.2: Bateries tenen dos elèctrodes (ànode i càtode)", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 213, "img_file": "item_21.png", "label": "Pregunta 21.3: Piles funcionen per reacció química entre dues substàncies", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 214, "img_file": "item_21.png", "label": "Pregunta 21.4: Bateries funcionen per reacció química entre dues substàncies", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 215, "img_file": "item_21.png", "label": "Pregunta 21.5: Piles (no recarregables) emmagatzemen càrrega d'un altre generador", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 216, "img_file": "item_21.png", "label": "Pregunta 21.6: Bateries (recarregables) emmagatzemen càrrega d'un altre generador", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "open_item", "num": 25, "label": "Pregunta 25 (Resposta oberta · 1 punt)", "points": 1, "desc": "Descriu almenys dos avantatges associats a una correcta gestió i reciclatge de les piles usades."}
        ]
    },

    # ── 4t d'ESO Ciència i Tecnologia 2022 ─────────────────────────────────
    ("4ESO", "CTE", 2022): {
        "title": "4t d’ESO · Competència cientificotecnològica 2022 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2022_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència cientificotecnològica (Curs 2021-2022)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 25 preguntes amb subapartats de vertader/fals i preguntes obertes (total 30 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2022_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2022_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Un mar de plàstics", "desc": "Ítems de l'1 al 8. Situació: contaminació per microplàstics, bioacumulació tròfica i identificació de polímers."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Microplàstics en els ecosistemes marins"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "open_item", "num": 3, "label": "Pregunta 3 (Resposta oberta · 1 punt)", "points": 1, "desc": "Explica per què les autoritats recomanen no consumir peixos grans massa sovint relacionant microplàstics, acumulació i transferència tròfica."},
            {"kind": "item", "num": 4},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 6},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 81, "img_file": "item_8.png", "label": "Pregunta 8.1: Mostra A de plàstic (flota a l'aigua i crema gairebé sense fum)", "options": ["a", "b", "c", "d"], "opt_labels": ["a. 1 PP", "b. 2 PVC", "c. 3 ABS", "d. 4 PEBD"]},
            {"kind": "item", "num": 82, "img_file": "item_8.png", "label": "Pregunta 8.2: Mostra B de plàstic (s'enfonsa a l'aigua i crema amb fum negre)", "options": ["a", "b", "c", "d"], "opt_labels": ["a. 1 PP", "b. 2 PVC", "c. 3 ABS", "d. 4 PEBD"]},
            {"kind": "item", "num": 83, "img_file": "item_8.png", "label": "Pregunta 8.3: Mostra C de plàstic (flota a l'aigua i crema amb fum negre)", "options": ["a", "b", "c", "d"], "opt_labels": ["a. 1 PP", "b. 2 PVC", "c. 3 ABS", "d. 4 PEBD"]},

            {"kind": "section", "title": "Activitat 2. Els secrets ocults dels ibers", "desc": "Ítems del 9 al 13. Situació: mètodes geofísics, prospecció electromagnètica, ceràmica i arqueometria."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: Jaciment arqueològic i prospecció científica"},
            {"kind": "item", "num": 9},
            {"kind": "item", "num": 10},
            {"kind": "item", "num": 11},
            {"kind": "item", "num": 12},
            {"kind": "item", "num": 13},

            {"kind": "section", "title": "Activitat 3. Alerta: tsunami!", "desc": "Ítems del 14 al 18. Situació: ones sísmiques, velocitat de propagació, tectònica de plaques i mètode científic."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Generació i propagació de tsunamis"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 171, "img_file": "item_17.png", "label": "Pregunta 17.1: Les teories científiques són immutables, no canvien mai", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 172, "img_file": "item_17.png", "label": "Pregunta 17.2: Les teories científiques es fonamenten en experiments i observacions", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 173, "img_file": "item_17.png", "label": "Pregunta 17.3: Les teories científiques són revisades en descobrir noves evidències", "options": ["a", "b"], "opt_labels": ["a. Vertader", "b. Fals"]},
            {"kind": "item", "num": 18},

            {"kind": "section", "title": "Activitat 4. Protegim-nos del Sol", "desc": "Ítems del 19 al 25. Situació: radiacions ultraviolades (UVA, UVB, UVC), capa d'ozó, fotoprotecció i salut de la pell."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Radiació solar i efectes sobre la salut"},
            {"kind": "open_item", "num": 19, "label": "Pregunta 19 (Resposta oberta · 1 punt)", "points": 1, "desc": "Explica per què al mercat no hi ha cremes solars contra les radiacions UVC tenint en compte el paper de la capa d'ozó."},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25}
        ]
    },

    # ── 4t d'ESO Ciència i Tecnologia 2021 ─────────────────────────────────
    ("4ESO", "CTE", 2021): {
        "title": "4t d’ESO · Competència cientificotecnològica 2021 · Prova oficial CB",
        "docTitle": "4ESO-CTE_CB-2021_prova-autocorregible",
        "desc_header": "Avaluació de final d’etapa — Competència cientificotecnològica (Curs 2020-2021)\nInstitut Escola Sant Pol de Mar\n\nProva oficial de 25 preguntes amb subapartats de vertader/fals i preguntes obertes (total 33 punts).",
        "target_folder": "4ESO_CTE",
        "pdf_path": "docencia/materials/competencies_basiques/4ESO/ciencia_tecnologia/4ESO_CB_2021_CTE_prova.pdf",
        "crops_dir": "scratch/crops_4eso_cte_2021_clean",
        "elements": [
            {"kind": "section", "title": "Activitat 1. Les crispetes", "desc": "Ítems de l'1 al 6. Situació: gra de blat de moro, canvis d'estat de la matèria, pressió de vapor i biopolímers sostenibles."},
            {"kind": "image", "file": "context_act1_intro.png", "title": "Context Activitat 1: Estructura del gra de blat de moro i esclat"},
            {"kind": "item", "num": 1},
            {"kind": "item", "num": 2},
            {"kind": "item", "num": 3},
            {"kind": "item", "num": 4},
            {"kind": "item", "num": 5},
            {"kind": "item", "num": 61, "img_file": "item_6.png", "label": "Pregunta 6.1: El porexpan és biodegradable", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 62, "img_file": "item_6.png", "label": "Pregunta 6.2: La crispeta és biodegradable", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 63, "img_file": "item_6.png", "label": "Pregunta 6.3: El porexpan és un material lleuger", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 64, "img_file": "item_6.png", "label": "Pregunta 6.4: La crispeta és un material lleuger", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 65, "img_file": "item_6.png", "label": "Pregunta 6.5: El porexpan és un material sintètic de la família dels polímers", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 66, "img_file": "item_6.png", "label": "Pregunta 6.6: La crispeta és un material sintètic de la família dels polímers", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},

            {"kind": "section", "title": "Activitat 2. L'aigua, una substància molt especial", "desc": "Ítems del 7 al 13. Situació: estructura molecular de l'H2O, anomalia tèrmica, potabilització i dissolució de gasos."},
            {"kind": "image", "file": "context_act2_intro.png", "title": "Context Activitat 2: Propietats fisicoquímiques de l'aigua"},
            {"kind": "item", "num": 7},
            {"kind": "item", "num": 8},
            {"kind": "item", "num": 9},
            {"kind": "open_item", "num": 10, "label": "Pregunta 10 (Resposta oberta · 1 punt)", "points": 1, "desc": "Explica la diferència de densitat entre el gel i l'aigua líquida a partir de l'estructura molecular i els ponts d'hidrogen."},
            {"kind": "item", "num": 111, "img_file": "item_11.png", "label": "Pregunta 11.1: L'aigua potable ha d'estar lliure de virus, bacteris i partícules sòlides", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 112, "img_file": "item_11.png", "label": "Pregunta 11.2: L'aigua potable ha de contenir una alta concentració de clor", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 113, "img_file": "item_11.png", "label": "Pregunta 11.3: L'aigua potable ha d'estar lliure de substàncies tòxiques", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 114, "img_file": "item_11.png", "label": "Pregunta 11.4: L'aigua potable ha d'estar lliure de sals minerals", "options": ["a", "b"], "opt_labels": ["a. Sí", "b. No"]},
            {"kind": "item", "num": 12},
            {"kind": "open_item", "num": 13, "label": "Pregunta 13 (Resposta oberta · 1 punt)", "points": 1, "desc": "Explica la relació entre la temperatura de l'aigua i la quantitat de gas dissolt (solubilitat)."},

            {"kind": "section", "title": "Activitat 3. Producció i conservació d'aliments", "desc": "Ítems del 14 al 19. Situació: tècniques de conservació d'aliments, pasteurització, liofilització i caducitat."},
            {"kind": "image", "file": "context_act3_intro.png", "title": "Context Activitat 3: Conservació i tractament tèrmic d'aliments"},
            {"kind": "item", "num": 14},
            {"kind": "item", "num": 15},
            {"kind": "item", "num": 16},
            {"kind": "item", "num": 17},
            {"kind": "item", "num": 18},
            {"kind": "item", "num": 19},

            {"kind": "section", "title": "Activitat 4. Els ferrocarrils", "desc": "Ítems del 20 al 25. Situació: tracció ferroviària, catenària, transformadors de tensió, energia cinètica i seguretat."},
            {"kind": "image", "file": "context_act4_intro.png", "title": "Context Activitat 4: Tecnologia i electrificació ferroviària"},
            {"kind": "item", "num": 20},
            {"kind": "item", "num": 21},
            {"kind": "item", "num": 22},
            {"kind": "item", "num": 23},
            {"kind": "item", "num": 24},
            {"kind": "item", "num": 25}
        ]
    }
}
