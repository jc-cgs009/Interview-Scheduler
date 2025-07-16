import atexit
import traceback
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from Utilities.get_custom_date import get_modified_date_format
from Utilities.get_custom_time import get_modified_time_format
from Utilities.html_date_time_format import get_html_date_time_format

from InterviewSchedulerScript.interview_scheduler import InterviewSchedulerTool

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column

from datetime import datetime, timedelta
from Utilities.get_date_time import get_date_time_obj
from Utilities.reminder_email import send_reminder_email



app = Flask(__name__)
app.secret_key = "InterviewSchedulerAlertSecretKey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interview.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class InterviewScheduler(db.Model):
    __tablename__ = 'interviews'

    cid: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(nullable=False)
    candidate_email:Mapped[str] = mapped_column(nullable=False)
    interviewer_email:Mapped[str] = mapped_column(nullable=False)
    guests: Mapped[str] = mapped_column(nullable=False)
    interview_date: Mapped[str] = mapped_column(nullable=False)
    interview_start_time: Mapped[str] = mapped_column(nullable=False)
    interview_end_time: Mapped[str] = mapped_column(nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    cid: Mapped[int] = mapped_column(primary_key=True)
    candidate_email: Mapped[str] = mapped_column(nullable=False)
    feedback: Mapped[str] = mapped_column(default="")

with app.app_context():
    db.create_all()


def check_reminders_job():
    try:
        print("Checking for upcoming interviews...")
        response = requests.get("http://127.0.0.1:5000/check-reminders")
        print(response.text)
    except Exception as e:
        print("Error while checking reminders:", e)

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reminders_job, trigger="interval", minutes=2)
scheduler.start()

# Shutdown scheduler when app stops
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        try:
            title = request.form['title']
            candidate_email = request.form['email']
            interviewer_email = request.form['interviewer']

            guest_raw = request.form['guests']
            guests = [g.strip() for g in guest_raw.replace('\n', ',').split(',') if g != ""]
            guests_ = ','.join(guests)

            guests.extend([interviewer_email, candidate_email])

            start_date = get_modified_date_format(request.form['date'])
            start_time = get_modified_time_format(request.form['start_time'])
            end_time = get_modified_time_format(request.form['end_time'])

            data = {
                "title": title,
                "start_date": start_date,
                "start_time": start_time,
                "end_time": end_time,
                "guests": guests
            }

            is_obj = InterviewSchedulerTool()
            is_obj.schedule_interview(data)

        except Exception as e:
            traceback.print_exc()
            flash(f"Failed to schedule interview: {str(e)}", "danger")

        else:
            last_record = InterviewScheduler.query.order_by(InterviewScheduler.cid.desc()).first()
            if last_record is None:
                cid = 1
            else:
                cid = last_record.cid + 1

            data = InterviewScheduler(
                cid = cid,
                title=title,
                candidate_email = candidate_email,
                interviewer_email = interviewer_email,
                guests=guests_,
                interview_date=start_date,
                interview_start_time=start_time,
                interview_end_time=end_time
            )

            db.session.add(data)
            db.session.commit()

            flash("Interview scheduled successfully!", "success")

        return redirect(url_for('schedule'))

    return render_template('schedule.html')


@app.route("/interviews", methods = ['GET', 'POST'])
def interviews():
    from Utilities.disable_action import should_disable_actions

    all_interviews = InterviewScheduler.query.all()

    for interview in all_interviews:
        interview.disable_actions = should_disable_actions(interview.interview_date, interview.interview_start_time)

    return render_template("interviews.html", all_interviews = all_interviews)


@app.route('/update/<int:cid>', methods=['GET', 'POST'])
def update(cid):
    if request.method == 'POST':
        try:
            title = request.form['title']
            candidate_email = request.form['email']
            interviewer_email = request.form['interviewer']

            guest_raw = request.form['guests']
            guests = [g.strip() for g in guest_raw.replace('\n', ',').split(',') if g != ""]
            guests_ = ','.join(guests)

            guests.extend([candidate_email, interviewer_email])

            start_date = get_modified_date_format(request.form['date'])
            start_time = get_modified_time_format(request.form['start_time'])
            end_time = get_modified_time_format(request.form['end_time'])

            interview = InterviewScheduler.query.filter_by(cid=cid).first()

            data = {
                "old_title": interview.title,
                "new_title": title,
                "interview_scheduled_date": interview.interview_date,
                "start_date":start_date,
                "start_time":start_time,
                "end_time":end_time,
                "guests":guests
            }

            is_obj = InterviewSchedulerTool()
            is_obj.update_scheduled_interview(data)

        except Exception as e:
            traceback.print_exc()
            flash(f"Failed to update interview: {str(e)}", "danger")

        else:
            interview.title = title
            interview.candidate_email = candidate_email
            interview.interviewer_email = interviewer_email
            interview.guests = guests_
            interview.interview_date = start_date
            interview.interview_start_time = start_time
            interview.interview_end_time = end_time

            db.session.commit()

            flash("Interview updated successfully!", "success")

        return redirect(url_for('interviews'))

    interview = InterviewScheduler.query.filter_by(cid = cid).first()
    start_date, start_time, end_time = get_html_date_time_format(interview.interview_date,
                                                                interview.interview_start_time,
                                                                interview.interview_end_time)

    return render_template('update.html',
                           interview = interview,
                           start_date = start_date,
                           start_time = start_time,
                           end_time = end_time
                           )

@app.route("/cancel/<int:cid>", methods = ['GET','POST'])
def cancel(cid):
    if request.method == 'POST':
        try:
            interview = InterviewScheduler.query.filter_by(cid = cid).first()
            data = {
                "title": interview.title,
                "interview_scheduled_date":interview.interview_date
            }

            is_obj = InterviewSchedulerTool()
            is_obj.cancel_scheduled_interview(data)

        except Exception as e:
            traceback.print_exc()
            flash(f"Failed to cancel interview: {str(e)}", "danger")
        else:
            db.session.delete(interview)
            db.session.commit()

            flash("Interview canceled successfully!", "success")

        return redirect(url_for("interviews"))

    interview = InterviewScheduler.query.filter_by(cid = cid).first()
    return render_template("cancel.html", interview = interview)

@app.route("/delete/<int:cid>", methods = ["GET", "POST"])
def delete(cid):
    if request.method == 'POST':
        interview = InterviewScheduler.query.filter_by(cid = cid).first()
        c_info = Feedback.query.filter_by(cid = cid).first()

        db.session.delete(interview)
        db.session.delete(c_info)
        db.session.commit()

        return redirect(url_for("interviews"))

    interview = InterviewScheduler.query.filter_by(cid=cid).first()
    return render_template("delete.html", interview = interview)

@app.route("/check-reminders", methods = ['GET', 'POST'])
def check_reminders():
    now = datetime.now()

    interviews_ = InterviewScheduler.query.all()
    for interview in interviews_:
        try:
            interview_time = get_date_time_obj(interview.interview_date, interview.interview_start_time)
            delta = interview_time - now

            cid = interview.cid
            feedback_mail_sent = Feedback.query.filter_by(cid = cid).first()
            print(feedback_mail_sent)

            if timedelta(minutes=0) <= delta <= timedelta(minutes=10) and not feedback_mail_sent:
                feedback_link = f"http://127.0.0.1:5000/feedback_form/{cid}"
                send_reminder_email(interview.interviewer_email, interview.title, feedback_link)
                print("sent email")

                data = Feedback(
                    cid = cid,
                    candidate_email = interview.candidate_email,
                )
                db.session.add(data)
                db.session.commit()

        except Exception as e:
            traceback.print_exc()
            print("Error while checking reminders:", e)

    return "checked for reminders"

@app.route("/feedback_form/<int:cid>", methods = ['GET', 'POST'])
def feedback_form(cid):
    if request.method == 'POST':
        feedback_ = request.form['feedback']
        c_info = Feedback.query.filter_by(cid = cid).first()
        c_info.feedback = feedback_

        db.session.commit()

        return redirect(url_for("edit_feedback", cid = cid))

    candidate_info = Feedback.query.filter_by(cid = cid).first()
    return render_template("feedback_form.html", candidate_info = candidate_info)

@app.route("/edit_feedback/<int:cid>", methods = ['GET', 'POST'])
def edit_feedback(cid):
    return render_template("edit_feedback.html", cid = cid)

@app.route("/feedback/<int:cid>", methods = ["GET"])
def feedback(cid):
    candidate_info = Feedback.query.filter_by(cid = cid).first()
    return render_template("feedback.html", candidate_info = candidate_info)

if __name__ == "__main__":
    app.run(debug=False)