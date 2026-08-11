from pathlib import Path
import generate_recipes

SOURCE = Path('tutis-airfryer-recipes-cleaned.txt')

lines = SOURCE.read_text(encoding='utf-8').splitlines()
headings = [generate_recipes.normalize_heading(line) for line in lines if generate_recipes.is_recipe_heading(line)]
expected = {generate_recipes.EXISTING_FILENAME_MAP.get(h, generate_recipes.slugify(h)) for h in headings}
existing = {p.name for p in Path('.').glob('*.html') if p.name != 'index.html'}
print('Headings:', len(headings))
print('Expected generated files:', len(expected))
print('Existing HTML files:', len(existing))
print('Missing pages:', sorted(expected - existing))
print('Extra files:', sorted(existing - expected))
print('Sample extra files:', sorted(existing - expected)[:30])
