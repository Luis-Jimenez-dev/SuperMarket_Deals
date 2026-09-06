import json
from pathlib import Path


def search(answer):
    data_folder = Path("data")
    deals = None

    for item in data_folder.iterdir():
        if answer.lower() in item.name.lower():
            item = item/'weekly_deals.json'
            with open(item, 'r', encoding='utf-8') as file:
                deals = json.load(file)

    return (deals)