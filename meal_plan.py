# Handles recipe matching, meal plan generation, and recipe loading

import json

# Load recipe data from the local JSON file
def load_recipes():
    with open("recipes.json", "r", encoding="utf-8") as file:
        recipes = json.load(file)

    return recipes

# Generate structured meal recommendations from weekly grocery deals
def generate(weekly_deals, recipes, meal_count):
    recommended_recipes = []

    # Compare each recipe against the available weekly deals
    for recipe in recipes:
        ingredients = set()
        matches = set()
        matched_deals = []
        total_cost = 0

        # Keep track of every ingredient needed for the recipe
        for ingredient in recipe['ingredients']:
            ingredients.add(ingredient['name'].title())

        # Find the best available deal for each recipe ingredient
        for ingredient in recipe['ingredients']:
            best_deal = None

            # Compare the current ingredient against every weekly deal
            for deal in weekly_deals:
                ingredient_words = set(
                    ingredient['name'].title().split()
                )
                deal_words = set(
                    deal['item'].title().split()
                )

                # Find words shared between the ingredient and deal names
                matching_words = ingredient_words & deal_words

                # Calculate how much of the ingredient name matches the deal
                if len(matching_words) > 0:
                    matching_percentage = (
                        len(matching_words) / len(ingredient_words)
                    )
                else:
                    matching_percentage = 0

                # Require more than half of the ingredient words to match
                if matching_percentage >= .51:

                    # Only use deals with a compatible unit
                    if ingredient['unit'] in deal['unit']:

                        # Keep the cheapest valid deal found
                        if best_deal is None:
                            best_deal = deal
                        elif best_deal['price'] > deal['price']:
                            best_deal = deal

            # Save the ingredient and deal when a valid match was found
            if best_deal is not None:
                matches.add(ingredient['name'].title())
                total_cost += best_deal['price'] * ingredient['quantity']

                matched_deals.append({
                    'ingredient': ingredient,
                    'item': best_deal['item'],
                    'price': best_deal['price'],
                    'unit': best_deal['unit'],
                })

        # Calculate how many recipe ingredients matched available deals
        matches_length = len(matches)

        # Find the ingredients that did not have matching deals
        missing = ingredients - matches
        missing_ingredients = []

        # Calculate the percentage of ingredients with matching deals
        match_percentage = (
            matches_length / len(ingredients)
        ) * 100

        # Keep the full ingredient data for the missing ingredients
        for ingredient in recipe['ingredients']:
            if ingredient['name'].title() in missing:
                missing_ingredients.append(ingredient)

        # Only recommend recipes that matched at least one deal
        if matches_length > 0:
            recommended_recipes.append({
                'recipe': recipe['name'],
                'matches': matches_length,
                'missing': list(missing),
                'missing_length': len(missing),
                'match_percentage': match_percentage,
                'matched_deals': matched_deals,
                'missing_ingredients': missing_ingredients,
                'total_cost': total_cost
            })

    # Rank recipes by the most matches and then the fewest missing ingredients
    recommended_recipes.sort(
        key=lambda item: (
            item['matches'],
            -item['missing_length']
        ),
        reverse=True
    )

    # Only return the number of recipes requested by the user
    selected_recipes = recommended_recipes[0:meal_count]

    shopping_list = {}
    for recipe in selected_recipes:
        for ingredient in recipe['missing_ingredients']:
            if ingredient['name'] not in shopping_list:
                shopping_list[ingredient['name']] = {
                    'quantity': ingredient['quantity'],
                    'unit': ingredient['unit']
                }
            else:
                shopping_list[ingredient['name']]['quantity'] += ingredient['quantity']

    return {
        'recipes': selected_recipes,
        'shopping_list': shopping_list
    }

# Format generated meal plan data for the command-line interface
def format_meal_plan(meal_data):
    output = ""

    # Format each selected recipe
    for index, recipe in enumerate(meal_data['recipes'], start=1):
        output += (
            f"{index}. {recipe['recipe']} - Matches: {recipe['matches']} "
            f"| Deal Match: {recipe['match_percentage']:.0f}% "
            f"| Matched Deal Cost: ${recipe['total_cost']:.2f}\n"
            f"Need to buy: " + ", ".join(recipe['missing']) + "\n"
        )

    # Format the combined shopping list
    output += "\nShopping List:\n"

    for name in meal_data['shopping_list']:
        output += (
            f"{name} - "
            f"{meal_data['shopping_list'][name]['quantity']} "
            f"{meal_data['shopping_list'][name]['unit']}\n"
        )

    return output