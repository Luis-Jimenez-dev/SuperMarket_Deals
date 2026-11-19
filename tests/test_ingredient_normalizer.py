from rework_normalization.ingredient_normalizer import (
    find_ingredients,
    get_ingredient_category,
    categorize_ingredients,
)

def test_find_ingredeints():
    result = find_ingredients("garlic butter shrimp",
                              ["chicken", "garlic", "butter", "shrimp"])
    assert result == ["garlic", "butter", "shrimp"]

def test_find_no_overlapping_ingredients():
    result = find_ingredients("boneless skinless chicken breast",
                              ["chicken", "chicken breast"])
    assert result == ["chicken breast"]

def test_best_matches_with_overlap():
    result = find_ingredients ("chicken breast with garlic and butter",
                               ["chicken", "chicken breast", "garlic", "butter"])
    assert result == ["chicken breast", "garlic", "butter"]

def test_salmon_category():
    result = get_ingredient_category("salmon", {
        "chicken breast": "protein",
        "salmon": "protein",
        "broccoli": "vegetable",
        "garlic": "aromatic",
        "butter": "fat",
        "honey": "sweetener",
        "flour": "baking",
        "milk": "dairy",
        "rice": "grain",
        "basil": "herb",
    })

    assert result == "protein"

def test_garlic_category():
    result = get_ingredient_category("garlic", {
        "chicken breast": "protein",
        "salmon": "protein",
        "broccoli": "vegetable",
        "garlic": "aromatic",
        "butter": "fat",
        "honey": "sweetener",
        "flour": "baking",
        "milk": "dairy",
        "rice": "grain",
        "basil": "herb",
    })

    assert result == "aromatic"

def test_unknown_category():
    result = get_ingredient_category("unknown", {
        "chicken breast": "protein",
        "salmon": "protein",
        "broccoli": "vegetable",
        "garlic": "aromatic",
        "butter": "fat",
        "honey": "sweetener",
        "flour": "baking",
        "milk": "dairy",
        "rice": "grain",
        "basil": "herb",
    })

    assert result == None

def test_catagorize_ingredients():
    result = categorize_ingredients(["honey", "garlic", "salmon"], {
        "honey": "sweetner",
        "garlic": "aromatic",
        "salmon": "protein"
    })

    assert result == [("honey", "sweetner"), ("garlic", "aromatic"), ("salmon", "protein")]

def test_catagorize_unknown_ingredient():
    result = categorize_ingredients(["garlic", "mystery", "salmon"], {
        "honey": "sweetner",
        "garlic": "aromatic",
        "salmon": "protein"
    })

    assert result == [("garlic", "aromatic"), ("mystery", None), ("salmon", "protein")]