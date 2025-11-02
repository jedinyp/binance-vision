from datetime import datetime, timedelta

def generate_date_list(date_range: tuple[str, str]) -> list[str]:
    """
    Generates a list of date strings between two dates.
    Args:
        date_range (tuple[str, str]): Tuple of start and end date strings.
    Returns:
        list[str]: List of date strings.
    """
    
    start_str, end_str = date_range
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")

    # Generate list of date strings
    date_list = [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end_date - start_date).days + 1)
    ]

    return date_list