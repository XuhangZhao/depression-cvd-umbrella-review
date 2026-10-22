"""Calculate corrected covered area (CCA) from c/N/r summary counts."""
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

summary = pd.read_csv('data/cca_summary.csv', keep_default_na=False)
assert not summary.duplicated(['biomarker', 'field']).any()
# c = mapped estimates; N = primary-study occurrences; r = unique primary studies.
rows = []
for row in summary.itertuples(index=False):
    c, N, r = row.c, row.N, row.r
    assert all(type(value) is int for value in (c, N, r))
    assert c >= 1 and r >= 1 and N >= c and r <= N <= r*c

    # CCA is undefined for a single mapped estimate (c = 1).
    cca = Decimal(N-r) / Decimal(r*c-r) if c > 1 else None
    # Classify overlap using the nearest whole percentage.
    rounded = int((cca*100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) if cca is not None else None
    if rounded is None:
        category = 'NA'
    elif rounded <= 5:
        category = 'slight'
    elif rounded <= 10:
        category = 'moderate'
    elif rounded <= 15:
        category = 'high'
    else:
        category = 'very high'
    # Export CCA to four decimals and its percentage to two.
    rows.append([row.biomarker, row.field, c, N, r, N-r,
                 str(cca.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)) if cca is not None else 'NA',
                 str((cca*100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) if cca is not None else 'NA',
                 rounded if rounded is not None else 'NA', category])

cca_results = pd.DataFrame(rows, columns=['biomarker', 'field', 'c', 'N', 'r', 'N-r',
                                        'CCA', 'CCA_percent', 'rounded_CCA_percent', 'overlap_category'])
cca_results.to_csv('results/cca_results.csv', index=False)
print(cca_results.to_string(index=False))
