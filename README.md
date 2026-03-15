# chaoss

Public datasets and community resources for *Finding Order in CHAOSS: A Survey of Open-Source Spiking Neural Network Software Simulators*.

## Repository Contents

### Simulator Worksheet

The primary community artifact: a scored feature matrix covering 45 open-source SNN simulators.

| File | Description |
|------|-------------|
| `simulator-notes/simulator-worksheet.tex` | Main worksheet LaTeX source |
| `simulator-notes/simulator_selection_worksheet.tex` | Selection criteria worksheet |
| `simulator-notes/simulator-notes.tex` | Per-simulator research notes (evidence behind feature matrix entries) |
| `simulator-notes/simulator-worksheet.pdf` | Compiled PDF (primary read format) |
| `simulator-notes/html/simulator-worksheet.html` | HTML version (hyperlinked, browser-filterable) |
| `simulator-notes/html/simulator-worksheet.css` | Stylesheet for HTML version |
| `simulator-notes/generate_table.py` | Python script that builds the HTML from source data |
| `simulator-notes/Makefile` | Build targets for PDF and HTML |

### Machine-Readable Data Files

Feature data in JSON format for programmatic use.

| File | Description |
|------|-------------|
| `simulator-data/simulator-worksheet-data.json` | Feature matrix: one entry per simulator with feature flags and sustainability scores |
| `simulator-data/simulator-table-data.json` | Simulator inventory: names, repository URLs, proposing paper citations, and sustainability scores |

### Methodology Artifacts

| File | Description |
|------|-------------|
| `literature-search-queries.md` | Database search strings (Table 1), inclusion/exclusion criteria, and screening funnel (573 → 321 → 261 → 83 → 45) |

## Building

From the `simulator-notes/` directory:

```
make        # PDF (two-pass pdflatex)
make html   # HTML → simulator-notes/html/
make clean  # Remove auxiliary files
```

Requires: `pdflatex`, `python3`.
