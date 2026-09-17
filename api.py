# FastAPI routes for accessing grocery deals and meal planning features

from fastapi import FastAPI

import database
import search_deals
import meal_plan


# Create the FastAPI application
app = FastAPI()


# Basic route to check that the API is running
@app.get("/")
def home():
    return {"message": "Grocery API is running"}


# Get all weekly deals for a selected store
@app.get("/stores/{store_name}/deals")
def store_deals(store_name):
    return database.get_deals(store_name)


# Search through a selected store's weekly deals
@app.get("/stores/{store_name}/deals/search")
def search_store_deals(store_name, item):
    # Get the store's deals before searching for the requested item
    deals = database.get_deals(store_name)
    results = search_deals.search(deals, item)

    return results


# Generate meal recommendations using deals from the selected store
@app.get("/stores/{store_name}/meal-plan")
def generate_meal_plan(store_name: str, meals: int):
    # Load the store's current deals and available recipes
    weekly_deals = database.get_deals(store_name)
    recipes = meal_plan.load_recipes()

    return meal_plan.generate(weekly_deals, recipes, meals)