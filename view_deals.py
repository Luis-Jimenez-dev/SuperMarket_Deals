def view(deals):
    to_print = ""
    for deal in deals:
        to_print += ((f"{deal['item']} - ${deal ['price']:.2f} {deal['unit']} \n"))

    return to_print