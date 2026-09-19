# Handles recipe matching, meal plan generation, and recipe loading

import json


# # Generate meal recommendations based on the store's weekly deals
# def format_meal_plan(weekly_deals, recipes, meal_count):
#     recommended_recipes = []

#     # Compare every recipe against the available weekly deals
#     for recipe in recipes:
#         ingredients = set()
#         matches = set()
#         matched_deals = []

#         # Keep track of all ingredients required by the recipe
#         for ingredient in recipe['ingredients']:
#             ingredients.add(ingredient['name'].title())

#         # Find the best available deal for each recipe ingredient
#         for ingredient in recipe['ingredients']:
#             best_deal = None

#             for deal in weekly_deals:
#                 # Split ingredient and deal names into words so partial names can match
#                 ingredient_words = set(ingredient['name'].title().split())
#                 deals_words = set(deal['item'].title().split())

#                 matching_words = ingredient_words & deals_words

#                 # Calculate how much of the ingredient name matches the deal name
#                 if len(matching_words) > 0:
#                     matching_percentage = (
#                         len(matching_words) / len(ingredient_words)
#                     )
#                 else:
#                     matching_percentage = 0

#                 # Require more than half of the ingredient words to match
#                 if matching_percentage >= .51:
#                     # Only compare deals that use a compatible unit
#                     if ingredient['unit'] in deal['unit']:
#                         # Keep the cheapest matching deal
#                         if best_deal is None:
#                             best_deal = deal
#                         elif best_deal['price'] > deal['price']:
#                             best_deal = deal

#             # Save the selected deal if a matching one was found
#             if best_deal is not None:
#                 matches.add(ingredient['name'].title())

#                 matched_deals.append({
#                     'ingredient': ingredient,
#                     'item': best_deal['item'],
#                     'price': best_deal['price'],
#                     'unit': best_deal['unit']
#                 })

#         matches_length = len(matches)

#         # Find which recipe ingredients were not matched to a weekly deal
#         missing = ingredients - matches
#         missing_ingredients = []

#         # Calculate the percentage of recipe ingredients that have matching deals
#         match_percentage = (matches_length / len(ingredients)) * 100

#         # Keep the full ingredient data for items that still need to be purchased
#         for ingredient in recipe['ingredients']:
#             if ingredient['name'].title() in missing:
#                 missing_ingredients.append(ingredient)

#         # Only recommend recipes that matched at least one weekly deal
#         if matches_length > 0:
#             recommended_recipes.append({
#                 'recipe': recipe['name'],
#                 'matches': matches_length,
#                 'missing': list(missing),
#                 'missing_length': len(missing),
#                 'match_percentage': match_percentage,
#                 'matched_deals': matched_deals,
#                 'missing_ingredients': missing_ingredients
#             })

#     # Rank recipes by the most matched ingredients and then the fewest missing
#     recommended_recipes.sort(
#         key=lambda item: (item['matches'], -item['missing_length']),
#         reverse=True
#     )

#     selected_recipes = recommended_recipes[0:meal_count]

#     if recommended_recipes:
#         output = ""
#         resize = None
#         shopping_list = {}

#         # Warn when fewer recipes are available than the user requested
#         if len(recommended_recipes) < meal_count:
#             resize = "Not enough recipes. Outputting all recipes: \n"

#         # Only generate the number of meals requested by the user
#         for index, recommendation in enumerate(
#             selected_recipes,
#             start=1
#         ):
#             match_list = ""
#             total_cost = 0

#             # Calculate the cost of the matched deal ingredients
#             for match in recommendation['matched_deals']:
#                 if match['ingredient']['unit'] in match['unit']:
#                     ingredient_cost = (
#                         match['ingredient']['quantity'] * match['price']
#                     )
#                 else:
#                     ingredient_cost = None

#                 # Add compatible ingredient costs to the recipe's total
#                 if ingredient_cost is not None:
#                     total_cost += ingredient_cost

#                     match_list += (
#                         f"{match['item']} -> "
#                         f"${match['price']:.2f} {match['unit']} x "
#                         f"{match['ingredient']['quantity']} "
#                         f"{match['ingredient']['unit']} = "
#                         f"${ingredient_cost:.2f} | "
#                     )
#                 else:
#                     match_list += (
#                         f"{match['item']} -> "
#                         f"${match['price']:.2f} {match['unit']} x "
#                         f"{match['ingredient']['quantity']} "
#                         f"{match['ingredient']['unit']} = Unavailable | "
#                     )

#             # Format the recipe recommendation for the command-line interface
#             output += (
#                 f"{index}. {recommendation['recipe']} - "
#                 f"Matches: {recommendation['matches']} "
#                 f"{match_list} "
#                 f"Missing: {recommendation['missing_length']} "
#                 f"Matched Deal Cost: ${total_cost:.2f} | "
#                 f"Deal Match: {recommendation['match_percentage']:.0f}% \n"
#             )

#             output += (
#                 " Need to buy: "
#                 + ", ".join(recommendation['missing'])
#                 + "\n"
#             )

#             # Combine missing ingredients from each meal into one shopping list
#             for ingredient in recommendation['missing_ingredients']:
#                 if ingredient['name'] not in shopping_list:
#                     shopping_list[ingredient['name']] = {
#                         'quantity': ingredient['quantity'],
#                         'unit': ingredient['unit']
#                     }
#                 else:
#                     shopping_list[ingredient['name']]['quantity'] += (
#                         ingredient['quantity']
#                     )

#         # Add the combined shopping list to the final output
#         output += "Shopping List: \n"

#         for name in shopping_list:
#             output += (
#                 f"{name} - "
#                 f"{shopping_list[name]['quantity']} "
#                 f"{shopping_list[name]['unit']} \n"
#             )

#         if resize is not None:
#             output = resize + output

#         return output

#     else:
#         return "No Matching recipes found"


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

                matched_deals.append({
                    'ingredient': ingredient,
                    'item': best_deal['item'],
                    'price': best_deal['price'],
                    'unit': best_deal['unit']
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
                'missing_ingredients': missing_ingredients
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

    return selected_recipes