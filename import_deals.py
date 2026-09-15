import json
import database
import store_search

def import_deals():
    store_name = input ("Input Store Name: ")
    deals = store_search.search(store_name)

    if deals is None:
        print ("No deals found for this store.")
        return

    database.cur.execute(
        """
        SELECT weekly_ads.id FROM weekly_ads JOIN stores ON weekly_ads.store_id = stores.id WHERE stores.name ILIKE %s
        """,
        (f"%{store_name}%",)
    )

    weekly_ad_id = database.cur.fetchone()
    weekly_ad_id = weekly_ad_id['id']

    print (weekly_ad_id)

    for deal in deals:
        database.cur.execute (
            """
            INSERT INTO deal_items (weekly_ad_id, item, unit, category, price)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (weekly_ad_id, deal['item'], deal['unit'], deal['category'], deal ['price'])
        )

    database.conn.commit()

# if __name__ == "__main__":
#     import_deals()