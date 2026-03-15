#!/usr/bin/env python3
"""
generate_table.py

Generates simulator-worksheet.html by:
  1. Parsing simulator_selection_worksheet.tex to build a clean HTML table
  2. Running pandoc on simulator-notes.tex to render the notes section
  3. Assembling a full HTML page

Usage:
    python3 generate_table.py [-o OUTPUT]
"""

import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# ── Column definitions ────────────────────────────────────────────────────────
# (display label, group key, CSS class)
COLUMNS = [
    ("Simulator",            "sim",        "col-sim"),
    ("Bio-Inspired",         "neuron",     "col-neuron"),
    ("Bio-Plausible",        "neuron",     "col-neuron"),
    ("Integrate-and-Fire",   "neuron",     "col-neuron"),
    ("Compartmental",        "neuron",     "col-neuron"),
    ("Equation-Based",       "neuron",     "col-neuron"),
    ("Supervised",           "learning",   "col-learning"),
    ("Unsupervised",         "learning",   "col-learning"),
    ("Static",               "learning",   "col-learning"),
    ("CPU",                  "hardware",   "col-hardware"),
    ("GPU",                  "hardware",   "col-hardware"),
    ("FPGA",                 "hardware",   "col-hardware"),
    ("Neuromorphic",         "hardware",   "col-hardware"),
    ("Freshness",            "viability",  "col-viability"),
    ("Documentation",        "viability",  "col-viability"),
    ("Community",            "viability",  "col-viability"),
    ("Viability Score",      "viability",  "col-viability"),
]

# (display label, number of columns it spans)
GROUPS = [
    ("",                     1),
    ("Neuron Model Family",  5),
    ("Learning Method",      3),
    ("Hardware Support",     4),
    ("Viability Scorecard",  4),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def pandoc_anchor(label: str) -> str:
    """
    Pandoc preserves \\label{X} directly as id="X" in HTML output.
    Spaces must be percent-encoded in href attributes.
    """
    return label.replace(" ", "%20")


def render_cell(val) -> str:
    if val == "check":
        return '<span class="check" aria-label="yes">✓</span>'
    if isinstance(val, int):
        return str(val)
    return ""


# ── LaTeX parser ──────────────────────────────────────────────────────────────

def parse_rows(tex_path: Path) -> list:
    text = tex_path.read_text()

    # Extract body between \midrule and \bottomrule
    m = re.search(r"\\midrule(.*?)\\bottomrule", text, re.DOTALL)
    if not m:
        sys.exit(f"ERROR: could not find table body in {tex_path}")

    rows = []
    for line in m.group(1).strip().splitlines():
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        # Strip trailing \\ or \\\hline
        line = re.sub(r"\\\\(?:\\hline)?\s*$", "", line).strip()
        if not line:
            continue

        cells = [c.strip() for c in line.split("&")]
        if len(cells) != len(COLUMNS):
            continue

        sim_cell = cells[0]
        url_m   = re.search(r"\\href\{([^}]+)\}\{([^}]+)\}", sim_cell)
        label_m = re.search(r"\\hyperref\[([^\]]+)\]",        sim_cell)
        if not url_m:
            continue

        values = []
        for cell in cells[1:]:
            c = cell.strip()
            if "\\checkmark" in c:
                values.append("check")
            elif re.fullmatch(r"\d+", c):
                values.append(int(c))
            else:
                values.append(None)

        label = label_m.group(1) if label_m else url_m.group(2)
        rows.append({
            "name":   url_m.group(2),
            "url":    url_m.group(1),
            "label":  label,
            "anchor": pandoc_anchor(label),
            "values": values,
        })

    return rows


# ── HTML table renderer ───────────────────────────────────────────────────────

def render_table(rows: list) -> str:
    lines = [
        '<table class="sim-table" aria-label="SNN Simulator Capability Worksheet">',
        "<thead>",
    ]

    # Group header row
    lines.append('<tr class="group-row">')
    for label, span in GROUPS:
        if label:
            lines.append(f'  <th class="group-{label.split()[0].lower()}" colspan="{span}">{label}</th>')
        else:
            lines.append(f'  <th class="group-sim" colspan="{span}"></th>')
    lines.append("</tr>")

    # Column header row (rotated labels)
    lines.append('<tr class="col-header-row">')
    for label, _group, css in COLUMNS:
        lines.append(f'  <th class="{css}"><div class="rotate">{label}</div></th>')
    lines.append("</tr>")

    lines.append("</thead>")
    lines.append("<tbody>")

    for row in rows:
        lines.append("<tr>")
        lines.append(
            f'  <td class="sim-name col-sim">'
            f'<a href="{row["url"]}">{row["name"]}</a>'
            f'&nbsp;<a class="notes-link" href="#{row["anchor"]}">[notes]</a></td>'
        )
        for val, (_label, _group, css) in zip(row["values"], COLUMNS[1:]):
            lines.append(f'  <td class="{css}">{render_cell(val)}</td>')
        lines.append("</tr>")

    lines += ["</tbody>", "</table>"]
    return "\n".join(lines)


# ── Notes via pandoc ──────────────────────────────────────────────────────────

def render_notes(notes_tex: Path) -> str:
    result = subprocess.run(
        ["pandoc", "--from", "latex", "--to", "html5", str(notes_tex)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(f"ERROR: pandoc failed on {notes_tex}")
    return result.stdout


# ── Page assembly ─────────────────────────────────────────────────────────────

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>SNN Simulator Worksheet and Research Notes</title>
  <link rel="stylesheet" href="simulator-worksheet.css"/>
</head>
<body>
<h1>SNN Simulator Worksheet and Research Notes</h1>
<p class="authors">Lucas S Hindman &amp; Kurtis D Cantley</p>
<p>This document provides a capability summary worksheet for the open-source spiking
neural network (SNN) simulators surveyed in <em>Finding Order in CHAOSS</em>, followed
by detailed research notes for each simulator. Each entry in the worksheet links to its
corresponding notes section via the <strong>[notes]</strong> reference.</p>

<section id="worksheet">
<h2>Simulator Capability Worksheet</h2>
<div class="table-scroll">
{table}
</div>
</section>

<section id="notes">
<h2>Simulator Research Notes</h2>
{notes}
</section>

</body>
</html>
"""


def main():
    out_path = SCRIPT_DIR / "simulator-worksheet.html"
    if len(sys.argv) == 3 and sys.argv[1] == "-o":
        out_path = Path(sys.argv[2])

    tex_path   = SCRIPT_DIR / "simulator_selection_worksheet.tex"
    notes_path = SCRIPT_DIR / "simulator-notes.tex"

    print(f"  Parsing {tex_path.name} …", file=sys.stderr)
    rows = parse_rows(tex_path)
    print(f"  Found {len(rows)} simulator rows", file=sys.stderr)

    table = render_table(rows)

    print(f"  Running pandoc on {notes_path.name} …", file=sys.stderr)
    notes = render_notes(notes_path)

    html = PAGE_TEMPLATE.format(table=table, notes=notes)
    out_path.write_text(html)
    print(f"  Written: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
