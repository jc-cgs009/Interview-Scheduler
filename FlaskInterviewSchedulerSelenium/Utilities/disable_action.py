from datetime import datetime, timedelta
from Utilities.get_date_time import get_date_time_obj

def should_disable_actions(date_str, time_str):
    try:
        interview_time = get_date_time_obj(date_str, time_str)
        return datetime.now() >= interview_time - timedelta(minutes=10)
    except Exception as e:
        print("Parse error:", e)
        return False


