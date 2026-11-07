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


def classify_canonical_ingredient(canonical_ingredient):
    """
    Classify an ingredient that has already been converted
    to its canonical form.
    """
    if canonical_ingredient is None:
        return None

    for category, ingredients in ingredient_categories.items():
        if canonical_ingredient in ingredients:
            return category

    return None


def classify_ingredient(ingredient_name):
    """
    Normalize an ingredient name and return its internal category.
    """
    matched_term = find_best_known_term(ingredient_name)

    if matched_term is None:
        return None

    canonical_ingredient = get_canonical_term(matched_term)

    if canonical_ingredient is None:
        return None

    return classify_canonical_ingredient(canonical_ingredient)