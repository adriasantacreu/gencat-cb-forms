# Scripts històrics i de desenvolupament (Setembre 2025)

Aquest directori aplega els scripts d'un sol ús utilitzats durant la campanya inicial de descàrrega, retall i creació de formularis de Competències Bàsiques (2ESO i 4ESO) de la Generalitat de Catalunya:

- `crea_formulari_cb.py` / `cb`: Generador principal de Google Forms a partir de proves CB.
- `crea_formulari_4eso_2025.py`: Generador específic per a la prova de 4t d'ESO de 2025.
- `descarrega_cb.py`: Descàrrega directa de quaderns i criteris d'avaluació oficials.
- `audita_cb.py`: Comprovació de marcs, marges i imatges retallades.
- `clona_cb_drive_personal.py`: Còpia de formularis cap a Google Drive personal.
- `config_cb_historics.py`: Taules de configuració de proves històriques anteriors.
- `automatitza_cb_2eso_cte_complet.py`: Pipeline complet per a Ciències i Tecnologia de 2n d'ESO.
- `genera_crops_2eso_cte.py` / `genera_crops_cte_perfecte.py`: Retall automàtic d'imatges d'enunciats.
- `genera_visor_claus.py`: Generador de visor web per auditar les respostes correctes.
- `retalla_cb_perfecte.py`: Algorisme de tight-crop sobre pàgines PDF.
- `tallador_automatic.py`: Segmentador de figures i enunciats.

Si es reprèn la feina del projecte, el codi canònic i net viu a `src/` d'aquest repositori (`gencat-cb-forms`).
