# Command-line interface for the grocery meal planning application

import view_deals
import search_deals
import meal_plan
import database


# Run the command-line version of the application
def main():
    print("Grocery Application for meal planning")

    # Load recipes once when the application starts
    recipes = meal_plan.load_recipes()

    # Ask for a store until one with available deals is found
    while True:
        search = input("Search for a store: ")
        weekly_deals = database.get_deals(search)

        if weekly_deals:
            break

        print("Store not Found. Try again")

    answer = ""

    # Keep displaying the menu until the user chooses to exit
    while answer != "4":
        print("1. View Weekly Deals")
        print("2. Search Deals")
        print("3. Generate Meal Plan")
        print("4. Exit")

        answer = input("Please select an option (1-4):")

        # Display all weekly deals for the selected store
        if answer == "1":
            print(view_deals.view(weekly_deals))

        # Search the store's weekly deals for a specific item
        elif answer == "2":
            search = input("What do you want to search for: ")
            results = search_deals.search(weekly_deals, search)

            # Format the structured search results for the CLI
            for result in results:
                print(
                    f"{result['item']} - "
                    f"${result['price']:.2f} {result['unit']}"
                )

        # Generate meal recommendations using the store's weekly deals
        elif answer == "3":
            while True:
                try:
                    meal_count = int(
                        input("How many meals would you like to generate: ")
                    )

                    # Meal count must be at least one
                    if meal_count <= 0:
                        print("Enter a value greater than 0")
                        continue

                    meal_data = meal_plan.generate(
                        weekly_deals,
                        recipes,
                        meal_count
                    )

                    formatted_data = meal_plan.format_meal_plan(meal_data)

                    print(formatted_data)
                    break

                # Handle input that cannot be converted to an integer
                except ValueError:
                    print("Please enter a number")

        elif answer == "4":
            print("Exiting Application...")

        else:
            print("Invalid option. Please select a valid option (1-4)")


# Only start the CLI when this file is run directly
if __name__ == "__main__":
    main()