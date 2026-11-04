# Command-line interface for the grocery meal planning application

import view_deals
import search_deals
import meal_plan
import database
import store_discovery
import safeway_deals


def main():
    print("Grocery Application for meal planning")

    # Load recipes once when the application starts
    recipes = meal_plan.load_recipes()

    # Find nearby stores using the user's ZIP code
    while True:
        postal_code = input("Enter your ZIP code: ").strip()

        # Basic CLI validation
        if len(postal_code) != 5 or not postal_code.isdigit():
            print("Please enter a valid 5-digit ZIP code.")
            continue

        try:
            stores = store_discovery.find_stores(postal_code)
            stores = database.save_stores(stores)
        except Exception as error:
            print(f"Could not find stores: {error}")
            continue

        if not stores:
            print("No stores found near that ZIP code. Try again.")
            continue

        break

    # Display nearby stores
    print("\nNearby Stores:")

    for index, store in enumerate(stores, start=1):
        print(
            f"{index}. {store['name']} - "
            f"{store['distance']} miles"
        )

    # Let the user choose one of the nearby stores
    while True:
        try:
            store_choice = int(
                input("\nSelect a store by number: ")
            )

            if store_choice < 1 or store_choice > len(stores):
                print("Please select a valid store number.")
                continue

            selected_store = stores[store_choice - 1]
            break

        except ValueError:
            print("Please enter a number.")

    store_id = selected_store['store_id']

    print(f"\nShopping at: {selected_store['name']}")

    # Make sure the selected store has its current weekly deals
    try:
        safeway_deals.ensure_current_deals(store_id)
        weekly_deals = database.get_deals(store_id)
    except Exception as error:
        print(f"Could not load weekly deals: {error}")
        return

    if not weekly_deals:
        print("No weekly deals are currently available for this store.")
        return

    print(f"{len(weekly_deals)} weekly deals found.")

    # Main CLI menu
    answer = ""

    while answer != "4":
        print("\n1. View Weekly Deals")
        print("2. Search Deals")
        print("3. Generate Meal Plan")
        print("4. Exit")

        answer = input("Please select an option (1-4): ").strip()

        # Display all weekly deals
        if answer == "1":
            print()
            print(view_deals.view(weekly_deals))

        # Search the selected store's weekly deals
        elif answer == "2":
            search = input(
                "What do you want to search for: "
            ).strip()

            results = search_deals.search(
                weekly_deals,
                search
            )

            if not results:
                print("No matching deals found.")
                continue

            print()

            for result in results:
                print(
                    f"{result['item']} - "
                    f"${result['price']:.2f} "
                    f"{result['unit'] or ''}"
                )

        # Generate a meal plan
        elif answer == "3":
            while True:
                try:
                    meal_count = int(
                        input(
                            "How many meals would you like "
                            "to generate (1-14): "
                        )
                    )

                    if meal_count < 1 or meal_count > 14:
                        print(
                            "Please enter a number between 1 and 14."
                        )
                        continue

                    meal_data = meal_plan.generate(
                        weekly_deals,
                        recipes,
                        meal_count
                    )

                    formatted_data = (
                        meal_plan.format_meal_plan(meal_data)
                    )

                    print()
                    print(formatted_data)
                    break

                except ValueError:
                    print("Please enter a number.")

        elif answer == "4":
            print("Exiting Application...")

        else:
            print(
                "Invalid option. "
                "Please select a valid option (1-4)."
            )


# Only start the CLI when this file is run directly
if __name__ == "__main__":
    try:
        main()
    finally:
        database.pool.close()