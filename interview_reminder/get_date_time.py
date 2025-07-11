from datetime import datetime

def get_date_time_obj():
    # example: combining date and time strings
    date_str = "July 11 2025"
    time_str = "10:48pm"

    datetime_str = f"{date_str} {time_str}"
    dt_obj = datetime.strptime(datetime_str, "%B %d %Y %I:%M%p")
    return dt_obj
