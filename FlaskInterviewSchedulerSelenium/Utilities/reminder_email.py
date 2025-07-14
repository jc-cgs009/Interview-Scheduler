import smtplib
from email.mime.text import MIMEText

def send_reminder_email(to_email, title, feedback_link):
    body = f"Reminder: Interview for '{title}' starts in few mins.\nFeedback: {feedback_link}"

    msg = MIMEText(body)
    msg['Subject'] = f"Interview Reminder - {title}"
    msg['From'] = "interviewscheduler0@gmail.com"
    msg['To'] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("interviewscheduler0@gmail.com", "zninnklshjnlwoug")
        server.send_message(msg)
