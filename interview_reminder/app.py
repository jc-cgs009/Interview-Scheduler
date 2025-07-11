import atexit
import traceback

from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

def check_reminders_job():
    try:
        print("⏰ Checking for upcoming interviews...")
        response = requests.get("http://127.0.0.1:5000/check-reminders")
        print(response.text)
    except Exception as e:
        print("❌ Error while checking reminders:", e)

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reminders_job, trigger="interval", minutes=2)
scheduler.start()

# Shutdown scheduler when app stops
atexit.register(lambda: scheduler.shutdown())

@app.route("/", methods = ['GET', "POST"])
def home():
    return render_template("home.html")

@app.route("/check-reminders", methods = ['GET', 'POST'])
def check_reminders():
    from datetime import datetime, timedelta
    from get_date_time import get_date_time_obj
    from reminder_email import send_reminder_email

    now = datetime.now()
    try:
        interview_time = get_date_time_obj()
        delta = interview_time - now
        print(delta)

        if timedelta(minutes=0) <= delta <= timedelta(minutes=10):
                send_reminder_email("jc.cgs.999@gmail.com", "Python Developer")
                print("sent email")

    except Exception as e:
        traceback.print_exc()
        print("Error while checking reminders:", e)

    return f"Sent reminders at {now.strftime('%Y-%m-%d %H:%M:%S')}"



if __name__ == "__main__":
    app.run(debug=False)