import json

from normalization.text_normalizer import (
    DATA_DIR,
    find_best_known_term,
    get_canonical_term,
)

CATEGORY_FILE = DATA_DIR / "ingredient_categories.json"


def load_ingredient_categories():
    with open(CATEGORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


ingredient_categories = load_ingredient_categories()


def classify_ingredient(ingredient_name):
    matched_term = find_best_known_term(ingredient_name)

    if matched_term is None:
        return None

    canonical = get_canonical_term(matched_term)

    if canonical is None:
        return None

    for category, ingredients in ingredient_categories.items():
        if canonical in ingredients:
            return category

    return None