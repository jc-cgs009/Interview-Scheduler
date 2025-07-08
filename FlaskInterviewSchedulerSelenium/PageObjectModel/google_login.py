import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class GoogleLogin:
    email_input_field_xpath = "//input[@id='identifierId']"
    password_input_field_xpath = "//input[@type='password']"

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def hit_url(self):
        self.driver.get(self.url)
        time.sleep(3)

    def enter_email(self, mail_id):
        email_input = self.driver.find_element(By.XPATH, GoogleLogin.email_input_field_xpath)
        email_input.send_keys(mail_id)
        email_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def enter_password(self, password):
        password_input = self.driver.find_element(By.XPATH, GoogleLogin.password_input_field_xpath)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)

