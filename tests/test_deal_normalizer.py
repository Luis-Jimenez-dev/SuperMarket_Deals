from normalization.deal_normalizer import (
    get_price,
    normalize_deal,
    get_ingredient_info,
    is_usable_deal,
    is_food_deal
)
import pytest


@pytest.mark.parametrize("item_name", [
    None,
    "",
    "   ",
    123,
])
def test_invalid_item_name_does_not_match_ingredient(item_name):
    result = get_ingredient_info(item_name)

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


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
        "food_category_path": [
            "Food Items",
            "Meat, Seafood & Eggs"
        ]
    }

    assert is_food_deal(deal) is True

def test_food_service_category_is_not_food_deal():
    deal = {
        "food_category_path": [
            "Business & Industrial",
            "Food Service",
            "Disposable Tableware",
        ]
    }

    assert is_food_deal(deal) is False


def test_missing_food_category_path_is_not_food_deal():
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

def test_potato_chips_do_not_match_potato():
    result = get_ingredient_info(
        "Lay's Potato Chips"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_yogurt_does_not_match_sugar():
    result = get_ingredient_info(
        "Chobani Greek, Less Sugar or Zero Sugar Yogurt"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_ice_cream_does_not_match_cream():
    result = get_ingredient_info(
        "Jeni's Splendid Ice Cream"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_pizza_does_not_match_cheese():
    result = get_ingredient_info(
        "Tattooed Chef Cottage Cheese Pizza"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_bell_pepper_does_not_match_seasoning_pepper():
    result = get_ingredient_info(
        "Red, Orange, Yellow or Green Bell Pepper"
    )

    assert result["canonical_ingredient"] == "bell pepper"
    assert result["ingredient_category"] == "vegetable"

def test_pot_pie_does_not_match_chicken():
    result = get_ingredient_info("Chicken or Turkey Pot Pie")

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None

def test_chicken_tenderloins_can_still_match_chicken():
    result = get_ingredient_info("Fresh Boneless Chicken Tenderloins")

    assert result["canonical_ingredient"] is not None

def test_prepared_chicken_tenders_do_not_match_chicken():
    result = get_ingredient_info(
        "Chicken Tenders Original or Nashville Hot., "
        "BBQ Rib Tips Available in the Deli., "
        "Tater Kegs Original."
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None


def test_low_carb_prepared_chicken_does_not_match_chicken():
    result = get_ingredient_info(
        "Real Good Foods Low Carb Chicken"
    )

    assert result["canonical_ingredient"] is None
    assert result["ingredient_category"] is None