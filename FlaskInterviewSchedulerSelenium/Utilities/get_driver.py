from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_web_driver():
    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument('--headless')  # Run headless
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service = service, options = options)
    driver.maximize_window()
    driver.implicitly_wait(15)
    return driver