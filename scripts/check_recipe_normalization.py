import database

from meal_plan import get_recipe_canonical_ingredient
from normalization.text_normalizer import analyze_text, save_review_cache


recipes = database.get_recipes()

total = 0
recognized = 0
unknown = 0
unknown_ingredients = []

for recipe in recipes:
    print(f"\nRecipe Name: {recipe['name']}")

    for ingredient in recipe["ingredients"]:
        ingredient_name = ingredient["name"]

        analysis = analyze_text(
            ingredient_name,
            source="recipe"
        )

        canonical = get_recipe_canonical_ingredient(ingredient_name)

        total += 1

        if canonical is None:
            unknown += 1
            unknown_ingredients.append({
                "recipe": recipe["name"],
                "ingredient": ingredient_name,
            })
        else:
            recognized += 1

        print({
            "Ingredient": ingredient_name,
            "Normalized": analysis["normalized"],
            "Match": analysis["matched_term"],
            "Canonical": canonical,
            "Is it recognized": analysis["recognized"],
        })


coverage = (recognized / total) * 100 if total > 0 else 0


print("\n" + "=" * 50)
print("RECIPE NORMALIZATION SUMMARY")
print("=" * 50)

print(f"Total recipe ingredients: {total}")
print(f"Canonicalized: {recognized}")
print(f"Unknown: {unknown}")
print(f"Coverage: {coverage:.1f}%")


print("\nUNKNOWN INGREDIENTS")
print("-" * 50)

if unknown_ingredients:
    for item in unknown_ingredients:
        print(
            f"{item['recipe']} | {item['ingredient']}"
        )
else:
    print("No unknown ingredients.")


save_review_cache()
database.pool.close()