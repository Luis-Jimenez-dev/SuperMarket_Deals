# Handles the connection to the PostgreSQL database and database queries
from datetime import datetime
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
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
def get_deals(store_id):
    cur.execute(
    """
    SELECT id
    FROM weekly_ads
    WHERE store_id = %s
    ORDER BY start_date DESC
    LIMIT 1
    """,
    (store_id,)
    )

    weekly_ad = cur.fetchone()
    if weekly_ad is None:
        return []

    weekly_ad_id = weekly_ad['id']

    cur.execute(
        """
        SELECT item, price, unit, category, category_path, promotion, description, 
        amount, min_amount, max_amount, package_count
        FROM deal_items
        WHERE deal_items.weekly_ad_id = %s
        """,
        (weekly_ad_id,)
    )

    deal_items = cur.fetchall()

    # PostgreSQL NUMERIC values are returned as Decimal, so convert prices to float
    for deal in deal_items:
        deal['price'] = float(deal['price'])

    return deal_items

def get_stores():
    cur.execute(
        """
        SELECT name, id, merchant_store_code, city, state, postal_code, address, latitude, longitude
        FROM stores
        """)
    stores = cur.fetchall()
    return stores

def _save_store(store):
    cur.execute(
        """
        INSERT INTO stores (name, brand, merchant_store_code, address, city, state, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (brand, merchant_store_code)
        DO UPDATE SET
        name = EXCLUDED.name, 
        address = EXCLUDED.address, 
        city = EXCLUDED.city, 
        state = EXCLUDED.state, 
        postal_code = EXCLUDED.postal_code
        RETURNING id
        """,(
            store['name'], store['brand'], store['merchant_store_code'], store['address'],
            store['city'], store['state'], store['postal_code']
        )
    )

    store_row = cur.fetchone()

    return store_row['id']

def save_stores(stores):
    for store in stores:
        store_id = _save_store(store)
        store.update({'store_id': store_id})

    conn.commit()

    return stores

def get_store_source_info(store_id):
    cur.execute(
        """
        SELECT merchant_store_code, postal_code
        FROM stores
        WHERE id = %s
        """,
        (store_id,)
    )
    store = cur.fetchone()

    if store is None:
        return None

    return store

def get_current_weekly_ad(store_id):
    cur.execute(
        """
        SELECT *
        FROM weekly_ads
        WHERE store_id = %s
        AND start_date <= CURRENT_DATE
        AND end_date >= CURRENT_DATE
        """,
        (store_id,)
    )

    weekly_ad = cur.fetchone()

    return weekly_ad

def save_weekly_ad(store_id, publication):
    source_publication_id = publication['id']
    start_date = datetime.fromisoformat(publication['valid_from']).date()
    end_date = datetime.fromisoformat(publication['valid_to']).date()

    cur.execute(
        """
        INSERT INTO weekly_ads(
            store_id,
            source_publication_id,
            start_date,
            end_date
        )
        VALUES(%s, %s, %s, %s)
        ON CONFLICT(store_id, source_publication_id)
        DO UPDATE SET
        start_date = EXCLUDED.start_date,
        end_date = EXCLUDED.end_date
        RETURNING id
        """,
        (store_id, source_publication_id, start_date, end_date)
    )

    weekly_ad_row = cur.fetchone()

    return(weekly_ad_row['id'])

def save_deals(deals, weekly_ad_id):
    for deal in deals:
        cur.execute(
            """
            INSERT INTO deal_items (
                weekly_ad_id,
                source_product_id,
                item,
                unit,
                category,
                category_path,
                price,
                promotion,
                description,
                amount,
                min_amount,
                max_amount,
                package_count
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (weekly_ad_id, source_product_id)
            DO NOTHING
            """,
            (
                weekly_ad_id,
                deal['source_product_id'],
                deal['item'],
                deal['unit'],
                deal['category'],
                Jsonb(deal['category_path']),
                deal['price'],
                deal['promotion'],
                deal['description'],
                deal['amount'],
                deal['min_amount'],
                deal['max_amount'],
                deal['package_count']
            )
        )