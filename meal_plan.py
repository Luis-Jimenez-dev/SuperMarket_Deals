def generate(weekly_deals, recipes):
    recommended_recipes = []
    deals = set()

    for deal in weekly_deals:
        deals.add(deal['item'].title())

    for recipe in recipes:
        ingredients = set ()
        matches = set ()

        for ingredient in recipe['ingredients']:
            ingredients.add(ingredient.title())

        for ingredient in ingredients:
            for deal in deals:
                ingredient_words = set(ingredient.split())
                deals_words = set(deal.split())

                matching_words = (ingredient_words & deals_words)
                if len(matching_words) > 0:
                    matching_percentage = len(matching_words) / len(ingredient_words)
                else:
                    matching_percentage = 0

                if matching_percentage >= .51:
                    matches.add(ingredient)


        matches_length = len(matches)
        missing = (ingredients - matches)
        match_percentage = (matches_length / len(ingredients)) * 100

        if matches_length > 0:
            recommended_recipes.append({'recipe': recipe['name'], 'matches': matches_length, 'missing': missing, 'missing_length': len(missing), 'match_percentage': match_percentage})

    recommended_recipes.sort(key=lambda item: (item['matches'], -item['missing_length']), reverse=True)

    if recommended_recipes:
        output = ""
        shopping_list = set()
        for index, recommendation in enumerate(recommended_recipes[0:3], start=1):
            output += f"{index}. {recommendation['recipe']} - Matches: {recommendation['matches']} Missing: {recommendation['missing_length']} Need to buy: " + ", ".join(recommendation['missing']) + f" | Deal Match: {recommendation['match_percentage']:.0f}%  \n"
            shopping_list = (shopping_list | recommendation['missing'])

        output += f"Shopping List: " + ", ".join(sorted(shopping_list)) + "\n"

        return output
    else:
        return "No Matching recipes found"