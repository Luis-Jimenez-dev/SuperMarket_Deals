import requests

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



if __name__ == "__main__":
    recipe = get_recipe("52772")
    ingredients = extract_ingredients(recipe)
    print(normalize_recipe(recipe))