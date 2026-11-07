import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "normalization" / "data"

VOCABULARY_FILE = DATA_DIR / "grocery_vocabulary.json"
CATEGORIES_FILE = DATA_DIR / "ingredient_categories.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def audit_ingredient_categories():
    vocabulary = load_json(VOCABULARY_FILE)
    categories = load_json(CATEGORIES_FILE)

    canonical_ingredients = set(
        vocabulary["ingredients"].keys()
    )

    categorized_ingredients = []
    ingredient_categories = {}

    for category, ingredients in categories.items():
        for ingredient in ingredients:
            categorized_ingredients.append(ingredient)

            if ingredient not in ingredient_categories:
                ingredient_categories[ingredient] = []

            ingredient_categories[ingredient].append(category)

    categorized_set = set(categorized_ingredients)

    missing_categories = (
        canonical_ingredients - categorized_set
    )

    unknown_ingredients = (
        categorized_set - canonical_ingredients
    )

    duplicate_categories = {
        ingredient: assigned_categories
        for ingredient, assigned_categories
        in ingredient_categories.items()
        if len(assigned_categories) > 1
    }

    print("\n--- Ingredient Category Audit ---")
    print(
        f"Canonical ingredients: "
        f"{len(canonical_ingredients)}"
    )
    print(
        f"Categorized ingredients: "
        f"{len(categorized_set)}"
    )
    print(
        f"Missing categories: "
        f"{len(missing_categories)}"
    )
    print(
        f"Unknown category entries: "
        f"{len(unknown_ingredients)}"
    )
    print(
        f"Duplicate assignments: "
        f"{len(duplicate_categories)}"
    )

    if missing_categories:
        print("\n--- Missing Categories ---")

        for ingredient in sorted(missing_categories):
            print(ingredient)

    if unknown_ingredients:
        print("\n--- Unknown Category Entries ---")

        for ingredient in sorted(unknown_ingredients):
            print(ingredient)

    if duplicate_categories:
        print("\n--- Duplicate Category Assignments ---")

        for ingredient, assigned_categories in sorted(
            duplicate_categories.items()
        ):
            categories_text = ", ".join(
                assigned_categories
            )

            print(
                f"{ingredient}: "
                f"{categories_text}"
            )

    if (
        not missing_categories
        and not unknown_ingredients
        and not duplicate_categories
    ):
        print(
            "\nCategory data is consistent."
        )


if __name__ == "__main__":
    audit_ingredient_categories()