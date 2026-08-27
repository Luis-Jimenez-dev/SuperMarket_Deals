import view_deals
import search_deals
import json

def main():
    print ("Grocery Application for meal planning")

    with open("weekly_deals.json", 'r', encoding='utf-8') as file:
        weekly_deals = json.load(file)

    answer = ""

    while answer != "4":
        print ("1. View Weekly Deals")
        print ("2. Search Deals")
        print ("3. Generate Meal Plan")
        print ("4. Exit")
        
        answer = input ("Please select an option (1-4):")

        if answer == "1":
            print ("Viewing Weekly Deals...")
            print (view_deals.view (weekly_deals))
        elif answer == "2":
            print ("Searching Deals...")
            search = input("What do you want to search for: ")
            print (search_deals.search(weekly_deals, search))

        elif answer == "3":
            print ("Generating Meal Plan...")
        elif answer == "4":
            print ("Exiting Application...")
        else:
            print ("Invalid option. Please select a valid option (1-4)")

if __name__ == "__main__":
    main()