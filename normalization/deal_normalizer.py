import re

from normalization.text_normalizer import (
    find_best_known_term,
    get_canonical_term,
)
from normalization.ingredient_normalizer import classify_canonical_ingredient

NON_INGREDIENT_PRODUCT_PHRASES = {
    "potato chips",
    "ice cream",
    "pizza",
    "yogurt",
}


def get_ingredient_info(item_name):
    """
    Identify a canonical recipe ingredient represented by a retailer deal.

    Deal names are treated conservatively because a known ingredient word
    can appear inside a different prepared or packaged product.
    """
    if contains_non_ingredient_product_phrase(item_name):
        return {
            "canonical_ingredient": None,
            "ingredient_category": None,
        }

    matched_term = find_best_known_term(item_name)

    if matched_term is None:
        return {
            "canonical_ingredient": None,
            "ingredient_category": None,
        }

    canonical_ingredient = get_canonical_term(matched_term)

    if canonical_ingredient is None:
        return {
            "canonical_ingredient": None,
            "ingredient_category": None,
        }

    ingredient_category = classify_canonical_ingredient(
        canonical_ingredient
    )

    return {
        "canonical_ingredient": canonical_ingredient,
        "ingredient_category": ingredient_category,
    }

def normalize_deal(raw_deal):
    price = get_price(raw_deal)

    category_path = get_category(raw_deal)
    category = category_path[-1] if category_path else None

    food_category_path = get_food_category_path(raw_deal)

    package_info = get_package_info(raw_deal.get("description")) or {}

    ingredient_info = get_ingredient_info(
        raw_deal.get("name", "")
    )

    deal = {
        "source_product_id": raw_deal["id"],

        # Original retailer name is preserved for display.
        "item": raw_deal["name"],

        # Internal values used for recipe/deal matching.
        "canonical_ingredient": ingredient_info["canonical_ingredient"],
        "ingredient_category": ingredient_info["ingredient_category"],

        "price": price,
        "promotion": raw_deal.get("post_price_text"),

        # Retailer-provided category information.
        "category": category,
        "category_path": category_path,

        # Structured Flipp/Google category hierarchy.
        "food_category_path": food_category_path,

        "description": raw_deal.get("description"),

        "amount": package_info.get("amount"),
        "min_amount": package_info.get("min_amount"),
        "max_amount": package_info.get("max_amount"),
        "package_count": package_info.get("package_count"),
        "unit": package_info.get("unit"),
    }

    return deal


def get_price(raw_deal):
    try:
        price = float(raw_deal["price_text"])
    except (KeyError, ValueError, TypeError):
        return None

    pre_price_text = raw_deal.get("pre_price_text")

    if pre_price_text and "for" in pre_price_text.lower():
        try:
            parts = pre_price_text.lower().split("for")
            quantity = int(parts[0].strip())

            if quantity > 0:
                price = price / quantity

        except (ValueError, TypeError, ZeroDivisionError):
            pass

    return price


def get_category(raw_deal):
    """
    Preserve the retailer-facing categories supplied by Flipp.
    Example: ["Deli"]
    """
    categories = raw_deal.get("categories")

    if not categories:
        return []

    category_path = []

    for category in categories:
        if isinstance(category, dict):
            name = category.get("name")

            if name:
                category_path.append(name)

        elif isinstance(category, str):
            category_path.append(category)

    return category_path


def get_food_category_path(raw_deal):
    """
    Extract the structured Flipp/Google category hierarchy.

    Example:
    Food, Beverages & Tobacco
        -> Food Items
        -> Meat, Seafood & Eggs
        -> Meat
        -> Fresh & Frozen Meats
    """
    item_categories = raw_deal.get("item_categories") or {}

    category_path = []

    # Flipp currently provides levels such as l1, l2, l3, etc.
    for level_number in range(1, 8):
        level = item_categories.get(f"l{level_number}")

        if not isinstance(level, dict):
            continue

        category_name = level.get("category_name")

        if category_name:
            category_path.append(category_name)

    return category_path


def is_valid_unit(unit):
    if unit is None:
        return False

    valid_units = {
        "oz",
        "lbs",
        "lb",
        "ml",
        "qt",
        "ct",
    }

    return unit.lower() in valid_units


def get_package_info(description):
    if not description:
        return None

    description = description.lower()

    package_match = re.search(
        r"(\d+)\s*(?:pack|pk)\s*[-x]?\s*(\d+(?:\.\d+)?)\s*(oz|lbs|lb|ml|qt|ct)",
        description,
    )

    if package_match:
        package_count = int(package_match.group(1))
        amount = float(package_match.group(2))
        unit = package_match.group(3)

        if is_valid_unit(unit):
            return {
                "amount": amount,
                "min_amount": None,
                "max_amount": None,
                "package_count": package_count,
                "unit": unit,
            }

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(oz|lbs|lb|ml|qt|ct)",
        description,
    )

    if range_match:
        min_amount = float(range_match.group(1))
        max_amount = float(range_match.group(2))
        unit = range_match.group(3)

        if is_valid_unit(unit):
            return {
                "amount": None,
                "min_amount": min_amount,
                "max_amount": max_amount,
                "package_count": None,
                "unit": unit,
            }

    single_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(oz|lbs|lb|ml|qt|ct)",
        description,
    )

    if single_match:
        amount = float(single_match.group(1))
        unit = single_match.group(2)

        if is_valid_unit(unit):
            return {
                "amount": amount,
                "min_amount": None,
                "max_amount": None,
                "package_count": None,
                "unit": unit,
            }

    return None


def is_usable_deal(deal):
    return deal.get("price") is not None


def is_food_deal(deal):
    """
    Determine whether the deal represents food using the structured
    Flipp/Google category hierarchy.
    """
    food_category_path = deal.get("food_category_path") or []

    return "Food Items" in food_category_path


def normalize_many_deals(raw_deals):
    usable_deals = []
    food_deals = []
    other_deals = []

    for raw_deal in raw_deals:
        deal = normalize_deal(raw_deal)

        if not is_usable_deal(deal):
            continue

        usable_deals.append(deal)

        if is_food_deal(deal):
            food_deals.append(deal)
        else:
            other_deals.append(deal)

    return {
        "Usable Deals": usable_deals,
        "Food Deals": food_deals,
        "Other Deals": other_deals,
    }

def contains_non_ingredient_product_phrase(item_name):
    normalized_name = item_name.lower()

    for phrase in NON_INGREDIENT_PRODUCT_PHRASES:
        pattern = rf"\b{re.escape(phrase)}\b"

        if re.search(pattern, normalized_name):
            return True

    return False