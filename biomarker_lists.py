"""List depression-only, CVD-only and shared biomarkers."""
import pandas as pd

inventory = pd.read_csv('data/biomarker_inventory.csv', keep_default_na=False)
assert inventory.biomarker.is_unique
assert inventory[['depression', 'CVD']].isin([0, 1]).all().all()
assert (inventory.depression + inventory.CVD).gt(0).all()

rows = []
for category, selected in [
    ('Depression only', inventory.depression.eq(1) & inventory.CVD.eq(0)),
    ('CVD only', inventory.depression.eq(0) & inventory.CVD.eq(1)),
    ('Shared', inventory.depression.eq(1) & inventory.CVD.eq(1))]:
    names = sorted(inventory.loc[selected, 'biomarker'], key=str.casefold)
    rows.extend([category, name] for name in names)

biomarker_lists = pd.DataFrame(rows, columns=['category', 'biomarker'])
biomarker_lists.to_csv('results/biomarker_lists.csv', index=False)
print(biomarker_lists.groupby('category', sort=False).size())
