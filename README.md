# Bridging Depression and Cardiovascular Disease: Shared Inflammatory Biomarkers from an Umbrella Review

Author: Xuhang Zhao

This repository provides data and code for biomarker summaries, AMSTAR 2 item-level analysis, primary-study overlap calculations and Figure 2.

## Analyses

| Script | Analysis in the article | Output |
| --- | --- | --- |
| `biomarker_lists.py` | Depression-only, CVD-only and shared biomarker lists (Table 1) | 1 CSV |
| `amstar2_analysis.py` | Overall and item-level AMSTAR 2 summaries (Supplementary Table 3), and the scenario assuming adequate protocol registration and excluded-study reporting | 4 CSVs |
| `shared_biomarker_summary.py` | Reported heterogeneity, publication-bias and effect-direction summaries (Table 2; Supplementary Tables 4–5) | 5 CSVs |
| `cca_analysis.py` | Corrected covered area (CCA) calculated from primary-study summary counts (Supplementary Table 8) | 1 CSV |
| `plot_figure2.R` | Cumulative publication trends for included reviews (Figure 2) | PNG |

The overlap analysis includes single-study estimates retained descriptively, which were not eligible to support Class I or II classification.

## Files

- `data/`: biomarker inventory, AMSTAR 2 assessments, shared-estimate table, CCA summary counts and Figure 2 data.
- Analysis scripts: four Python scripts and one R plotting script in the repository root.
- `results/`: the 11 CSV result tables.
- `figure/`: Figure 2 artwork. The R script saves the PNG; the PDF is a reference copy.

Supporting materials, including the primary-study overlap records, are provided in the Supplementary Information and Supplementary Data accompanying the article.


## Running the scripts

Set the working directory to the repository root, including when using Spyder or RStudio.

Run a Python script, for example:

```bash
python -m pip install pandas==2.3.3
python amstar2_analysis.py
```

For Figure 2, install `ggplot2` and `ragg` and ensure Arial is available, then run:

```r
source("plot_figure2.R")
```

Tested with Python 3.13.9 (pandas 2.3.3) and R 4.3.2 (ggplot2 3.5.2, ragg 1.2.6).
