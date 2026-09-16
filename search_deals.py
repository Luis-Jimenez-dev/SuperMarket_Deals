def search(deals, search_term):
    results = []

    for deal in deals:
        if search_term.upper() in deal['item'].upper():
            results.append(deal)

    return results