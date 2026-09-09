import psycopg
from psycopg.rows import dict_row
import os

conn = psycopg.connect(
    dbname = "grocery_app",
    user = "postgres",
    password = os.getenv("GROCERY_DB_PASSWORD"),
    host = "localhost",
    port = 5432
)

cur = conn.cursor(row_factory=dict_row)



def get_deals(store_name):
    cur.execute(
        """
        SELECT deal_items.item, deal_items.price, deal_items.unit, deal_items.category
        FROM deal_items JOIN weekly_ads ON deal_items.weekly_ad_id = weekly_ads.id
        JOIN stores on weekly_ads.store_id = stores.id WHERE name ILIKE %s
        """,
        (store_name,)
    )
    deal_items = cur.fetchall()

    for deal in deal_items:
        deal['price'] = float(deal['price'])
    
    return (deal_items)
