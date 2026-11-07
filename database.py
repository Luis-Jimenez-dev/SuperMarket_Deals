# Handles the connection to the PostgreSQL database and database queries
from datetime import datetime
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool
import os
from dotenv import load_dotenv


# Load database settings from the .env file
load_dotenv()


# Connect to the Supabase PostgreSQL database using environment variables
database_url = (
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"password={os.getenv('DB_PASSWORD')} "
    f"host={os.getenv('DB_HOST')} "
    f"port={os.getenv('DB_PORT')} "
    f"sslmode=require"
)

pool = ConnectionPool(
    conninfo = database_url,
    min_size = 1,
    max_size = 5
)


# Get the weekly deals for the selected store
def get_deals(store_id):
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            cur.execute(
                """
                SELECT id
                FROM weekly_ads
                WHERE store_id = %s
                AND start_date <= CURRENT_DATE
                AND end_date >= CURRENT_DATE
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
                SELECT id, source_product_id, item, price, unit, category, category_path, promotion, description, 
                amount, min_amount, max_amount, package_count, canonical_ingredient
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
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            cur.execute(
                """
                SELECT name, id, merchant_store_code, city, state, postal_code, address, latitude, longitude
                FROM stores
                """)
            stores = cur.fetchall()
            return stores

def _save_store(store, cur):
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
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            for store in stores:
                store_id = _save_store(store, cur)
                store.update({'store_id': store_id})
    return stores

def get_store_source_info(store_id):
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
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
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
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

def _save_weekly_ad(store_id, publication, cur):
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

def _save_deals(deals, weekly_ad_id, cur):
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
                package_count,
                canonical_ingredient
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (weekly_ad_id, source_product_id)
            DO UPDATE SET
                item = EXCLUDED.item,
                unit = EXCLUDED.unit,
                category = EXCLUDED.category,
                category_path = EXCLUDED.category_path,
                price = EXCLUDED.price,
                promotion = EXCLUDED.promotion,
                description = EXCLUDED.description,
                amount = EXCLUDED.amount,
                min_amount = EXCLUDED.min_amount,
                max_amount = EXCLUDED.max_amount,
                package_count = EXCLUDED.package_count,
                canonical_ingredient = EXCLUDED.canonical_ingredient
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
                deal['package_count'],
                deal['canonical_ingredient']
            )
        )

def save_weekly_ad_with_deals(store_id, publication, deals):
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            weekly_ad_id = _save_weekly_ad(store_id, publication, cur)
            _save_deals(deals, weekly_ad_id, cur)

def _save_recipe (recipe, cur):
    cur.execute(
        """
        INSERT INTO recipes (
            source,
            source_recipe_id,
            name,
            instructions,
            image_url,
            servings,
            cuisine,
            category
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (source, source_recipe_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            instructions = EXCLUDED.instructions,
            image_url = EXCLUDED.image_url,
            servings = EXCLUDED.servings,
            cuisine = EXCLUDED.cuisine,
            category = EXCLUDED.category

        RETURNING id
        """,
        (
            recipe['source'],
            recipe['source_recipe_id'],
            recipe['name'],
            recipe['instructions'],
            recipe['image_url'],
            None,
            recipe['cuisine'],
            recipe['category']
        )
    )

    recipe_row = cur.fetchone()

    return recipe_row['id']

def _save_recipe_ingredients(recipe_id, ingredients, cur):
    cur.execute(
        """
        DELETE FROM recipe_ingredients
        WHERE recipe_id = %s
        """,
        (recipe_id,)
    )
        
    for ingredient in ingredients:
        cur.execute(
            """
            INSERT INTO recipe_ingredients (
                recipe_id,
                name,
                measurement
            )
            VALUES (%s, %s, %s)
            """,
            (
                recipe_id,
                ingredient['name'],
                ingredient['measurement']
            )
        )

def save_recipe(recipe):
    with pool.connection() as conn:
        with conn.cursor(row_factory = dict_row) as cur:
            recipe_id = _save_recipe(recipe, cur)
            _save_recipe_ingredients(recipe_id, recipe['ingredients'], cur)
            return recipe_id
        
def get_recipes():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    r.id,
                    r.source,
                    r.source_recipe_id,
                    r.name,
                    r.instructions,
                    r.image_url,
                    r.servings,
                    r.cuisine,
                    r.category,
                    ri.name AS ingredient_name,
                    ri.measurement
                FROM recipes r
                JOIN recipe_ingredients ri
                    ON r.id = ri.recipe_id
                ORDER BY r.id
                """
            )

            rows = cur.fetchall()

            recipes = {}

            for row in rows:
                recipe_id = row['id']

                if recipe_id not in recipes:
                    recipes[recipe_id] = {
                        "id": recipe_id,
                        "source" : row['source'],
                        "source_recipe_id" : row['source_recipe_id'],
                        "name" : row['name'],
                        "instructions": row['instructions'],
                        "image_url" : row['image_url'],
                        "servings" : row['servings'],
                        "cuisine" : row['cuisine'],
                        "category" : row['category'],
                        "ingredients": [{
                            'name': row['ingredient_name'],
                            'measurement' : row['measurement']
                        }]
                    }
                else:
                    recipes[recipe_id]['ingredients'].append({
                        'name': row['ingredient_name'],
                        'measurement': row['measurement']
                    })

            return list(recipes.values())
