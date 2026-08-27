def search(deals, search_term):
    found = False
    to_print = ""

    for deal in deals:
        if search_term.upper() in deal['item'].upper():
            to_print += (f"{deal['item']} - ${deal['price']:.2f} {deal['unit']} \n")
            found = True

    if not found:
        to_print += (f"No results for {search_term} found")

    return to_print