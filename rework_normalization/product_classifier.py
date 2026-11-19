from rework_normalization import ingredient_normalizer
from rework_normalization import text_normalizer

def calculate_keyword_score(text, keywords):
    prepared_food_score = 0
    seasoned_food_score = 0
    unmatched_words = []

    for word in text.split():
        if word in keywords["prepared_foods"] or word in keywords["seasoned_foods"]:
            if word in keywords["prepared_foods"]:
                prepared_food_score += keywords["prepared_foods"][word]
            if word in keywords["seasoned_foods"]:
                seasoned_food_score += keywords["seasoned_foods"][word]
        else:
            unmatched_words.append(word)

    return {
        "prepared_food_score": prepared_food_score,
        "seasoned_food_score": seasoned_food_score,
        "unmatched_words": unmatched_words
    }

def classify_product(text, keywords, known_ingredients, ingredient_categories):
    normalized_text = text_normalizer.normalize_text(text)

    if normalized_text is None:
        return None

    
    score = calculate_keyword_score(normalized_text, keywords)
    ingredients = ingredient_normalizer.find_ingredients(normalized_text, known_ingredients)
    is_prepared = False
    is_seasoned = False

    if score["prepared_food_score"] >= 5:
        is_prepared = True
    if score["seasoned_food_score"] >= 5:
        is_seasoned = True

    if is_prepared:
        return "prepared_food"
    elif is_seasoned:
        return "seasoned_ingredient"
    elif ingredients:

        categories = ingredient_normalizer.categorize_ingredients(ingredients, ingredient_categories)
        ingredient_analysis = analyze_ingredient_categories(categories)

        if (ingredient_analysis['core_ingredients'] 
            and ingredient_analysis['flavoring_ingredients']):
            return "seasoned_ingredient"
        
        if len(ingredient_analysis["core_ingredients"]) > 1:
            return "ambiguous"
        
        return "base_ingredient"
    else:
        return None

def analyze_ingredient_categories(categorized_ingredients):
    core_ingredients = []
    flavoring_ingredients = []

    core_categories = {
        "protein",
        "vegetable",
        "grain",
        "dairy",
    }
    flavoring_categories = {
        "aromatic",
        "sweetener",
        "herb",
        "spice",
    }

    for ingredient, category in categorized_ingredients:
        if category in core_categories:
            core_ingredients.append(ingredient)
        elif category in flavoring_categories:
            flavoring_ingredients.append(ingredient)

    return {
        "core_ingredients": core_ingredients,
        "flavoring_ingredients": flavoring_ingredients
    }