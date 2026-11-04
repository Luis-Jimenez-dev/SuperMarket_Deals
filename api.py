# FastAPI routes for accessing grocery deals and meal planning features

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import database
import search_deals
import meal_plan
import store_discovery
import safeway_deals


# Create the FastAPI application
app = FastAPI()
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


# Basic route to check that the API is running
@app.get("/")
def home():
    return {"message": "Grocery API is running"}


# Get all weekly deals for a selected store
@app.get("/stores/{store_id}/deals")
def store_deals(store_id: int):
    safeway_deals.ensure_current_deals(store_id)
    return database.get_deals(store_id)


# Search through a selected store's weekly deals
@app.get("/stores/{store_name}/deals/search")
def search_store_deals(store_name, item):
    # Get the store's deals before searching for the requested item
    deals = database.get_deals(store_name)
    results = search_deals.search(deals, item)

    return results


# Generate meal recommendations using deals from the selected store
@app.get("/stores/{store_id}/meal-plan")
def generate_meal_plan(store_id: int, meals: int):
    # Load the store's current deals and available recipes
    safeway_deals.ensure_current_deals(store_id)
    weekly_deals = database.get_deals(store_id)
    recipes = meal_plan.load_recipes()

    return meal_plan.generate(weekly_deals, recipes, meals)

@app.get("/stores")
def get_stores():
    return database.get_stores()

@app.get("/stores/nearby")
def get_nearby_stores(
        postal_code: str = 
        Query(
            min_length=5, 
            max_length=5, 
            pattern=r"^\d{5}$"
        )
    ):
    stores = store_discovery.find_stores(postal_code)
    return database.save_stores(stores)
