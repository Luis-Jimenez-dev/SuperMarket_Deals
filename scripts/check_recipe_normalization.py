import database
from normalization.text_normalizer import analyze_text, save_review_cache

recipes = database.get_recipes()

for recipe in recipes:
    print ("Recipe Name: " + recipe['name'])
    ingredients = recipe['ingredients']
    for ingredient in ingredients:
        analysis = analyze_text(ingredient['name'],
                     source = 'recipe')
        print ({
            "Ingredient ": ingredient['name'],
            "Normalized": analysis['normalized'],
            "Match": analysis['matched_term'],
            "Is it recognized": analysis['recognized']
        })

    save_review_cache()
database.pool.close()