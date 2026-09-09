import json
import database

with open ("data/safeway/weekly_deals.json", 'r', encoding='utf-8') as file:
    deals = json.load(file)

for deal in deals:
    database.cur.execute (
        """
        INSERT INTO deal_items (weekly_ad_id, item, unit, category, price)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
        (1, deal['item'], deal['unit'], deal['category'], deal ['price'])
    )

database.conn.commit()