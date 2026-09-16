from fastapi import FastAPI
import database
import search_deals
import meal_plan

app = FastAPI()

@app.get("/")
def home ():
    return {"message": "Grocery API is running"}

@app.get("/stores/{store_name}/deals")
def store_deals(store_name):
    return database.get_deals(store_name);

@app.get("/stores/{store_name}/deals/search")
def search_store_deals(store_name, item):
    deals = database.get_deals(store_name)
    results = search_deals.search(deals, item)
    return results

@app.get("/stores/{store_name}/meal-plan")
def generate_meal_plan(store_name: str, meals: int):
    weekly_deals = database.get_deals(store_name)
    recipes = meal_plan.load_recipes()
    return meal_plan.generate(weekly_deals, recipes, meals)