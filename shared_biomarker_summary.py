"""Summarise reported heterogeneity, publication bias and effect direction."""
import pandas as pd

shared = pd.read_csv('data/shared_biomarker_estimates.csv', keep_default_na=False)
assert shared.field.isin(['depression', 'CVD']).all()
categories = {
    'heterogeneity': ['High', 'Moderate', 'Low', 'Single-study', 'NR'],
    'publication_bias': ['YES', 'NO', 'NR', 'not applicable'],
    'direction': ['↑', '↓', 'NS']}
direction_labels = {'↑': 'Increase', '↓': 'Decrease', 'NS': 'NS'}

# Percentages include all estimates, including NR and not applicable.
for column, labels in categories.items():
    assert shared[column].isin(labels).all(), f'Unexpected category in {column}.'
    rows = []
    for scope in ['Overall', 'depression', 'CVD']:
        selected = shared if scope == 'Overall' else shared.loc[shared.field.eq(scope)]
        counts = selected[column].value_counts().reindex(labels, fill_value=0)
        for label, count in counts.items():
            rows.append([scope, label, int(count), round(100*count/len(selected), 1)])
    summary = pd.DataFrame(rows, columns=['Scope', 'Category', 'Count', 'Percent'])
    if column == 'direction':
        summary['Category'] = summary['Category'].replace(direction_labels)
    summary.to_csv(f'results/{column}_summary.csv', index=False, encoding='utf-8-sig')
    print(column)
    print(summary.to_string(index=False))

# Estimate counts by biomarker and field.
for column in ['heterogeneity', 'direction']:
    counts = (shared.groupby(['biomarker', 'field'], sort=False)[column]
              .value_counts().unstack(fill_value=0)
              .reindex(columns=categories[column], fill_value=0))
    counts.insert(0, 'Total', counts.sum(axis=1))
    by_biomarker = counts.reset_index()
    by_biomarker = by_biomarker.rename(columns=direction_labels)
    by_biomarker.to_csv(f'results/{column}_by_biomarker.csv', index=False, encoding='utf-8-sig')
