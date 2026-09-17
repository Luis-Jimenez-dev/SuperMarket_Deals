# SuperMarket Deals

SuperMarket Deals is a grocery meal-planning application that uses weekly supermarket deals to help users find discounted groceries and generate meal recommendations.

I started this project as a way to practice Python while solving a real-world problem: deciding what meals to make based on what is actually on sale that week. The project has grown from a command-line program using local JSON files into an application with a PostgreSQL database, a FastAPI backend, and Docker support.

## Features

The application currently supports:

- Searching for participating grocery stores
- Viewing weekly grocery deals
- Searching deals by item name
- Matching recipe ingredients against weekly deals
- Selecting the cheapest matching deal for an ingredient
- Ranking recipes based on available discounted ingredients
- Calculating estimated costs for matched ingredients
- Identifying ingredients that still need to be purchased
- Combining missing ingredients into a shopping list
- Generating a requested number of meal recommendations
- Accessing grocery and meal-planning features through a FastAPI API
- Running the application through a command-line interface
- Connecting to a hosted PostgreSQL database
- Running the application inside Docker

## How It Works

The application follows this general flow:

```text
Store
  ↓
Weekly Ad
  ↓
Grocery Deals
  ↓
Recipe Matching
  ↓
Meal Recommendations
  ↓
Shopping List
```

Weekly grocery deals are stored in PostgreSQL and associated with a store and weekly advertisement.

When generating a meal plan, the application compares recipe ingredients against the available deals. Ingredient and deal names are split into words so that items with slightly different names can still match.

For example:

```text
Recipe Ingredient:
Chicken Breast

Weekly Deal:
Boneless Chicken Breast
```

The application determines whether enough words match, checks that the units are compatible, and selects the cheapest matching deal.

Recipes are then ranked based on how many ingredients have matching grocery deals and how many ingredients are still missing.

## Project Architecture

The project is separated into modules so that the same business logic can be used by both the command-line application and the API.

```text
                    PostgreSQL
                        │
                   database.py
                        │
              ┌─────────┴─────────┐
              │                   │
           main.py              api.py
             CLI                FastAPI
              │                   │
              └─────────┬─────────┘
                        │
              Application Logic
                        │
          ┌─────────────┼─────────────┐
          │             │             │
   search_deals.py  meal_plan.py  view_deals.py
```

This separation allows the project to grow beyond the original command-line application without rewriting the core grocery and meal-planning logic.

## File Structure

```text
SuperMarket_Deals/
│
├── data/
│   └── Store deal data
│
├── api.py
├── database.py
├── import_deals.py
├── main.py
├── meal_plan.py
├── search_deals.py
├── store_search.py
├── view_deals.py
│
├── recipes.json
├── weekly_deals.json
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

### `main.py`

Runs the command-line version of the application.

It provides the main menu and connects the database, deal search, weekly deal display, and meal-planning features.

### `api.py`

Contains the FastAPI routes.

The API exposes grocery deal and meal-planning functionality so that the application can eventually be used by a web or mobile frontend.

### `database.py`

Handles the PostgreSQL database connection and database queries.

Database credentials are loaded from environment variables rather than being stored directly in the source code.

### `meal_plan.py`

Contains the main meal recommendation logic.

It:

- Compares recipe ingredients against grocery deals
- Finds compatible deal matches
- Chooses the cheapest matching deal
- Determines missing ingredients
- Ranks recipes
- Calculates matched ingredient costs
- Builds the shopping list

### `search_deals.py`

Searches structured grocery deal data by item name.

The function returns structured deal information so that the same search logic can be used by both the CLI and API.

### `view_deals.py`

Formats grocery deal data into readable output for the command-line application.

### `store_search.py`

Searches locally stored grocery deal folders and loads weekly deal information from JSON files.

This is primarily used when working with locally stored deal data.

### `import_deals.py`

Imports locally stored grocery deals into PostgreSQL and associates them with the appropriate weekly advertisement.

Duplicate deal records are ignored during import.

### `recipes.json`

Contains the recipe information used by the meal-planning algorithm, including ingredient names, quantities, and units.

## Database Structure

The PostgreSQL database currently uses three primary tables:

```text
stores
   │
   │ one-to-many
   ↓
weekly_ads
   │
   │ one-to-many
   ↓
deal_items
```

### Stores

Stores basic information about participating supermarkets.

### Weekly Ads

Associates a weekly advertisement with a specific store and date range.

### Deal Items

Stores the individual grocery items belonging to a weekly advertisement, including:

- Item name
- Price
- Unit
- Category

## API

The backend is built using FastAPI.

Start the development server with:

```bash
uvicorn api:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

FastAPI automatically generates interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### Current Endpoints

Check that the API is running:

```http
GET /
```

Get weekly deals for a store:

```http
GET /stores/{store_name}/deals
```

Example:

```http
GET /stores/safeway/deals
```

Search a store's weekly deals:

```http
GET /stores/{store_name}/deals/search?item={item}
```

Example:

```http
GET /stores/safeway/deals/search?item=chicken
```

Generate meal recommendations:

```http
GET /stores/{store_name}/meal-plan?meals={number}
```

Example:

```http
GET /stores/safeway/meal-plan?meals=3
```

## Running the CLI

Create and activate a Python virtual environment, then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

The CLI provides the following menu:

```text
1. View Weekly Deals
2. Search Deals
3. Generate Meal Plan
4. Exit
```

## Environment Variables

Database credentials are stored in a local `.env` file.

The application expects:

```text
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

The `.env` file is excluded from Git and should never be committed to the repository.

## Docker

The application can also run inside a Docker container.

Build the image:

```bash
docker build -t supermarket-deals .
```

Run the command-line application while providing the database environment variables:

```bash
docker run -it --env-file .env supermarket-deals
```

This provides a reproducible Python environment while the application connects to the hosted PostgreSQL database.

## Technologies

- **Python** - Core application logic
- **FastAPI** - REST API
- **PostgreSQL** - Grocery deal database
- **Psycopg** - PostgreSQL database connection
- **Supabase** - Hosted PostgreSQL database
- **Docker** - Containerized application environment
- **JSON** - Recipe and local deal data
- **Git / GitHub** - Version control

## Current Development

The project originally started as a command-line Python application using JSON files.

It is currently being expanded into a full-stack application.

The current development focus is separating the meal-planning calculations from command-line formatting so that the API can return structured JSON data.

## Future Development

Planned improvements include:

- Structured JSON meal-plan responses
- Improved recipe and grocery matching
- Current weekly-ad filtering
- Additional grocery stores
- Automated or semi-automated deal ingestion
- Improved database access patterns
- Web frontend
- User-selected stores and meal preferences
- Better cost comparisons between stores
- Deployment of the API and frontend

## Project Goal

The long-term goal is to make grocery planning easier by connecting supermarket discounts directly to meal decisions.

Instead of asking:

> "What should I cook this week?"

the application is designed to help answer:

> "What can I cook this week based on what is currently on sale?"

The project also serves as an ongoing opportunity to practice backend development, databases, APIs, Docker, application architecture, and eventually full-stack development.