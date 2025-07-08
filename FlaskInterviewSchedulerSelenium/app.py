import time
import traceback

from Utilities.get_custom_date import get_modified_date_format
from Utilities.get_custom_time import get_modified_time_format
from Utilities.html_date_time_format import get_html_date_time_format

from InterviewSchedulerScript.interview_scheduler import InterviewSchedulerTool

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column



app = Flask(__name__)
app.secret_key = "InterviewSchedulerAlertSecretKey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interview.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class InterviewScheduler(db.Model):
    sno: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(nullable=False)
    guests: Mapped[str] = mapped_column(nullable=False)
    interview_date: Mapped[str] = mapped_column(nullable=False)
    interview_start_time: Mapped[str] = mapped_column(nullable=False)
    interview_end_time: Mapped[str] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        try:
            title = request.form['title']
            candidate_email = request.form['email']

            guest_raw = request.form['guests']
            guests = [g.strip() for g in guest_raw.replace('\n', ',').split(',') if g != ""]
            guests.append(candidate_email)
            guests_ = ','.join(guests)

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
            data = InterviewScheduler(
                title=title,
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
    all_interviews = InterviewScheduler.query.all()
    return render_template("interviews.html", all_interviews = all_interviews)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        try:
            title = request.form['title']
            candidate_email = request.form['email']

            guest_raw = request.form['guests']
            guests = [g.strip() for g in guest_raw.replace('\n', ',').split(',') if g != ""]
            guests.append(candidate_email)
            guests_ = ','.join(guests)

            start_date = get_modified_date_format(request.form['date'])
            start_time = get_modified_time_format(request.form['start_time'])
            end_time = get_modified_time_format(request.form['end_time'])

            interview = InterviewScheduler.query.filter_by(sno=sno).first()

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
            interview.guests = guests_
            interview.interview_date = start_date
            interview.interview_start_time = start_time
            interview.interview_end_time = end_time

            db.session.commit()

            flash("Interview updated successfully!", "success")

        return redirect(url_for('interviews'))

    interview = InterviewScheduler.query.filter_by(sno = sno).first()
    start_date, start_time, end_time = get_html_date_time_format(interview.interview_date,
                                                                interview.interview_start_time,
                                                                interview.interview_end_time)

    return render_template('update.html',
                           interview = interview,
                           start_date = start_date,
                           start_time = start_time,
                           end_time = end_time
                           )

@app.route("/cancel/<int:sno>", methods = ['GET','POST'])
def cancel(sno):
    if request.method == 'POST':
        try:
            interview = InterviewScheduler.query.filter_by(sno = sno).first()
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

    interview = InterviewScheduler.query.filter_by(sno = sno).first()
    return render_template("cancel.html", interview = interview)



if __name__ == "__main__":
    app.run(debug=False)