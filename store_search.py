# Finds and loads weekly deal data stored locally for a selected store

import json
from pathlib import Path


# Search the data folder for a store and load its weekly deals
def search(answer):
    data_folder = Path("data")
    deals = None

    # Check each store folder for a name matching the user's search
    for item in data_folder.iterdir():

        # Normalize spaces and periods so names like "Foods CO." can still match
        if answer.lower().replace(" ", "_").replace(".", "") in item.name.lower():
            item = item / 'weekly_deals.json'

            # Load the store's weekly deals from its JSON file
            with open(item, 'r', encoding='utf-8') as file:
                deals = json.load(file)

    return deals