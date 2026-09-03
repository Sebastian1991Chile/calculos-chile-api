def format_variation(variation):
    variation_with_coma = f"{variation:,.1f}".replace(".", ",")
    return f"{variation_with_coma}%"

def amount_with_currency(amount, currency="$"):
    amount_with_separator = f"{amount:,.0f}".replace(",", ".")
    return f"{currency}{amount_with_separator}"