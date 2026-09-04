def generate(weekly_deals, recipes, meal_count):
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
        resize = None
        shopping_list = set()
        if len(recommended_recipes) < meal_count:
            resize = "Not enough recipes. Outputting all recipes: \n"

        for index, recommendation in enumerate(recommended_recipes[0:meal_count], start=1):
            output += f"{index}. {recommendation['recipe']} - Matches: {recommendation['matches']} Missing: {recommendation['missing_length']} Need to buy: " + ", ".join(recommendation['missing']) + f" | Deal Match: {recommendation['match_percentage']:.0f}%  \n"
            shopping_list = (shopping_list | recommendation['missing'])

        output += f"Shopping List: " + ", ".join(sorted(shopping_list)) + "\n"

        if resize is not None:
            output = resize + output

        return output
    else:
        return "No Matching recipes found"