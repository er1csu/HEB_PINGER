from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptionsimport requests
import beepy
import timeopts = Options()
opts.add_argument("user-agent=whatever you want")SELECTION_DELAY = 0.5
FIREFOX = Truedef find_locations(city_list):
   while (True):
       r = requests.get('https://heb-ecom-covid-vaccine.hebdigital-prd.com/vaccine_locations.json')
       locations = r.json()['locations']
       urls = []
       cities = set()
       for location in locations:
           cities.add(location['city'])        for location in [location for location in locations if location['openTimeslots'] > 0]:
           city = location['city']
           vaccine_type = location['slotDetails'][0]['manufacturer']
           print(f"Open timeslot in {city} - {vaccine_type}")
           if city in city_list:
               if location['openTimeslots'] > 0:
                   url = location['url']
                   urls.append(url)
       print("---------------------------------------------------")
       if len(urls) > 0:
           return urlsdef get_appt(url, driver):    driver.get(url)    # xpath for date selection input control
   # date_selection_xpath = '/html/body/span[2]/div/c-f-s-registration/div/div[1]/div[3]/lightning-card/article/div[2]/slot/div/form/div/lightning-combobox[2]/div[1]/lightning-base-combobox/div/div[1]/input'
   date_selection_xpath = '//*[@id="input-14"]'
   try:
       date_selection_element = WebDriverWait(driver, 5).until(
           EC.presence_of_element_located((By.XPATH, date_selection_xpath))
       )
   except:
       return False    no_appts_path = '//*[@id="container"]/c-f-s-registration/div/div[1]/div[3]/lightning-card/article/div[2]/slot/div/div[2]'
   no_appts_el = driver.find_elements(by=By.XPATH, value=no_appts_path)
   if len(no_appts_el) > 0:
       return False    date_selection_element.click()    date_options_xpath = '//*[@id="input-14-0-14"]'
   date_options_elements = driver.find_elements(by=By.XPATH, value=date_options_xpath)
   if len(date_options_elements) == 0:
       return False    for date_option_element in date_options_elements:
       date_value = date_option_element.get_attribute('data-value')
       date_selection_element.clear()
       if FIREFOX:
           date_selection_element.click()
       time.sleep(SELECTION_DELAY)
       date_selection_element.send_keys(date_value + Keys.RETURN)        appt_time_select_xpath = '//*[@id="input-18"]'
       appt_time_element = driver.find_element(by=By.XPATH, value=appt_time_select_xpath)
       appt_time_element.click()
       appt_options_xpath = '//*[@id="input-18-0-18"]'
       appt_options_elements = driver.find_elements(by=By.XPATH, value=appt_options_xpath)
       for appt_options_element in appt_options_elements:
           appt_time = appt_options_element.get_attribute('data-value')
           appt_time_element.clear()
           if FIREFOX:
               appt_time_element.click()
           time.sleep(SELECTION_DELAY)
           appt_time_element.send_keys(appt_time + Keys.RETURN)            continue_button_path = '//*[@id="container"]/c-f-s-registration/div/div[1]/div[4]/lightning-button/button'
           continue_button = driver.find_element(by=By.XPATH, value=continue_button_path)
           time.sleep(SELECTION_DELAY)
           continue_button.click()            timeslot_full_xpath = '//*[@id="container"]/c-f-s-registration/div/div[1]/div[3]/div/p/lightning-formatted-text'
           try:
               element = WebDriverWait(driver, 3).until(
                   EC.presence_of_element_located((By.XPATH, timeslot_full_xpath))
               )
               print(element.text)
               continue
           except:
               print("timeslot available")
               return Truedef main():
   if FIREFOX:
       opts = FirefoxOptions()
       opts.add_argument("user-agent=whatever you want")
       driver = webdriver.Firefox(options=opts)
   else:
       driver = webdriver.Chrome()    city_list = ['AUSTIN', 'CEDAR PARK', 'LAKEWAY', 'PFLUGERVILLE', 'ROUND ROCK', 'LEANDER', 'WEST LAKE HILLS', 'BEE CAVE']    while True:
       urls = find_locations(city_list)
       for url in urls:
           if get_appt(url, driver):
               driver.maximize_window()
               while True:
                   beepy.beep(4)
                   time.sleep(5)if __name__ == '__main__':
   main()