from datetime import datetime
def get_html_date_time_format(date, start_time, end_time):
    if start_time.startswith('0:'):
        start_time = '12:' + start_time[2:]

    if end_time.startswith('0:'):
        end_time = '12:' + end_time[2:]

    # Parse to datetime objects
    date_obj = datetime.strptime(date, "%B %d %Y")  # → 2025-07-09
    start_time_obj = datetime.strptime(start_time, "%I:%M%p")  # → 09:20
    end_time_obj = datetime.strptime(end_time, "%I:%M%p")  # → 10:20


    # Format for HTML input fields
    date_for_html = date_obj.strftime("%Y-%m-%d")
    start_for_html = start_time_obj.strftime("%H:%M")
    end_for_html = end_time_obj.strftime("%H:%M")

    return date_for_html, start_for_html, end_for_html