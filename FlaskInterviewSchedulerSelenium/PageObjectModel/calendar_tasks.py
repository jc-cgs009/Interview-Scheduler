import time

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CalendarTask:
    create_button_xpath = "//button/span[text()='Create']"
    event_dropdown_xpath = "//div/ul/li/span/span[text()='Event']//ancestor::li"
    add_title_xpath = "//input[@placeholder='Add title']"
    start_date_xpath = "//span[@data-Key='startDate']"
    enter_start_date_xpath = "//input[@aria-label='Start date']"
    enter_start_time_xpath = "//input[@aria-label='Start time']"
    enter_end_time_xpath = "//input[@aria-label='End time']"
    add_guest_click_xpath = "//div[text()='Add guests']//parent::button"
    add_guest_xpath = "//input[@placeholder='Add guests']"
    save_button_xpath = "//span[text()='Save']//parent::button"
    send_button_xpath = "//span[text()='Send']//parent::button"
    # update
    year_month_xpath = "//h1[text()='Drawer']//following-sibling::div[1]/div/div/span"
    next_month_button_xpath = "//button[@aria-label='Next month']"
    day_button_xpath = "//div[text()='{}']//parent::button"
    event_xpath = "//span[contains(text(), '{}')]//parent::span//parent::div"
    edit_button_xpath = "//div[text()='Edit event']//preceding-sibling::button"
    existing_guest_mail_id_xpath = "//div[@aria-label='Guests invited to this event.']/div/div[2]"
    remove_guest_button_xpath = "(//button[@data-email='{}'])[3]"
    # cancel
    delete_event_button_xpath = "//div[text()='Delete event']//preceding-sibling::button"

    def __init__(self, driver, cal_url):
        self.driver = driver
        self.cal_url = cal_url

    def hit_calendar_url(self):
        self.driver.get(self.cal_url)

    def click_on_create_button(self):
        self.driver.find_element(By.XPATH, CalendarTask.create_button_xpath).click()

    def click_on_event_option(self):
        self.driver.find_element(By.XPATH, CalendarTask.event_dropdown_xpath).click()

    def add_title(self, title):
        adt = self.driver.find_element(By.XPATH, CalendarTask.add_title_xpath)
        time.sleep(1)
        adt.send_keys(Keys.CONTROL + "a")
        adt.send_keys(Keys.DELETE)
        adt.send_keys(title)

    def click_on_start_date(self):
        self.driver.find_element(By.XPATH, CalendarTask.start_date_xpath).click()

    def enter_interview_start_date(self, date_):
        sd = self.driver.find_element(By.XPATH, CalendarTask.enter_start_date_xpath)
        sd.send_keys(Keys.CONTROL + "a")
        sd.send_keys(Keys.DELETE)
        sd.send_keys(date_)

    def enter_interview_start_time(self, time_):
        st = self.driver.find_element(By.XPATH, CalendarTask.enter_start_time_xpath)
        st.send_keys(Keys.CONTROL + "a")
        st.send_keys(Keys.DELETE)
        st.send_keys(time_)

    def enter_interview_end_time(self, time_):
        et = self.driver.find_element(By.XPATH, CalendarTask.enter_end_time_xpath)
        et.send_keys(Keys.CONTROL + "a")
        et.send_keys(Keys.DELETE)
        et.send_keys(time_)

    def click_on_add_guest(self):
        self.driver.find_element(By.XPATH, CalendarTask.add_guest_click_xpath).click()

    def add_guests(self, guests):
        ag = self.driver.find_element(By.XPATH, CalendarTask.add_guest_xpath)
        for guest in guests:
            ag.send_keys(guest)
            ag.send_keys(Keys.ENTER)

    def click_on_save_button(self):
        self.driver.find_element(By.XPATH, CalendarTask.save_button_xpath).click()

    def click_on_send_button(self):
        self.driver.find_element(By.XPATH, CalendarTask.send_button_xpath).click()

    def click_on_event_date(self, date):
        m, d, y = date.split()
        while True:
            year_month_text = self.driver.find_element(By.XPATH, CalendarTask.year_month_xpath).text
            if m in year_month_text and y in year_month_text:
                    break

            self.driver.find_element(By.XPATH, CalendarTask.next_month_button_xpath).click()

        self.driver.find_element(By.XPATH, CalendarTask.day_button_xpath.format(d)).click()

    def click_on_event(self, title):
        self.driver.find_element(By.XPATH, CalendarTask.event_xpath.format(title)).click()

    def click_on_edit(self):
        self.driver.find_element(By.XPATH, CalendarTask.edit_button_xpath).click()

    def manage_guest(self, guest_mails):
        eg = self.driver.find_elements(By.XPATH, CalendarTask.existing_guest_mail_id_xpath)

        actions = ActionChains(self.driver)
        for ele in eg[1:]:
            mail = ele.get_attribute('data-hovercard-id')
            if mail not in guest_mails:
                actions.move_to_element(ele).perform()

                remove_btn = self.driver.find_element(By.XPATH, CalendarTask.remove_guest_button_xpath.format(mail))
                actions.move_to_element(remove_btn).click().perform()

            else:
                guest_mails.remove(mail)

        self.add_guests(guest_mails)

    def click_on_delete_event_button(self):
        self.driver.find_element(By.XPATH, CalendarTask.delete_event_button_xpath).click()



















