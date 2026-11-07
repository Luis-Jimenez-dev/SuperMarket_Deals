# SuperMarket Deals

SuperMarket Deals started as a Python command-line project for answering a question I run into every week: what can I cook based on what is actually on sale?

The first version used local JSON files and a small list of recipes. Since then, I have been rebuilding it as a web application that pulls current grocery deals, stores them in PostgreSQL, matches those deals against recipe ingredients, and recommends meals based on the matches it finds.

The project is still in development. Safeway is currently the retailer I use for testing.

## What it does

A user enters a ZIP code and chooses a nearby store. The backend gets the store's current weekly ad and saves its deals to the database.

Those deals can then be browsed in the React frontend or used to generate a meal plan.

For meal planning, the backend compares the ingredients in each recipe against ingredients identified in the current weekly deals. Recipes with more discounted ingredients are ranked higher.

The generated meal plan shows:

- Recipes that match the current deals
- Which recipe ingredients are on sale
- The grocery product associated with each match
- The sale price
- Ingredients that are still needed
- A combined shopping list for the selected meals

## Current flow

```text
ZIP code
   |
   v
Nearby Safeway stores
   |
   v
Selected store
   |
   v
Current weekly ad
   |
   v
Normalized grocery deals
   |
   +--------------------+
   |                    |
   v                    v
Browse deals       Match recipes
                        |
                        v
                  Rank recipes
                        |
                        v
                   Meal plan
                        |
                        v
                  Shopping list
```

## Grocery data

The grocery side of the project currently uses Safeway publication data retrieved through Flipp endpoints.

When a store is selected, the backend checks PostgreSQL for a weekly ad that is still valid for that store.

If a current ad already exists, the existing data is reused.

If the previous ad has expired, the backend looks for the current publication, retrieves its products, normalizes the usable food deals, and saves the new weekly ad and its deal items.

Weekly ads are identified using the source publication ID so the same publication can be updated without creating duplicate records.

## Recipes

Recipes currently come from [TheMealDB](https://www.themealdb.com/).

The import code retrieves the full recipe information, extracts its ingredients and measurements, and stores the results in PostgreSQL.

The current database contains 452 recipes across:

- Beef
- Chicken
- Pork
- Seafood
- Vegetarian
- Pasta
- Breakfast

Recipes are stored separately from their ingredients so they can be queried and reconstructed from the database when a meal plan is generated.

## Ingredient matching

One of the harder parts of this project has been dealing with the different ways the same ingredient can be written.

A recipe might contain:

```text
Chicken Breasts
```

while a grocery deal might be listed as:

```text
Boneless Skinless Chicken Breast
```

Simple string equality would treat those as different ingredients.

The normalization code uses a grocery vocabulary containing canonical ingredient names and their known aliases. Text is cleaned and normalized before known terms are identified.

For example:

```text
chicken breasts
       |
       v
chicken breast
       |
       v
canonical ingredient: chicken breast
```

The vocabulary currently contains 370 canonical ingredients.

I also keep ingredient categories separate from the vocabulary. This allows an ingredient such as `chicken breast` to have a canonical identity while also belonging to a broader category such as `poultry`.

Unknown ingredients are left unmatched instead of forcing them into a category that may be wrong.

The current recipe ingredient audit recognizes 99.88% of the ingredient uses in the recipe database.

## Avoiding bad grocery matches

Finding a known ingredient word inside a grocery product does not automatically mean the product should count as that ingredient.

For example, a product containing the word `chicken` could be raw chicken, but it could also be a prepared meal or another packaged product.

`non_ingredient_products.json` contains phrases used to reject known false positives before a grocery product is assigned a canonical ingredient.

This is intentionally conservative. Missing a questionable match is preferable to recommending a recipe because an unrelated grocery product happened to contain the same word.

## Meal plan ranking

When a meal plan is requested, the backend first builds a lookup containing the cheapest current deal for each canonical ingredient.

Each recipe ingredient is normalized and checked against that lookup.

For every recipe, the matcher keeps track of:

- Matched ingredients
- Missing ingredients
- Number of matches
- Percentage of matchable ingredients on sale

A recipe needs at least one discounted ingredient to be included in the recommendations.

Recipes are currently ranked using the number of matching ingredients, match percentage, and number of missing ingredients.

Water is ignored when calculating recipe matches.

## Matching performance

As the recipe database and grocery vocabulary grew, meal-plan generation became noticeably slower.

With 452 recipes, one meal-plan request was taking about:

```text
7.65 seconds
```

The slowdown came largely from repeatedly rebuilding vocabulary information and scanning aliases during ingredient normalization.

I changed the normalizer so vocabulary indexes are built once when the backend starts. Normalized aliases can then be mapped directly to their canonical ingredients. Frequently repeated normalization results are also cached in memory.

The meal planner separately builds a lookup for the cheapest deal associated with each canonical ingredient instead of scanning every deal for every recipe ingredient.

After those changes, the same meal-plan generation path dropped to approximately:

```text
1.32 seconds
```

The recipe normalization audit still reports 99.88% coverage after the optimization.

## Project structure

```text
SuperMarket_Deals/
|
|-- api.py
|-- database.py
|-- meal_plan.py
|-- recipe_source.py
|-- safeway_deals.py
|-- search_deals.py
|-- store_discovery.py
|
|-- normalization/
|   |-- deal_normalizer.py
|   |-- ingredient_normalizer.py
|   |-- text_normalizer.py
|   |
|   `-- data/
|       |-- grocery_vocabulary.json
|       |-- ingredient_categories.json
|       |-- non_ingredient_products.json
|       |-- normalization_cache.json
|       `-- normalization_review.example.json
|
|-- scripts/
|   |-- audit_ingredient_categories.py
|   |-- audit_recipe_ingredients.py
|   `-- check_deal_normalization.py
|
|-- tests/
|   |-- test_deal_normalizer.py
|   |-- test_ingredient_normalizer.py
|   |-- test_meal_plan.py
|   `-- test_text_normalizer.py
|
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- pages/
|   |   |-- App.jsx
|   |   |-- App.css
|   |   |-- index.css
|   |   `-- main.jsx
|   |
|   |-- package.json
|   `-- vite.config.js
|
|-- data/
|   `-- safeway_sample.json
|
|-- Dockerfile
|-- requirements.txt
|-- requirements-dev.txt
`-- README.md
```

## Backend

The API uses FastAPI.

Start it locally with:

```bash
uvicorn api:app --reload
```

By default it runs at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Current routes include:

```http
GET /
GET /stores
GET /stores/nearby?postal_code={zip_code}
GET /stores/{store_id}/deals
GET /stores/{store_id}/deals/search?item={item}
GET /stores/{store_id}/meal-plan?meals={number}
```

The meal count is currently limited to 1 through 14.

## Frontend

The frontend uses React and Vite.

From the `frontend` directory:

```bash
npm install
npm run dev
```

The development frontend runs separately from FastAPI and currently expects the backend at:

```text
http://127.0.0.1:8000
```

The frontend currently includes:

### Home

- Store search
- Store selection
- Weekly deal preview
- Meal-plan controls

### Weekly Deals

- Deal search
- Category filtering
- Current sale information

### Meal Plan

- Recipe recommendations
- Recipe images
- Deal matches
- Missing ingredients
- Shopping list

The selected store and ZIP code are stored in the browser so the user does not have to select the store again when moving between pages.

Meal-plan results are currently passed through React Router state. Refreshing the meal-plan page directly will clear the generated plan. Persistent meal plans are not implemented yet.

## Database

The project uses PostgreSQL hosted through Supabase.

The main relationships are:

```text
stores
   |
   v
weekly_ads
   |
   v
deal_items


recipes
   |
   v
recipe_ingredients
```

A store can have multiple weekly ads over time, and each weekly ad contains its own deal items.

Recipes and recipe ingredients are stored independently from grocery deals. The canonical ingredient vocabulary is what allows the two datasets to be compared.

Database access is handled through `psycopg` and `psycopg_pool`.

## Environment variables

Local credentials and API configuration are kept in `.env`, which is excluded from Git.

The backend currently expects database configuration along with the credentials needed by the grocery data requests.

```text
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

FLIPP_ACCESS_TOKEN=
```

Actual credentials should not be committed to the repository.

## Tests and audits

The project has pytest coverage for the main normalization and meal-planning behavior.

Run the tests with:

```bash
pytest
```

There are also scripts for checking the data itself.

Recipe ingredient coverage:

```bash
python scripts/audit_recipe_ingredients.py
```

Ingredient category consistency:

```bash
python scripts/audit_ingredient_categories.py
```

Deal normalization against the saved Safeway sample:

```bash
python scripts/check_deal_normalization.py
```

I use these separately from the unit tests because some problems only become obvious when the normalization code is run against the larger recipe or grocery datasets.

## Main tools

- Python
- FastAPI
- PostgreSQL
- Supabase
- Psycopg
- React
- Vite
- JavaScript
- TheMealDB
- Flipp grocery data
- pytest
- Docker

## Where it is now

The main path works from store selection through meal-plan generation.

Safeway is still the only grocery retailer being tested. The recipe matcher is based on a manually maintained vocabulary, and grocery product classification is intentionally conservative.

Before expanding to more retailers or adding more features, I am working through the existing code and data pipeline to make sure the current version stays understandable and testable as the project grows.