def generate(weekly_deals, recipes, meal_count):
    recommended_recipes = []

    for recipe in recipes:
        ingredients = set ()
        matches = set ()
        matched_deals = []

        for ingredient in recipe['ingredients']:
            ingredients.add(ingredient['name'].title())

        for ingredient in recipe['ingredients']:
            best_deal = None
            for deal in weekly_deals:
                ingredient_words = set(ingredient['name'].title().split())
                deals_words = set(deal['item'].title().split())

                matching_words = (ingredient_words & deals_words)
                if len(matching_words) > 0:
                    matching_percentage = len(matching_words) / len(ingredient_words)
                else:
                    matching_percentage = 0

                if matching_percentage >= .51:
                    if ingredient['unit'] in deal['unit']:
                        if best_deal is None:
                            best_deal = deal
                        elif best_deal['price'] > deal['price']:
                            best_deal = deal

            if best_deal is not None:
                matches.add(ingredient['name'].title())
                matched_deals.append({
                    'ingredient': ingredient,
                    'item': best_deal['item'],
                    'price': best_deal['price'],
                    'unit': best_deal['unit']
                })

        matches_length = len(matches)
        missing = (ingredients - matches)
        missing_ingredients = []
        match_percentage = (matches_length / len(ingredients)) * 100

        for ingredient in recipe['ingredients']:
            if ingredient['name'].title() in missing:
                missing_ingredients.append(ingredient)


        if matches_length > 0:
            recommended_recipes.append({
                'recipe': recipe['name'], 
                'matches': matches_length, 
                'missing': missing, 
                'missing_length': len(missing), 
                'match_percentage': match_percentage,
                'matched_deals': matched_deals,
                'missing_ingredients': missing_ingredients
                })

    recommended_recipes.sort(key=lambda item: (item['matches'], -item['missing_length']), reverse=True)


    if recommended_recipes:
        output = ""
        resize = None
        shopping_list = {}
        if len(recommended_recipes) < meal_count:
            resize = "Not enough recipes. Outputting all recipes: \n"

        for index, recommendation in enumerate(recommended_recipes[0:meal_count], start=1):
            match_list = ""
            total_cost = 0
            for match in recommendation['matched_deals']:
                if match['ingredient']['unit'] in match['unit']:
                    ingredient_cost = match['ingredient']['quantity'] * match['price']
                else:
                    ingredient_cost = None

                if ingredient_cost is not None:
                    total_cost += ingredient_cost
                    match_list += (f"{match['item']} -> ${match['price']:.2f} {match['unit']} x {match['ingredient']['quantity']} {match['ingredient']['unit']} = ${ingredient_cost:.2f} | ")
                else:
                    match_list += (f"{match['item']} -> ${match['price']:.2f} {match['unit']} x {match['ingredient']['quantity']} {match['ingredient']['unit']} = Unavailable | ")
                

            output += f"{index}. {recommendation['recipe']} - Matches: {recommendation['matches']} {match_list} Missing: {recommendation['missing_length']}  Matched Deal Cost: ${total_cost:.2f} | Deal Match: {recommendation['match_percentage']:.0f}% \n"
            output += " Need to buy: " + ", ".join(recommendation['missing'])  +"\n"

            for ingredient in recommendation['missing_ingredients']:
                if ingredient['name'] not in shopping_list:
                    shopping_list[ingredient['name']] = {
                        'quantity': ingredient['quantity'],
                        'unit': ingredient['unit']
                    }
                else:
                    shopping_list[ingredient['name']]['quantity'] += ingredient['quantity']

        output += "Shopping List: \n"
        for name in shopping_list:
            output += f"{name} - {shopping_list[name]['quantity']} {shopping_list[name]['unit']} \n"

        if resize is not None:
            output = resize + output

        return output
    else:
        return "No Matching recipes found"