import time

from normalization.text_normalizer import (
    find_best_known_term,
    get_canonical_term,
)

IGNORED_RECIPE_INGREDIENTS = {
    "water",
}

def get_recipe_canonical_ingredient(ingredient_name):
    if not isinstance(ingredient_name, str) or not ingredient_name.strip():
        return None

    matched_term = find_best_known_term(ingredient_name)

    if matched_term is None:
        return None

    return get_canonical_term(matched_term)


def match_canonical_ingredient(ingredient_name, deal):
    recipe_ingredient = get_recipe_canonical_ingredient(
        ingredient_name
    )

    deal_ingredient = deal.get("canonical_ingredient")

    if recipe_ingredient is None or deal_ingredient is None:
        return False

    return recipe_ingredient == deal_ingredient


def find_best_deal(ingredient_name, weekly_deals):
    """
    Find the cheapest weekly deal with the same canonical ingredient.
    """
    best_deal = None

    for deal in weekly_deals:
        if not match_canonical_ingredient(ingredient_name, deal):
            continue

        if deal.get("price") is None:
            continue

        if (
            best_deal is None
            or deal["price"] < best_deal["price"]
        ):
            best_deal = deal

    return best_deal


def generate(weekly_deals, recipes, meal_count):
    start_time = time.time()

    recommended_recipes = []
    best_deal_cache = {}

    for recipe in recipes:
        ingredients = recipe.get("ingredients", [])

        matched_deals = []
        missing_ingredients = []
        matchable_ingredients = []

        for ingredient in ingredients:
            ingredient_name = ingredient.get("name")

            canonical_ingredient = get_recipe_canonical_ingredient(
                ingredient_name
            )

            # Unknown ingredients should not hurt the recipe's score.
            if canonical_ingredient is None:
                continue

            if canonical_ingredient in IGNORED_RECIPE_INGREDIENTS:
                continue

            matchable_ingredients.append(ingredient)

            if canonical_ingredient in best_deal_cache:
                best_deal = best_deal_cache[canonical_ingredient]
            else:
                best_deal = find_best_deal(
                    ingredient_name,
                    weekly_deals,
                )
                best_deal_cache[canonical_ingredient] = best_deal

            if best_deal is not None:
                matched_deals.append({
                    "ingredient": ingredient,
                    "canonical_ingredient": canonical_ingredient,
                    "item": best_deal["item"],
                    "price": best_deal["price"],
                    "unit": best_deal.get("unit"),
                })
            else:
                missing_ingredients.append(ingredient)

        matches_length = len(matched_deals)
        matchable_count = len(matchable_ingredients)

        if matchable_count == 0:
            continue

        match_percentage = (
            matches_length / matchable_count
        ) * 100

        # A recipe needs at least one discounted ingredient
        # to be useful as a deal-based recommendation.
        if matches_length > 0:
            recommended_recipes.append({
                "recipe": recipe["name"],
                "recipe_id": recipe.get("id"),
                "image_url": recipe.get("image_url"),
                "category": recipe.get("category"),
                "cuisine": recipe.get("cuisine"),
                "instructions": recipe.get("instructions"),
                "matches": matches_length,
                "missing": [
                    ingredient["name"]
                    for ingredient in missing_ingredients
                ],
                "missing_length": len(missing_ingredients),
                "match_percentage": match_percentage,
                "matched_deals": matched_deals,
                "missing_ingredients": missing_ingredients,
            })

    recommended_recipes.sort(
        key=lambda item: (
            item["matches"],
            item["match_percentage"],
            -item["missing_length"],
        ),
        reverse=True,
    )

    selected_recipes = recommended_recipes[:meal_count]

    shopping_list = {}

    for recipe in selected_recipes:
        for ingredient in recipe["missing_ingredients"]:
            ingredient_name = ingredient["name"]

            if ingredient_name not in shopping_list:
                shopping_list[ingredient_name] = {
                    "measurement": ingredient.get("measurement")
                }

    end_time = time.time()

    print(
        f"Meal plan generation took: "
        f"{end_time - start_time:.2f} seconds"
    )

    return {
        "recipes": selected_recipes,
        "shopping_list": shopping_list,
    }


def format_meal_plan(meal_data):
    output = ""

    for index, recipe in enumerate(
        meal_data["recipes"],
        start=1,
    ):
        output += (
            f"{index}. {recipe['recipe']} - "
            f"Matches: {recipe['matches']} "
            f"| Deal Match: "
            f"{recipe['match_percentage']:.0f}%\n"
            f"Need to buy: "
            + ", ".join(recipe["missing"])
            + "\n"
        )

    output += "\nShopping List:\n"

    for name, ingredient in meal_data["shopping_list"].items():
        measurement = ingredient.get("measurement")

        if measurement:
            output += f"{name} - {measurement}\n"
        else:
            output += f"{name}\n"

    return output