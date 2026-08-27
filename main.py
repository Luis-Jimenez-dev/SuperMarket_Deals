def main():
    print ("Grocery Application for meal planning")

    weekly_deals = [{
        "item": "Chicken Breast", "price": 2.49, "unit": "per lb", "category": "protein"
    }, {
        "item": "Broccoli", "price": 1.29, "unit": "per lb", "category": "vegetable" 
        }, {
            "item": "Jasmine Rice", "price": 5.99, "unit": "per bag", "category": "grain"
        }]
    answer = ""

    while answer != "4":
        print ("1. View Weekly Deals")
        print ("2. Search Deals")
        print ("3. Generate Meal Plan")
        print ("4. Exit")
        
        answer = input ("Please select an option (1-4):")

        if answer == "1":
            print ("Viewing Weekly Deals...")
            for deal in weekly_deals:
                print (f"{deal['item']} - ${deal['price']:.2f} {deal['unit']}")
        elif answer == "2":
            found = False
            print ("Searching Deals...")
            search = input("What do you want to search for: ")
            for deal in weekly_deals:
                if search.upper() in deal['item'].upper():
                    print (f"{deal['item']} - ${deal['price']:.2f} {deal['unit']}")
                    found = True

            if not found:
                print (f"No results for {search} found")
        elif answer == "3":
            print ("Generating Meal Plan...")
        elif answer == "4":
            print ("Exiting Application...")
        else:
            print ("Invalid option. Please select a valid option (1-4)")

if __name__ == "__main__":
    main()