import json

def load_ingredient_categories():
    with open(
        "ingredient_categories.json",
        "r",
        encoding = "utf-8"
    ) as file:
        categories = json.load(file)

    return categories

ingredient_categories = load_ingredient_categories()

def classify_ingredient (ingredient_name):
    ingredient_name = ingredient_name.lower()
    for category, ingredients in ingredient_categories.items():
        if ingredient_name in ingredients:
            return category

    return None

print(classify_ingredient("chicken breasts"))
print(classify_ingredient("brown rice"))
print(classify_ingredient("soy sauce"))
print(classify_ingredient("cornstarch"))