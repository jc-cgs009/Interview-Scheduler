from datetime import datetime

def get_date_time_obj(date_str,time_str):
    datetime_str = f"{date_str} {time_str}"
    dt_obj = datetime.strptime(datetime_str, "%B %d %Y %I:%M%p")
    return dt_obj
