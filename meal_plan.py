def generate(weekly_deals, recipes):
    best_match = 0
    best_recipe = None
    best_missing = None
    least_missing = 999
    recommended_recipes = []
    deals = set ()

    for deal in weekly_deals:
        deals.add(deal['item'])

    for recipe in recipes:
        ingredients = set (recipe['ingredients'])
        matches_length = len(deals & ingredients)
        missing_length = len(ingredients - deals)
        missing = (ingredients - deals)

        if matches_length > 0 and ((matches_length > best_match) or (matches_length == best_match and missing_length < least_missing)): 
            best_match = matches_length
            best_recipe = recipe
            best_missing = missing
            least_missing = missing_length
        if matches_length > 0:
            recommended_recipes.append({'recipe': recipe['name'], 'matches': matches_length, 'missing': missing, 'missing_length': missing_length})

    recommended_recipes.sort(key=lambda item: (item['matches'], -item ['missing_length']), reverse=True)
    print (recommended_recipes)

    if best_recipe is not None:
        return f"{best_recipe['name']} - Matches: {best_match} Missing: {len(best_missing)} \n Need to buy: " + ", ".join(best_missing)
    else:
        return "No Matching recipes found"