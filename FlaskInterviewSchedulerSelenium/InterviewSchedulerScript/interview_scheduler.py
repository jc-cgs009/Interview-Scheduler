from Utilities.get_driver import get_web_driver
from PageObjectModel.google_login import GoogleLogin
from PageObjectModel.calendar_tasks import CalendarTask


class InterviewSchedulerTool:
    def __init__(self):
        self.driver = get_web_driver()
        self.url = 'https://accounts.google.com/'
        self.cal_url = 'https://calendar.google.com'
        self.email_id = "interviewscheduler13@gmail.com"
        self.password = "is@43210"


    def login_to_google(self):
        gl = GoogleLogin(self.driver, self.url)
        gl.hit_url()
        gl.enter_email(self.email_id)
        gl.enter_password(self.password)


    def schedule_interview(self, data):
        self.login_to_google()
        sct = CalendarTask(self.driver, self.cal_url)
        sct.hit_calendar_url()
        sct.click_on_create_button()
        sct.click_on_event_option()
        sct.add_title(data['title'])
        sct.click_on_start_date()
        sct.enter_interview_start_date(data['start_date'])
        sct.enter_interview_start_time(data['start_time'])
        sct.enter_interview_end_time(data['end_time'])
        sct.click_on_add_guest()
        sct.add_guests(data['guests'])
        sct.click_on_save_button()
        sct.click_on_send_button()

    def update_scheduled_interview(self, data):
        self.login_to_google()
        uct = CalendarTask(self.driver, self.cal_url)
        uct.hit_calendar_url()
        uct.click_on_event_date(data['interview_scheduled_date'])
        uct.click_on_event(data['old_title'])
        uct.click_on_edit()
        uct.add_title(data['new_title'])
        uct.enter_interview_start_date(data['start_date'])
        uct.enter_interview_start_time(data['start_time'])
        uct.enter_interview_end_time(data['end_time'])
        uct.manage_guest(data['guests'])
        uct.click_on_save_button()
        uct.click_on_send_button()

    def cancel_scheduled_interview(self, data):
        self.login_to_google()
        cct = CalendarTask(self.driver, self.cal_url)
        cct.hit_calendar_url()
        cct.click_on_event_date(data['interview_scheduled_date'])
        cct.click_on_event(data['title'])
        cct.click_on_delete_event_button()
        cct.click_on_send_button()


if __name__ == "__main__":
    insh = InterviewSchedulerTool()
    # insh.schedule_interview()
    # insh.update_scheduled_interview()
    # insh.cancel_scheduled_interview()
    # insh.login_to_google()
    # time.sleep(2)



