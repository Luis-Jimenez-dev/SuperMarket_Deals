import json
import re
import import_deals

with open ('data/safeway_sample.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Used for a single deal
def normalize_deal(raw_deal):
    price = get_price(raw_deal)
    category_path = get_category(raw_deal)
    if category_path:
        category = category_path[-1]
    else:
        category = None

    package_info = get_package_info(raw_deal.get('description')) or {}

    amount = package_info.get('amount')
    min_amount = package_info.get('min_amount')
    max_amount = package_info.get('max_amount')
    package_count = package_info.get('package_count')
    unit = package_info.get('unit')

    deal = {
        'item': raw_deal['name'],
        'price': price,
        'promotion': raw_deal['post_price_text'],
        'category': category,
        'category_path': category_path,
        'description': raw_deal['description'],
        'amount': amount,
        'min_amount': min_amount,
        'max_amount': max_amount,
        'package_count': package_count,
        'unit': unit
    }



    return deal

def get_category(raw_deal):
    categories = raw_deal.get('item_categories', {})

    category_path = []

    for level in categories.values():
        if level is not None and level.get('category_name') is not None:
            category_path.append(level['category_name'])

    return category_path

def get_price(raw_deal):
    try:
        price = float(raw_deal['price_text'])
    except (KeyError, ValueError):
        return None

    pre_price_text = raw_deal.get('pre_price_text', '')

    if 'for' in pre_price_text:
        parts = pre_price_text.split()
        quantity = int(parts[0])
        price = price / quantity

    return price

def is_valid_unit(unit):
    valid_units = {'oz', 'lbs', 'lb', 'ml', 'qt', 'ct' }
    if unit in valid_units:
        return True
    else:
        return False

def get_package_info(description):

    if description is None:
        return None

    match = re.search(r"(\d+(?:\.\d+)?)\s*\-\s*([a-zA-Z]+)", description)
    range_match = re.search(r"(\d+(?:\.\d+)?)\s*to\s*(\d+(?:\.\d+)?)\s*\-\s*([a-zA-Z]+)", description)
    pack_match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*pack,\s*(\d+(?:\.\d+)?)\s*-\s*([a-zA-Z]+)", description)
    if pack_match and is_valid_unit(pack_match.group(3)):
        return {
                'package_count': int(pack_match.group(1)), 
                'amount': float(pack_match.group(2)), 
                'unit': pack_match.group(3)
                }
    elif range_match and is_valid_unit(range_match.group(3)):
        return {'min_amount': float(range_match.group(1)), 'max_amount': float(range_match.group(2)), 'unit': range_match.group(3)}
    elif match and is_valid_unit(match.group(2)):
        return {'amount': float(match.group(1)), 'unit': match.group(2)}


def is_usable_deal(deal):
    if deal.get('price') is None:
        return False
    else:
        return True

def is_food_deal(deal):
    category_path = deal.get('category_path', [])

    if 'Food Items' in category_path:
        return True

    return False

def normalize_many_deals(raw_deals):
    usable_deals = []
    food_deals = []
    other_deals = []

    for raw_deal in raw_deals:
        normalized_deal = normalize_deal(raw_deal)
        if is_usable_deal(normalized_deal):
            usable_deals.append(normalized_deal)
            if is_food_deal(normalized_deal):
                food_deals.append(normalized_deal)
            else:
                other_deals.append(normalized_deal)

    return ({
        'Usable Deals': usable_deals,
        'Food Deals': food_deals,
        'Other Deals': other_deals
    })

results = normalize_many_deals(data)
food_deals = results['Food Deals']

import_deals.import_deals(food_deals, '2026-09-16', '2026-09-22')