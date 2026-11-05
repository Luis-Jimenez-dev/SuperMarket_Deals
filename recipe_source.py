import requests
import database

def get_recipe(recipe_id):
    url = "https://www.themealdb.com/api/json/v1/1/lookup.php"
    params = {
        'i': recipe_id
    }

    response = requests.get(
        url,
        params = params,
        timeout = 10
    )

    response.raise_for_status()
    data = response.json()

    return data["meals"][0]

def extract_ingredients(recipe):
    ingredients = []

    for i in range (1, 21):
        ingredient_key = f"strIngredient{i}"
        measurement_key = f"strMeasure{i}"

        ingredient = recipe[ingredient_key]
        measurement = recipe[measurement_key]

        if not ingredient:
            break

        ingredients.append({
            "name" : ingredient,
            "measurement": measurement
        })

    return ingredients

def normalize_recipe(recipe):
    return {
        "source": "themealdb",
        "source_recipe_id": recipe["idMeal"],
        "name": recipe["strMeal"],
        "instructions": recipe["strInstructions"],
        "image_url": recipe["strMealThumb"],
        "cuisine": recipe["strArea"],
        "category": recipe["strCategory"],
        "ingredients": extract_ingredients(recipe)
    }

def get_categories():
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    response = requests.get(
        url = url,
        timeout = 10
    )

    response.raise_for_status()
    data = response.json()
    categories = data['categories']
    category_names = [
        category['strCategory']
        for category in categories
    ]

    return category_names

def get_recipes_by_category(category):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php"

    params = {
        "c": category
    }

    response = requests.get(
        url = url,
        params = params,
        timeout = 10
    )

    response.raise_for_status()
    data = response.json()

    return data["meals"]

def ingest_category(category, limit = None):
    recipes = get_recipes_by_category(category)

    if limit is not None:
        recipes = recipes [:limit]

    for recipe in recipes:
        recipe_id = recipe["idMeal"]

        full_recipe = get_recipe(recipe_id)

        normalized_recipe = normalize_recipe(full_recipe)

        hungy_recipe_id = hungy_recipe_id = database.save_recipe(normalized_recipe)

        print(
            f"Saved {normalized_recipe['name']} "
            f"as Hungy recipe {hungy_recipe_id}"
        )

if __name__ == "__main__":
    try:
        ingest_category("Chicken", limit=3)
    finally:
        database.pool.close()