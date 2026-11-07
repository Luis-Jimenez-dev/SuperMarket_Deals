import database

from normalization.text_normalizer import (
    find_best_known_term,
    get_canonical_term,
)


def audit_recipe_ingredients():
    recipes = database.get_recipes()

    total_ingredients = 0
    recognized_ingredients = 0

    recognized = {}
    unrecognized = set()

    for recipe in recipes:
        for ingredient in recipe["ingredients"]:
            ingredient_name = ingredient["name"]

            if not isinstance(ingredient_name, str):
                continue

            ingredient_name = ingredient_name.strip()

            if not ingredient_name:
                continue

            total_ingredients += 1

            matched_term = find_best_known_term(ingredient_name)

            if matched_term is None:
                unrecognized.add(ingredient_name)
                continue

            canonical_ingredient = get_canonical_term(matched_term)

            if canonical_ingredient is None:
                unrecognized.add(ingredient_name)
                continue

            recognized_ingredients += 1

            if canonical_ingredient not in recognized:
                recognized[canonical_ingredient] = set()

            recognized[canonical_ingredient].add(ingredient_name)

    if total_ingredients > 0:
        coverage = (
            recognized_ingredients
            / total_ingredients
            * 100
        )
    else:
        coverage = 0

    print("\n--- Recipe Ingredient Audit ---")
    print(f"Recipes: {len(recipes)}")
    print(f"Total ingredient uses: {total_ingredients}")
    print(f"Recognized ingredient uses: {recognized_ingredients}")
    print(
        f"Unrecognized ingredient uses: "
        f"{total_ingredients - recognized_ingredients}"
    )
    print(f"Coverage: {coverage:.2f}%")

    print(
        f"\nUnique canonical ingredients: "
        f"{len(recognized)}"
    )

    print(
        f"Unique unrecognized ingredients: "
        f"{len(unrecognized)}"
    )

    if unrecognized:
        print("\n--- Unrecognized Ingredients ---")

        for ingredient_name in sorted(
            unrecognized,
            key=str.lower
        ):
            print(ingredient_name)


if __name__ == "__main__":
    audit_recipe_ingredients()