# Search grocery deals by item name
def search(deals, search_term):
    results = []

    # Check each deal for a case-insensitive match
    for deal in deals:
        if search_term.upper() in deal['item'].upper():
            results.append(deal)

    # Return structured deal data so it can be used by the CLI or API
    return results