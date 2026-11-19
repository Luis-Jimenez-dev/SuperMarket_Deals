from rework_normalization.product_classifier import (
    calculate_keyword_score, classify_product
    )

keywords = {
    "prepared_foods": {
        "soup": 5,
        "dip": 5,
        "pizza": 5,
        "mashed": 5
    },
    "seasoned_foods": {
        "marinated": 5,
        "seasoned": 5,
    }
}

known_ingredients = [
    "chicken",
    "chicken breast",
    "salmon",
    "broccoli",
    "potato",
    "garlic",
    "butter",
    "honey",
    "rice",
]

ingredient_categories = {
    "chicken": "protein",
    "chicken breast": "protein",
    "salmon": "protein",
    "broccoli": "vegetable",
    "potato": "vegetable",
    "garlic": "aromatic",
    "butter": "fat",
    "honey": "sweetener",
    "rice": "grain",
}

def test_prepared_food_score():
    result = calculate_keyword_score("chicken noodle soup", {
        "prepared_foods": {
            "soup": 5,
        },
        "seasoned_foods":{

        }
    })

    assert result == ({
        "prepared_food_score": 5,
        "seasoned_food_score": 0,
        "unmatched_words": ["chicken", "noodle"]
     })

def test_seasoned_food_score():
    result = calculate_keyword_score("marinated chicken breast", {
        "prepared_foods": {

        },
        "seasoned_foods":{
            "marinated": 5,
        }
    })

    assert result == ({
        "prepared_food_score": 0,
        "seasoned_food_score": 5,
        "unmatched_words": ["chicken", "breast"]
    })

def test_unmatched_words():
    result = calculate_keyword_score("fresh salmon fillet", {
        "prepared_foods":{

        },
        "seasoned_foods":{

        }
    })

    assert result == ({
        "prepared_food_score": 0,
        "seasoned_food_score": 0,
        "unmatched_words": ["fresh", "salmon", "fillet"]
    })

def test_fresh_salmon_is_base_ingredient():
    result = classify_product(
        "fresh salmon fillet",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "base_ingredient"

def test_marinated_chicken_is_seasoned_ingredient():
    result = classify_product(
        "marinated chicken breast",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "seasoned_ingredient"

def test_chicken_noodle_soup_is_prepared_food():
    result = classify_product(
        "chicken noodle soup",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "prepared_food"

def test_non_food_product_returns_none():
    result = classify_product(
        "playstation controller",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result is None

def test_none_returns_none():
    result = classify_product(
        None,
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result is None

def test_honey_garlic_salmon_is_seasoned_ingredient():
    result = classify_product(
        "honey garlic salmon",
        keywords,
        [
            "honey",
            "garlic",
            "salmon",
        ],
        ingredient_categories
    )

    assert result == "seasoned_ingredient"

def test_fresh_garlic_is_base_ingredient():
    result = classify_product(
        "fresh garlic",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "base_ingredient"


def test_frozen_broccoli_is_base_ingredient():
    result = classify_product(
        "frozen broccoli",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "base_ingredient"


def test_garlic_mashed_potatoes_is_prepared_food():
    result = classify_product(
        "garlic mashed potatoes",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "prepared_food"


def test_garlic_butter_is_seasoned_ingredient():
    result = classify_product(
        "garlic butter",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "seasoned_ingredient"

def test_chicken_and_broccoli_is_ambiguous():
    result = classify_product(
        "chicken and broccoli",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "ambiguous"


def test_chicken_and_rice_is_ambiguous():
    result = classify_product(
        "chicken and rice",
        keywords,
        known_ingredients,
        ingredient_categories
    )

    assert result == "ambiguous"