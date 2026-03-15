# Literature Search Queries

Supporting data for *Finding Order in CHAOSS: A Survey of Open-Source Spiking Neural Network Software Simulators* — Hindman & Cantley (2026).

---

## Search date

September 2024

## Databases searched

| Database | Coverage includes |
|---|---|
| ACM Digital Library | ACM conferences and journals |
| IEEE Xplore | IEEE conferences, journals, and standards |
| Scopus | Springer, MIT Press, Frontiers in Neuroinformatics, and others |

## Search query

Both conditions below were applied simultaneously to each database (AND logic between rows).

| Applied to | Search string |
|---|---|
| Title or Abstract | `"Spiking Neural Network"` OR `"Spike Neural Network"` OR `"SNN"` OR `"Neuromorphic Computing"` |
| Any Field | `"Neuromorphic Simulator"` OR `"SNN Simulator"` OR `"Software Simulator"` OR `"Neural Network Simulator"` OR `"Software Framework"` OR `"Software Co-design"` |

**Scope filters applied in all databases:** journals, workshops, and conferences; English language only.

## Results

| Database | Raw results |
|---|---|
| ACM Digital Library | 56 |
| IEEE Xplore | 243 |
| Scopus | 274 |
| **Total (before deduplication)** | **573** |
| **After deduplication and filtering** | **321** |

## Inclusion / exclusion criteria

1. **Open-source and publicly available.** The software framework must be released under an open-source license and accessible via a public repository. Frameworks described in publications but not publicly released were excluded.

2. **Active within the past eight years.** The framework must have been used in published research or show active development from 2016 onward. The year 2016 corresponds to the inflection point in neuromorphic computing publication activity identified in the paper. Frameworks from earlier periods that show continued development and use (e.g., NEST, GENESIS) are included.

3. **Specific framework identified.** Publications that describe SNN simulation work without naming the specific software framework used were excluded.

4. **English-language publications only.** Only journals, workshops, and conferences published in English were targeted.

## Screening funnel

| Stage | Count |
|---|---|
| Raw results across all databases | 573 |
| After deduplication and exclusion of papers not naming a specific SNN framework | 321 (Baseline Corpus) |
| Candidate software frameworks extracted from Baseline Corpus | 261 |
| Validated open-source SNN frameworks (after reverse snowball and repository search) | 83 |
| Final: frameworks confirmed to include a software simulator, active since 2016 | **45** |

## Validation seed list

The search queries were validated by confirming that results included publications associated with the following frameworks, which served as the initial seed list:

SNNTorch, NEST, PyNN, Brian2, BindsNET, Nengo, Lava

---

*The complete feature matrix, sustainability scores, and per-simulator research notes for all 45 simulators are provided in this repository.*
