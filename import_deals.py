# Imports grocery deals from a selected store into the PostgreSQL database

import json
import database
import store_search


# Find a store's deals and add them to its weekly ad in the database
def import_deals(deals, start_date, end_date):
    store_name = input("Input Store Name: ")

    if deals is None:
        print("No deals found for this store.")
        return

    # Find the weekly ad ID connected to the selected store
    database.cur.execute(
        """
        SELECT weekly_ads.id
        FROM weekly_ads
        JOIN stores ON weekly_ads.store_id = stores.id
        WHERE stores.name ILIKE %s
        AND weekly_ads.start_date = %s
        AND weekly_ads.end_date = %s
        """,
        (
        f"%{store_name}%",
        start_date,
        end_date
        )
    )

    weekly_ad = database.cur.fetchone()

    if weekly_ad is None:
        print ("Weekly ad not found")
        return
    weekly_ad_id = weekly_ad['id']

    print(weekly_ad_id)

    # Add each deal to the store's weekly ad
    for deal in deals:
        database.cur.execute(
            """
            INSERT INTO deal_items 
            (weekly_ad_id, item, unit, category, price, 
            promotion, description, amount, min_amount, max_amount, package_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                weekly_ad_id,
                deal['item'],
                deal['unit'],
                deal['category'],
                deal['price'],
                deal['promotion'],
                deal['description'],
                deal['amount'],
                deal['min_amount'],
                deal['max_amount'],
                deal['package_count']   
            )
        )

    # Save all inserted deals to the database
    database.conn.commit()


# Run the importer directly when this file is executed
# if __name__ == "__main__":
#     import_deals()