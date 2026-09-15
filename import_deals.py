import json
import database

with open ("data/nob_hill/weekly_deals.json", 'r', encoding='utf-8') as file:
    deals = json.load(file)

database.cur.execute(
    """
    INSERT INTO weekly_ads (store_id, start_date, end_date)
    VALUES (%s, %s, %s)
    """,
    (3, '2026-09-09', '2026-09-15'),
)

database.conn.commit()

# store_name = "Nob Hill"

# database.cur.execute(
#     """
#     SELECT weekly_ads.id FROM weekly_ads JOIN stores ON weekly_ads.store_id = stores.id WHERE stores.name ILIKE %s
#     """,
#     (store_name,)
# )

# weekly_ad_id = database.cur.fetchone()
# weekly_ad_id = weekly_ad_id['id']

# print (weekly_ad_id)

# for deal in deals:
#     database.cur.execute (
#         """
#         INSERT INTO deal_items (weekly_ad_id, item, unit, category, price)
#         VALUES (%s, %s, %s, %s, %s)
#         ON CONFLICT DO NOTHING
#         """,
#         (weekly_ad_id, deal['item'], deal['unit'], deal['category'], deal ['price'])
#     )

# database.conn.commit()