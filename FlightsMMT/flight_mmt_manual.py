from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chr_options = Options()

options = [
    "--disable-gpu",
    "--start-maximized",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features",
    "--disable-blink-features=AutomationControlled",
    "--disable-3d-apis"
]
for option in options:
   chr_options.add_argument(option)


driver = webdriver.Chrome(options=chr_options)
driver.get('https://www.makemytrip.com')
time.sleep(5)

a = driver.find_element(By.ID, 'webklipper-publisher-widget-container-notification-frame')
if a is not None:
  print("Ad frame found")
  driver.switch_to.frame('webklipper-publisher-widget-container-notification-frame')
  driver.find_element(By.ID, 'webklipper-publisher-widget-container-notification-close-div').click()
  driver.switch_to.default_content()


time.sleep(2)
dept_city = "DEL"
arr_city = "PNQ"
dept_date = 'Wed Apr 17 2024'

#For dept city
driver.find_element(By.XPATH, '//*[@id="fromCity"]').click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(dept_city)
time.sleep(2)  # Add some wait time to let the suggestions load
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(Keys.ARROW_DOWN)
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(Keys.ENTER)
time.sleep(2)

#For arrival city
driver.find_element(By.XPATH, '//*[@id="toCity"]').click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(arr_city)
time.sleep(2)  # Add some wait time to let the suggestions load
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(Keys.ARROW_DOWN)
driver.find_element(By.CLASS_NAME, "react-autosuggest__input").send_keys(Keys.ENTER)
time.sleep(2)

#For Date input
driver.find_element(By.XPATH, f"//div[@class='DayPicker-Day'][@aria-label='{dept_date}']").click()

#for Searching
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/p/a').click()

time.sleep(3)
#for closing warning
warni = driver.find_element(By.CLASS_NAME, "bgProperties")
if warni is not None:
   warni.click()
