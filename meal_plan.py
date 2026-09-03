def generate(weekly_deals, recipes):
    recommended_recipes = []
    deals = set()

    for deal in weekly_deals:
        deals.add(deal['item'])

    for recipe in recipes:
        ingredients = set (recipe['ingredients'])
        matches_length = len(deals & ingredients)
        missing_length = len(ingredients - deals)
        missing = (ingredients - deals)

        if matches_length > 0:
            recommended_recipes.append({'recipe': recipe['name'], 'matches': matches_length, 'missing': missing, 'missing_length': missing_length})

    recommended_recipes.sort(key=lambda item: (item['matches'], -item['missing_length']), reverse=True)

    if recommended_recipes:
        output = ""
        for index, recommendation in enumerate(recommended_recipes, start=1):
            output += f"{index}. {recommendation['recipe']} - Matches: {recommendation['matches']} Missing: {recommendation['missing_length']} Need to buy: " + ", ".join(recommendation['missing']) + "\n" 

        return output
    else:
        return "No Matching recipes found"