import view_deals
import search_deals
import meal_plan
import json

def main():
    print ("Grocery Application for meal planning")

    with open("weekly_deals.json", 'r', encoding='utf-8') as file:
        weekly_deals = json.load(file)

    with open ("recipes.json", 'r', encoding='utf-8') as file:
        recipes = json.load(file)           

    answer = ""

    while answer != "4":
        print ("1. View Weekly Deals")
        print ("2. Search Deals")
        print ("3. Generate Meal Plan")
        print ("4. Exit")
        
        answer = input ("Please select an option (1-4):")

        if answer == "1":
            print (view_deals.view (weekly_deals))

        elif answer == "2":
            search = input("What do you want to search for: ")
            print (search_deals.search(weekly_deals, search))

        elif answer == "3":
            generated = meal_plan.generate(weekly_deals, recipes)
            print (generated)
            
        elif answer == "4":
            print ("Exiting Application...")
        else:
            print ("Invalid option. Please select a valid option (1-4)")

if __name__ == "__main__":
    main()