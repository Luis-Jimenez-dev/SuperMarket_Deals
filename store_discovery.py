import requests
import os
from dotenv import load_dotenv

load_dotenv()

safeway_api_key = os.getenv("SAFEWAY_API_KEY")

def extract_stores(data):
    stores = data['instore']['stores']
    nearby_stores = []

    for store in stores:
        store_data = {
            "name": store["domainName"],
            "merchant_store_code": store["locationId"],
            "address": store["address"]["line1"],
            "city": store["address"]["city"],
            "state": store["address"]["state"],
            "postal_code": store["address"]["zipcode"],
            "distance": store["distance"]
        }
        nearby_stores.append(store_data)

    return nearby_stores

def find_stores(zipcode):
    url = f"https://www.safeway.com/abs/pub/xapi/storeresolver/v2/all?zipcode={zipcode}&size=10&radius=50&excludeBanners=none&includeNonMigratedStores=true"
    header = {
        "ocp-apim-subscription-key": safeway_api_key
    }

    response = requests.get(url, headers = header)
    response.raise_for_status()

    data = response.json()

    return extract_stores(data)

def main():
    stores = find_stores("93907")

    for store in stores:
        print(store)

if __name__ == "__main__":
    main()