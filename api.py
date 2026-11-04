# FastAPI routes for accessing grocery deals and meal planning features

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

import database
import search_deals
import meal_plan
import store_discovery
import safeway_deals
import requests


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
    try:
        safeway_deals.ensure_current_deals(store_id)
        return database.get_deals(store_id)

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Weekly deals are temporarily unavailable. Please try again in a moment."
        )

# Search through a selected store's weekly deals
@app.get("/stores/{store_id}/deals/search")
def search_store_deals(store_id, item):
    # Get the store's deals before searching for the requested item
    deals = database.get_deals(store_id)
    results = search_deals.search(deals, item)

    return results


# Generate meal recommendations using deals from the selected store
@app.get("/stores/{store_id}/meal-plan")
def generate_meal_plan(store_id: int, meals: int = Query(ge=1, le=14)):
    # Load the store's current deals and available recipes
    try:
        safeway_deals.ensure_current_deals(store_id)
        weekly_deals = database.get_deals(store_id)
        recipes = meal_plan.load_recipes()
        return meal_plan.generate(weekly_deals, recipes, meals)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code = 503,
            detail = "Meal planning is temporarily unavailable. Please try again in a moment."
        )

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

    try:
        stores = store_discovery.find_stores(postal_code)
        return database.save_stores(stores)
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code = 503,
            detail = "We couldn't search for stores right now. Please try again in a moment."
        )