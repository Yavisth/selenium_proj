from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os
import re
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

driver.delete_all_cookies()

dept_city = "DEL"
arr_city = "BOM"
dept_date = 'Wed Apr 23 2024'

def conv_date(dept_date):
  monthday = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  ddmmyyyy = dept_date.split()[2] + "/" + str(monthday.index(dept_date.split()[1]) + 1).zfill(2) + "/" + dept_date.split()[3]
  return ddmmyyyy


itinerary_ud = dept_city + '-' + arr_city + '-' + conv_date(dept_date)
mod_url = "https://www.makemytrip.com/flight/search?itinerary=" + itinerary_ud + "&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"
print(mod_url)
driver.get(mod_url)
time.sleep(3)

#reload if network error
try:
   driver.find_element(By.XPATH, '//*[@id="fullpage-error"]/div/div/div/button').click()
   time.sleep(2)
except:
   pass
   

COUNT = 100

CSV_Loc = "Flight_dat.csv"
fields = ["fname","fcode","dept_city","dept_time","arr_city","arr_time","price","Time of Ret"]

#Close "lock price" popup
try:
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/div[3]/button').click()
    time.sleep(3) 
except:
    pass

#scroll to end
st_tm = time.time()
while True:
    ActionChains(driver).send_keys(Keys.END).perform()
    time.sleep(2)
    # Check for end
    if driver.execute_script("return window.scrollY + window.innerHeight >= document.body.scrollHeight"):
        break
    #timeout for scroll
    elif time.time() - st_tm >= 5:
        break

time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[8]/div[2]').click()
time.sleep(2)

for i in range(1, COUNT+1):
    try:
        #create a list for all the offers
        offer_list = []

        # scrape Flight names
        fname = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[1]/div/p[1]').text
        fcode = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[1]/div/p[2]').text
        # print(f"Flight\nname: {fname} \t code: {fcode}\n")
        # print(f"Date: {conv_date(dept_date)}\n")

        #Dept_city and Arr_city
        dept_city = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[2]/font').text
        arr_city = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[2]/font').text

        #Scrape dept and arr time
        dept_time = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[1]/span').text
        arr_time = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[1]/span').text
        # print(f"Dept_city: {dept_city} \t Arr_city: {arr_city}\n")
        # print(f"Dept_time: {dept_time} \t Arr_time: {arr_time}\n")
        
        #scrape prices
        main_window = driver.current_window_handle

        ##outter list
        out_tx = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/p').text
        print(f'element: {out_tx}')
        outter_offer = re.split("/|\\|", out_tx)
        print(outter_offer)
        for part in outter_offer:
            print(f"part: {part}\n")
            code = part.split()[-1]
            if (code not in offer_list) and (code.isupper):
                offer_list.append(code)
                print( f'Code: {code} added\n')

        time.sleep(2)

        ##Booking page promo list
        driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[2]/div/button').click()
        time.sleep(2)

        ###fare options window open
        if driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button[2]') is not None:
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button[2]').click()
        elif driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button') is not None:
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div/div[1]/div[3]/div/button').click()
        else:
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[3]/button[2]').click()
        time.sleep(3)

        ###switch to booking window
        for window_handle in driver.window_handles:
            if window_handle != main_window:
                driver.switch_to.window(window_handle)
                break

        time.sleep(2)

        ###click to see all promo
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/section/div/div[3]').click()
        time.sleep(2)

        ###Copy and append promo to list
        s = 1
        while True:
            try:
                code_in = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div/section/div/div[3]/div[{s}]/div/div/div/span[1]').text
                if (code not in offer_list) and (code.isupper):
                    offer_list.append(code_in)
                    print(f'code_in: {code_in} added')
                s += 1
            except NoSuchElementException:
                break
        time.sleep(2)

        ###switch to main window
        driver.close()
        driver.switch_to.window(main_window)

        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[1]/div/span').click()

        time.sleep(2)
        print(f'offer list is: {offer_list}')

        #Logging the time of retrival 
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        # print(f'Time of info retrival: {curr_time}\n')

        data=[fname,fcode,dept_city,dept_time,arr_city,arr_time, curr_time]

        if not os.path.exists(CSV_Loc):
            with open(CSV_Loc,'w',newline='',encoding="utf-8") as file:
                writer=csv.writer(file)
                writer.writerow(fields)

        with open(CSV_Loc,'a',newline='',encoding="utf-8") as file:
            writer=csv.writer(file)
            writer.writerow(data)

        if driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]') is None:
            break
    except:
       pass

driver.close()


