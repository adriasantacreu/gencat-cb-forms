#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un panell visual HTML d'auditoria de claus de correcció.
Mostra cara a cara la captura original de la clau del Departament i la llista de solucions
assignades al Google Forms per a cadascun dels 9 exàmens.
"""

import base64
from pathlib import Path
import sys

# Importem ANSWERS de crea_formulari_cb
sys.path.insert(0, str(Path(__file__).resolve().parent))
from crea_formulari_cb import ANSWERS

EXAMS = [
    {
        "id": "4eso_mat_2026",
        "titol": "4t ESO · Matemàtiques 2026",
        "key": ("4ESO", "MAT", 2026),
        "img": "scratch/claus_modernes/4ESO_CB_2026_criteris_pag8.png"
    },
    {
        "id": "4eso_mat_2025",
        "titol": "4t ESO · Matemàtiques 2025",
        "key": ("4ESO", "MAT", 2025),
        "img": "scratch/clau_2025.png"
    },
    {
        "id": "4eso_mat_2024",
        "titol": "4t ESO · Matemàtiques 2024",
        "key": ("4ESO", "MAT", 2024),
        "img": "scratch/claus_modernes/4ESO_CB_2024_criteris_pag8.png"
    },
    {
        "id": "2eso_mat_2026",
        "titol": "2n ESO · Matemàtiques 2026",
        "key": ("2ESO", "MAT", 2026),
        "img": "scratch/claus_modernes/2ESO_AD_2026_criteris_pag5.png"
    },
    {
        "id": "2eso_mat_2025",
        "titol": "2n ESO · Matemàtiques 2025",
        "key": ("2ESO", "MAT", 2025),
        "img": "scratch/claus_modernes/2ESO_AD_2025_criteris_pag9.png"
    },
    {
        "id": "2eso_mat_2024",
        "titol": "2n ESO · Matemàtiques 2024",
        "key": ("2ESO", "MAT", 2024),
        "img": "scratch/claus_modernes/2ESO_AD_2024_criteris_pag6.png"
    },
    {
        "id": "4eso_cte_2026",
        "titol": "4t ESO · Ciència i Tecnologia 2026",
        "key": ("4ESO", "CTE", 2026),
        "img": "scratch/claus_modernes/4ESO_CB_2026_CTE_criteris_pag8.png"
    },
    {
        "id": "4eso_cte_2025",
        "titol": "4t ESO · Ciència i Tecnologia 2025",
        "key": ("4ESO", "CTE", 2025),
        "img": "scratch/claus_modernes/4ESO_CB_2025_CTE_criteris_pag6.png"
    },
    {
        "id": "4eso_cte_2024",
        "titol": "4t ESO · Ciència i Tecnologia 2024",
        "key": ("4ESO", "CTE", 2024),
        "img": "scratch/claus_modernes/4ESO_CB_2024_CTE_criteris_pag6.png"
    },
]

def img_to_b64(path_str):
    p = Path(path_str)
    if not p.exists():
        return ""
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

html = """<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>Auditoria Visual de Claus de Correcció — CB i AD</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }
  h1 { font-size: 24px; margin-bottom: 8px; color: #38bdf8; }
  p.sub { color: #94a3b8; margin-top: 0; margin-bottom: 24px; font-size: 14px; }
  .exam-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; margin-bottom: 32px; overflow: hidden; }
  .exam-header { background: #0f172a; padding: 12px 20px; font-weight: 600; font-size: 16px; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }
  .badge { background: #0284c7; color: white; padding: 3px 8px; border-radius: 6px; font-size: 12px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; }
  .side { background: #0f172a; border-radius: 8px; padding: 16px; border: 1px solid #1e293b; }
  .side h3 { font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; color: #38bdf8; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 8px; }
  img.key-img { width: 100%; border-radius: 6px; background: white; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4)); }
  .answers-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 13px; }
  .answers-table th, .answers-table td { padding: 6px 10px; border-bottom: 1px solid #334155; text-align: left; }
  .answers-table th { color: #94a3b8; font-weight: 500; }
  .ans-badge { background: #10b981; color: #022c22; font-weight: bold; padding: 2px 8px; border-radius: 4px; display: inline-block; }
  .ans-sub { background: #f59e0b; color: #451a03; }
</style>
</head>
<body>
<h1>Auditoria Visual de Solucions Oficials vs. Google Forms</h1>
<p class="sub">Verificació creuada: Pauta oficial de la Generalitat (esquerra) vs. Solucions injectades a l'API de Google Forms (dreta).</p>
"""

for exam in EXAMS:
    answers_dict = ANSWERS.get(exam["key"], {})
    b64_img = img_to_b64(exam["img"])
    
    table_rows = []
    # Ordenar claus
    def sort_key(k):
        if isinstance(k, int):
            return (k, 0)
        s = str(k)
        if "_" in s:
            p = s.split("_")
            try:
                return (int(p[0]), int(p[1]))
            except:
                return (999, s)
        try:
            return (int(s), 0)
        except:
            return (999, s)

    sorted_keys = sorted(answers_dict.keys(), key=sort_key)
    
    # Crear files de 2 columnes per aprofitar espai
    half = (len(sorted_keys) + 1) // 2
    col1 = sorted_keys[:half]
    col2 = sorted_keys[half:]
    
    for i in range(half):
        k1 = col1[i] if i < len(col1) else ""
        v1 = answers_dict.get(k1, "") if k1 != "" else ""
        k2 = col2[i] if i < len(col2) else ""
        v2 = answers_dict.get(k2, "") if k2 != "" else ""
        
        b1_class = "ans-sub" if "_" in str(k1) else "ans-badge"
        b2_class = "ans-sub" if "_" in str(k2) else "ans-badge"
        
        v1_html = f'<span class="{b1_class}">{v1}</span>' if v1 else ""
        v2_html = f'<span class="{b2_class}">{v2}</span>' if v2 else ""
        
        table_rows.append(f"""
        <tr>
            <td><strong>Ítem {k1}</strong></td><td>{v1_html}</td>
            <td><strong>Ítem {k2}</strong></td><td>{v2_html}</td>
        </tr>
        """)
        
    rows_html = "".join(table_rows)

    html += f"""
    <div class="exam-card" id="{exam['id']}">
      <div class="exam-header">
        <span>{exam['titol']}</span>
        <span class="badge">{len(answers_dict)} ítems avaluats</span>
      </div>
      <div class="grid">
        <div class="side">
          <h3>Pauta Oficial (Generalitat de Catalunya)</h3>
          <img class="key-img" src="{b64_img}" alt="Clau oficial">
        </div>
        <div class="side">
          <h3>Solucions Injectades al Formulari (Google Forms)</h3>
          <table class="answers-table">
            <thead>
              <tr><th>Ítem</th><th>Solució</th><th>Ítem</th><th>Solució</th></tr>
            </thead>
            <tbody>
              {rows_html}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    """

html += """
</body>
</html>
"""

out_file = Path("scratch/auditoria_claus_cb.html")
out_file.write_text(html, encoding="utf-8")
print(f"✓ Panell d'auditoria visual generat amb èxit a: {out_file} ({out_file.stat().st_size // 1024} KB)")
