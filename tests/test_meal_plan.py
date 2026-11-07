from meal_plan import (
    get_recipe_canonical_ingredient,
    match_canonical_ingredient,
    generate
)

import pytest


@pytest.mark.parametrize(
    "ingredient_name, expected",
    [
        ("Chicken Breast", "chicken breast"),
        ("Chicken Breasts", "chicken breast"),
        ("Unsalted Butter", "butter"),
        ("Olive Oil", "olive oil"),
        ("Extra Virgin Olive Oil", "olive oil"),
        ("Potatoes", "potato"),
        ("Carrots", "carrot"),
        ("Red Pepper", "red pepper"),
    ],
)
def test_recipe_ingredient_canonicalization(
    ingredient_name,
    expected,
):
    assert (
        get_recipe_canonical_ingredient(ingredient_name)
        == expected
    )

def test_recipe_ingredient_is_canonicalized():
    result = get_recipe_canonical_ingredient(
        "Chicken Breasts"
    )

    assert result == "chicken breast"

def test_canonical_ingredient_matches_deal():
    deal = {
        "item": "Open Nature Boneless Skinless Chicken Breasts",
        "canonical_ingredient": "chicken breast",
    }

    assert match_canonical_ingredient(
        "Chicken Breasts",
        deal,
    )

def test_different_canonical_ingredients_do_not_match():
    deal = {
        "item": "Land O'Lakes Butter",
        "canonical_ingredient": "butter",
    }

    assert not match_canonical_ingredient(
        "Chicken Breast",
        deal,
    )

def test_unknown_recipe_ingredient_does_not_match():
    deal = {
        "item": "Land O'Lakes Butter",
        "canonical_ingredient": "butter",
    }

    assert not match_canonical_ingredient(
        "Some Ingredient We Do Not Know",
        deal,
    )

def test_generate_ignores_water():
    weekly_deals = [
        {
            "item": "Boneless Skinless Chicken Breast",
            "canonical_ingredient": "chicken breast",
            "price": 4.99,
        }
    ]

    recipes = [
        {
            "name": "Test Recipe",
            "ingredients": [
                {"name": "Water", "measurement": "1 cup"},
                {"name": "Chicken Breast", "measurement": "1"},
            ],
        }
    ]

    result = generate(weekly_deals, recipes, 1)

    recipe = result["recipes"][0]

    assert recipe["matches"] == 1
    assert recipe["match_percentage"] == 100
    assert "Water" not in recipe["missing"]
    assert "Water" not in result["shopping_list"]