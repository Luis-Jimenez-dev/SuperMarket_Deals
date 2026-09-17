# Formats weekly deal data for the command-line interface

def view(deals):
    to_print = ""

    # Format each deal into a readable line
    for deal in deals:
        to_print += (
            f"{deal['item']} - ${deal['price']:.2f} {deal['unit']} \n"
        )

    return to_print