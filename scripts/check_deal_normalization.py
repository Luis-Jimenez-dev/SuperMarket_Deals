from pathlib import Path
import json

from normalization.deal_normalizer import normalize_many_deals


SAMPLE_PATH = Path(__file__).parent.parent / "data" / "safeway_sample.json"

def main():
    with open(SAMPLE_PATH, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # Handle either a raw list of products or a response containing products
    if isinstance(raw_data, list):
        raw_deals = raw_data
    else:
        raw_deals = raw_data.get("products", [])

    normalized = normalize_many_deals(raw_deals)

    matched_deals = [
        deal
        for deal in normalized["Food Deals"]
        if deal["canonical_ingredient"] is not None
    ]

    matched_deals.sort(
        key=lambda deal: (
            deal["canonical_ingredient"],
            deal["item"],
        )
    )

    print(f"\nFood deals: {len(normalized['Food Deals'])}")
    print(f"Canonical matches: {len(matched_deals)}\n")

    print("-" * 100)

    for deal in matched_deals:
        print(
            f"{deal['canonical_ingredient']:<20} | "
            f"{str(deal['category']):<15} | "
            f"{deal['item']}"
        )

    print("-" * 100)


if __name__ == "__main__":
    main()