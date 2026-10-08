# Paper archive guidance

This directory is the single entry point for source papers of the touch/somatosensation restoration
collection. Naming follows the `yyyymmdd_<author>` convention (same style as the speech neuroprosthesis
archive): one folder per paper, lowercase, digits + letters + underscores only. The date is the paper's
publication date (journal issue date for Nature/Science family weeklies, published-online date for
Nat Commun/Nat BME/J Neuroeng Rehabil/eLife, epub date for Elsevier/IOP/IEEE journals, preprint
posting date for medRxiv). Each folder contains the main article named after the folder
(`<folder>.pdf`), plus supplementary PDFs named `<folder>_supplement.pdf` where available.

All PDFs were collected by ZCode on 2026-09-18. Sources: publisher-direct (nature.com, medRxiv,
DuckDuckGo-hosted lab copies), PMC author manuscripts (downloaded through a real browser session
because scripted PMC access is bot-blocked), and one lab-hosted copy (motorlab.pitt.edu for Flesher
2016). Every PDF was verified with pypdf (page count + EOF marker) after download; a text cache
lives under `../paper_text/` (run `python tools/build_text_cache.py` to refresh).

Per-paper folders (chronologically ordered):

- `19980326_romo/` — Romo 1998 (Nature): **no local PDF** (paywalled; no legal open copy found on
  2026-09-18). Entry kept in the notes catalogue because it is the founding ICMS paper. DOI 10.1038/32891.
- `20111005_odoherty/` — O'Doherty 2011 (Nature): first brain-machine-brain interface (NHP).
- `20131105_tabot/` — Tabot 2013 (PNAS): NHP behavioral detection/location of ICMS as touch.
- `20151208_kim/` — Kim 2015 (PNAS): systematic psychophysical assessment of ICMS sensitivity (NHP).
- `20161019_flesher/` — Flesher 2016 (Sci Transl Med): first human ICMS touch restoration; lab copy
  from motorlab.pitt.edu (11-page author version).
- `20171125_wendelken/` — Wendelken 2017 (J Neuroeng Rehabil): USEA peripheral-nerve route, 2 amputees.
- `20180410_armenta_salas/` — Armenta Salas 2018 (eLife): Caltech line, cutaneous + proprioceptive
  percepts (participant FG).
- `20210521_flesher/` — Flesher 2021 (Science): ICMS feedback halves robotic-arm task time;
  `20210521_flesher_supplement.pdf` included.
- `20210617_simeral/` — Simeral 2021 (IEEE TBME): first human wireless broadband iBCI (T5, T10).
- `20210727_hughes/` — Hughes 2021 (eLife): frequency-perception groups (P2, P3); open data/code.
- `20210813_hughes/` — Hughes 2021 (J Neural Eng): stimulation/recording stability over 1500 days.
- `20220215_fifer/` — Fifer 2022 (Neurology): JHU APL line clinical note, 96 electrodes, both hands.
- `20220604_hughes/` — Hughes 2022 (Brain Stimul): percept adaptation to continuous ICMS.
- `20231110_shelchkova/` — Shelchkova 2023 (Nat Commun): S1 ICMS responses in motor cortex (C1, P2, P3).
- `20231214_nanivadekar/` — Nanivadekar 2023/2024 (Nat Biomed Eng): closed-loop SCS foot feedback +
  phantom-limb-pain relief, 3 transtibial amputees.
- `20240520_moritz/` — Moritz 2024 (Nat Med): ARC-EX noninvasive cervical SCS pivotal trial.
- `20241206_greenspon/` — Greenspon 2024 (Nat Biomed Eng): stable & precise multi-electrode ICMS.
- `20241215_downey/` — Downey 2024 (Hum Brain Mapp): presurgical mapping/implantation roadmap, 5
  participants across two sites.
- `20250117_valle/` — Valle 2025 (Science): tactile edges and motion via patterned ICMS (C1, C2).
- `20250410_osborn/` — Osborn 2025 (Brain Stimul): subthreshold ICMS enhances tactile sensitivity.
- `20250501_verbaarschot/` — Verbaarschot 2025 (Nat Commun): participant-customized ICMS conveying
  object characteristics (P2, P3, C1).
- `20250514_hobbs/` — Hobbs 2025 (J Neural Eng): biomimetic patterns feel more natural (C1, P2, P3).
- `20250514_smith/` — Smith 2025 (Front Neurosci): spatial limits of ICMS discrimination in rats.
- `20250722_ren/` — Ren 2025 (Cyborg Bionic Syst): epidural EES + PT in incomplete SCI (11 patients),
  sensory-function outcomes.
- `20250811_greenspon/` — Greenspon 2025 (medRxiv preprint) = "ICMS in humans: a decade of safety and
  efficacy"; published as Sci Transl Med 2026-07-15 (DOI 10.1126/scitranslmed.aec3728, paywalled).
  Five participants, 2-10 year implants, 24 cumulative implant-years, >168M stimuli.

General rules:

- Participant codes differ per team and are NOT a shared numbering system: `P2/P3` = Pittsburgh
  BrainGate2 touch-study participants (P2 is the participant of Flesher 2016/2021); `C1/C2` =
  Chicago-site participants in the same collaboration; `FG` = Caltech participant; the JHU APL line
  reports one unnamed participant; `T5/T10` are BrainGate consortium numbers (speech/typing line
  uses the same T-system). Do not sum participants across papers.
- Berg 2013 (IEEE TNSRE, "Behavioral demonstration of a somatosensory neuroprosthesis") is NOT
  archived: no legal open copy was found on 2026-09-18 and its content is covered by Kim 2015.
- New papers go into a new `yyyymmdd_<author>` folder and must be added to the notes catalogue
  (`../notes/20260918_somatosensory_neuroprosthesis_all_papers_collected_by_zcode.html`), then
  regenerate its machine-readable companion
  `../notes/20260918_somatosensory_neuroprosthesis_catalogue.json` by editing the note's
  embedded `#papers-data` JSON block and running `python tools/build_note_catalogue.py`.
- Verify important claims against the rendered PDF page; the text cache under `../paper_text/` may
  have reading-order or character errors.
