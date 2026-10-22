"""Summarise AMSTAR 2 overall confidence ratings and item-level responses.

Also recalculate overall ratings under a hypothetical scenario in which
all reviews receive 'Yes' for item 2 (protocol registration) and item 7
(excluded-study reporting), with all other item responses unchanged.
"""
import pandas as pd

reviews = pd.read_csv('data/amstar2.csv', keep_default_na=False)
items = [f'amstar_item_{i}' for i in range(1, 17)]
critical_items = [2, 4, 7, 9, 11, 13, 15]
critical_columns = [f'amstar_item_{i}' for i in critical_items]
grades = ['High', 'Moderate', 'Low', 'Critically low']
assert reviews.review_id.is_unique
assert reviews[items].isin(['Y', 'P', 'N']).all().all()
assert reviews.field.isin(['Depression', 'CVD']).all()


def overall_rating(scores):
    """Apply the study's rule: only 'N' counts as a weakness."""
    weaknesses = scores.eq('N').sum(axis=1)
    critical_weaknesses = scores[critical_columns].eq('N').sum(axis=1)
    rating = pd.Series('High', index=scores.index)
    rating.loc[weaknesses.gt(1)] = 'Moderate'
    rating.loc[critical_weaknesses.eq(1)] = 'Low'
    rating.loc[critical_weaknesses.gt(1)] = 'Critically low'
    return rating


assert overall_rating(reviews[items]).equals(reviews.amstar_grade), 'Original ratings do not match item scores.'

scenario_scores = reviews[items].copy()
scenario_scores[['amstar_item_2', 'amstar_item_7']] = 'Y'
scenario_column = 'scenario_rating_items_2_and_7_adequate'
reviews[scenario_column] = overall_rating(scenario_scores)
scenario = reviews[['review_id', 'reference', 'amstar_grade', scenario_column]].rename(
    columns={'amstar_grade': 'reported_rating'})
scenario.to_csv('results/amstar2_scenario.csv', index=False)

# Overall ratings: original and hypothetical scenario.
for column, filename in [('amstar_grade', 'study_quality_summary.csv'),
                         (scenario_column, 'amstar2_scenario_summary.csv')]:
    rows = []
    for scope in ['Overall', 'depression', 'CVD']:
        selected = reviews if scope == 'Overall' else reviews.loc[
            reviews.field.str.lower().eq(scope.lower())]
        counts = selected[column].value_counts().reindex(grades, fill_value=0)
        for grade, count in counts.items():
            rows.append([scope, grade, int(count), round(100*count/len(selected), 1)])
    grade_summary = pd.DataFrame(rows, columns=['Scope', 'Grade', 'Count', 'Percent'])
    grade_summary.to_csv(f'results/{filename}', index=False)
    print(filename)
    print(grade_summary.to_string(index=False))

# Item-level responses, with critical domains first.
labels = {
    1: 'PICO', 2: 'Protocol', 3: 'Study Design', 4: 'Search',
    5: 'Selection', 6: 'Extraction', 7: 'Exclusion', 8: 'Characteristics',
    9: 'BiasRisk', 10: 'Funding', 11: 'Statistics', 12: 'Bias Impact',
    13: 'Bias Discussion', 14: 'Heterogeneity', 15: 'Publication Bias', 16: 'Conflict'}
order = critical_items + [i for i in range(1, 17) if i not in critical_items]
rows = []
for item in order:
    counts = reviews[f'amstar_item_{item}'].value_counts().reindex(['Y', 'P', 'N'], fill_value=0)
    y, p, n = (int(counts[response]) for response in ['Y', 'P', 'N'])
    rows.append([f'{item}_{labels[item]}', 'Yes' if item in critical_items else 'No',
                 y, p, n, len(reviews)-y-p-n, round(100*n/len(reviews), 1),
                 round(100*(y+p)/len(reviews), 1)])
item_summary = pd.DataFrame(rows, columns=['Item', 'Critical item', 'Y', 'P', 'N',
                                         'Other/Blank', 'N percent', 'Y or P percent'])
item_summary.to_csv('results/amstar2_item_summary.csv', index=False)
print(item_summary.to_string(index=False))
