def generate(weekly_deals, recipes, meal_count):
    recommended_recipes = []

    for recipe in recipes:
        ingredients = set ()
        matches = set ()
        matched_deals = []

        for ingredient in recipe['ingredients']:
            ingredients.add(ingredient['name'].title())

        for ingredient in recipe['ingredients']:
            for deal in weekly_deals:
                ingredient_words = set(ingredient['name'].title().split())
                deals_words = set(deal['item'].title().split())

                matching_words = (ingredient_words & deals_words)
                if len(matching_words) > 0:
                    matching_percentage = len(matching_words) / len(ingredient_words)
                else:
                    matching_percentage = 0

                if matching_percentage >= .51:
                    matches.add(ingredient['name'].title())
                    matched_deals.append({
                        'ingredient': ingredient,
                        'item': deal['item'],
                        'price': deal['price'],
                        'unit': deal['unit']
                    })

        matches_length = len(matches)
        missing = (ingredients - matches)
        match_percentage = (matches_length / len(ingredients)) * 100

        if matches_length > 0:
            recommended_recipes.append({
                'recipe': recipe['name'], 
                'matches': matches_length, 
                'missing': missing, 
                'missing_length': len(missing), 
                'match_percentage': match_percentage,
                'matched_deals': matched_deals
                })

    recommended_recipes.sort(key=lambda item: (item['matches'], -item['missing_length']), reverse=True)


    if recommended_recipes:
        output = ""
        resize = None
        shopping_list = set()
        if len(recommended_recipes) < meal_count:
            resize = "Not enough recipes. Outputting all recipes: \n"

        for index, recommendation in enumerate(recommended_recipes[0:meal_count], start=1):
            match_list = ""
            total_cost = 0
            for match in recommendation['matched_deals']:
                ingredient_cost = match['ingredient']['quantity'] * match['price']
                total_cost += ingredient_cost
                match_list += (f"{match['item']} -> ${match['price']:.2f} {match['unit']} x {match['ingredient']['quantity']} {match['ingredient']['unit']} = ${ingredient_cost:.2f} | ")
                

            output += f"{index}. {recommendation['recipe']} - Matches: {recommendation['matches']} {match_list} Missing: {recommendation['missing_length']}  Matched Deal Cost: ${total_cost:.2f} | Deal Match: {recommendation['match_percentage']:.0f}% \n"
            output += " Need to buy: " + ", ".join(recommendation['missing']) 
            shopping_list = (shopping_list | recommendation['missing'])

        output += f"Shopping List: " + ", ".join(sorted(shopping_list)) + "\n"

        if resize is not None:
            output = resize + output

        return output
    else:
        return "No Matching recipes found"