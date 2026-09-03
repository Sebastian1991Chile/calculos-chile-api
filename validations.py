from datetime import datetime

def validate_date(initial_date, final_date):
    try:
        initial = datetime.strptime(initial_date, "%Y-%m-%d")
        final = datetime.strptime(final_date, "%Y-%m-%d")
        return initial <= final
    except ValueError:
        return False