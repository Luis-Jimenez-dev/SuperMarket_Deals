# Handles the connection to the PostgreSQL database and database queries

import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv


# Load database settings from the .env file
load_dotenv()


# Connect to the Supabase PostgreSQL database using environment variables
conn = psycopg.connect(
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT"),
    sslmode = "require"
)

# Return database rows as dictionaries instead of tuples
cur = conn.cursor(row_factory=dict_row)


# Get the weekly deals for the selected store
def get_deals(store_name):
    cur.execute(
        """
        SELECT deal_items.item, deal_items.price, deal_items.unit, deal_items.category
        FROM deal_items
        JOIN weekly_ads ON deal_items.weekly_ad_id = weekly_ads.id
        JOIN stores ON weekly_ads.store_id = stores.id
        WHERE name ILIKE %s
        """,
        (store_name,)
    )

    deal_items = cur.fetchall()

    # PostgreSQL NUMERIC values are returned as Decimal, so convert prices to float
    for deal in deal_items:
        deal['price'] = float(deal['price'])

    return deal_items