import re


def find_ingredients(text, known_ingredients):
    ingredient_candidates = []
    accepted_ingredients = []
    found_ingredients = []

    for ingredient in known_ingredients:
        escaped_ingredient = re.escape(ingredient)
        match = re.search(rf'\b{escaped_ingredient}\b', text)

        if match:
            ingredient_candidates.append(
                (ingredient, match.start(), match.end())
            )

    sorted_ingredients = sorted(
        ingredient_candidates,
        key=lambda i: i[2] - i[1],
        reverse=True
    )

    for candidate in sorted_ingredients:
        has_overlap = False

        for found in found_ingredients:
            if candidate[1] < found[2] and candidate[2] > found[1]:
                has_overlap = True
                break

        if not has_overlap:
            found_ingredients.append(candidate)
            accepted_ingredients.append(candidate[0])

    return accepted_ingredients


def get_ingredient_category(ingredient, ingredient_categories):
    return ingredient_categories.get(ingredient)


def categorize_ingredients(ingredients, ingredient_categories):
    result = []

    for ingredient in ingredients:
        category = get_ingredient_category(
            ingredient,
            ingredient_categories
        )
        result.append((ingredient, category))

    return result