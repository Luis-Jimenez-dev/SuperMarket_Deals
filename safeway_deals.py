import requests
import database
import deal_normalizer
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def ensure_current_deals(store_id):
    weekly_ad = database.get_current_weekly_ad(store_id)
    if weekly_ad is None:
        sync_current_deals(store_id)

def get_publications(store_id):
    store_info = database.get_store_source_info(store_id)

    if store_info is None:
        return None

    merchant_store_code = store_info['merchant_store_code']
    postal_code = store_info['postal_code']

    params = {
        "access_token": os.getenv("FLIPP_ACCESS_TOKEN"),
        "locale": "en-US",
        "postal_code": postal_code,
        "store_code": merchant_store_code
    }

    url = "https://api.flipp.com/flyerkit/v4.0/publications/safeway"

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()
    return data

def get_publication_products(publication_id):
    params = {
        "display_type": 'all',
        "locale": 'en',
        "access_token": os.getenv("FLIPP_ACCESS_TOKEN")
    }

    url = f"https://dam.flippenterprise.net/hosted/publication/{publication_id}/products"

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()
    return data

def get_current_publication(publications):

    for publication in publications:
        start_date = datetime.fromisoformat(publication['valid_from'])
        end_date = datetime.fromisoformat(publication['valid_to'])
        current_date = datetime.now(start_date.tzinfo)

        if start_date <= current_date and current_date <= end_date:
            return publication

    return None

def sync_current_deals(store_id):
    publications = get_publications(store_id)
    if publications is None:
        return None
    
    current_publication = get_current_publication(publications)
    if current_publication is None:
        return None

    publication_id = current_publication['id']

    products = get_publication_products(publication_id)
    results = deal_normalizer.normalize_many_deals(products)
    food_deals = results['Food Deals']

    database.save_weekly_ad_with_deals(store_id, current_publication, food_deals)