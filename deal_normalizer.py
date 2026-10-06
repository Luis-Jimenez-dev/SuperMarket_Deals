import json
import re

with open ('data/safeway_sample.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def normalize_deal(raw_deal):
    price = get_price(raw_deal)
    category = get_category(raw_deal)

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

    category = None

    for level in categories.values():
        if level is not None and level.get('category_name') is not None:
            category = level['category_name']

    return category

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
total = 0
with_price = 0
with_category = 0
without_category = 0
without_price = 0


for raw_deal in data:
    price = get_price(raw_deal)
    category = get_category(raw_deal)
    description = raw_deal.get('description')

    total += 1
    if price is None:
        without_price += 1
    else:
        with_price += 1

    if category is None:
        without_category += 1
    else:
        with_category += 1

    if description is not None:
        normalized_deal = normalize_deal(raw_deal)
        print(normalized_deal)

print (
f"""
Total: {total}
With price: {with_price}
Without price: {without_price}
With Category: {with_category}
Without Category: {without_category}
"""
)
# get_package_info(raw_deal)
