from normalization.deal_normalizer import (
    get_price,
    get_package_info,
    normalize_deal,
    get_ingredient_info,
    is_usable_deal,
    is_food_deal
)


def test_get_regular_price():
    raw_deal = {
        "price_text": "5.99",
        "pre_price_text": ""
    }

    assert get_price(raw_deal) == 5.99


def test_get_multi_item_price():
    raw_deal = {
        "price_text": "10.00",
        "pre_price_text": "2 for"
    }

    assert get_price(raw_deal) == 5.00


def test_missing_price_returns_none():
    raw_deal = {}

    assert get_price(raw_deal) is None


def test_none_price_returns_none():
    raw_deal = {
        "price_text": None
    }

    assert get_price(raw_deal) is None


def test_usable_deal_requires_price():
    assert is_usable_deal({"price": 4.99}) is True
    assert is_usable_deal({"price": None}) is False


def test_food_deal():
    deal = {
        "category_path": [
            "Food Items",
            "Meat, Seafood & Eggs"
        ]
    }

    assert is_food_deal(deal) is True


def test_non_food_deal():
    deal = {
        "category_path": [
            "Household",
            "Cleaning Supplies"
        ]
    }

    assert is_food_deal(deal) is False

def test_get_ingredient_info_chicken_breast():
    result = get_ingredient_info(
        "Signature Farms Boneless Skinless Chicken Breasts"
    )

    assert result["canonical_ingredient"] == "chicken breast"
    assert result["ingredient_category"] == "poultry"


def test_get_ingredient_info_unknown_product():
    result = get_ingredient_info(
        "Mystery Grocery Product XYZ"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_normalize_deal_preserves_original_item_name():
    original_name = (
        "Signature Farms Boneless Skinless Chicken Breasts"
    )

    raw_deal = {
        "id": "12345",
        "name": original_name,
        "price_text": "5.99",
        "pre_price_text": "",
        "post_price_text": "Sale",
        "description": "3 lb",
        "categories": [
            {"name": "Food Items"},
            {"name": "Meat"},
            {"name": "Chicken"},
        ],
    }

    result = normalize_deal(raw_deal)

    assert result["item"] == original_name
    assert result["canonical_ingredient"] == "chicken breast"
    assert result["ingredient_category"] == "poultry"