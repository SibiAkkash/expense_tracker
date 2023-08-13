from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import time
import os
from dotenv import load_dotenv

load_dotenv()
    
HDFC_NETBANKING_URL = "https://netbanking.hdfcbank.com/netbanking/"


CUSTOMER_ID_XPATH = "/html/body/div[1]/form/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/input"
CONTINUE_XPATH = "/html/body/div[1]/form/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/a"


options = FirefoxOptions()
# profile = FirefoxProfile()
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.dir', './transaction_list/')

driver = webdriver.Firefox(options=options)

driver.get(HDFC_NETBANKING_URL)
time.sleep(3)
print('loaded ?')

driver.switch_to.frame('login_page')

# input customer id
customer_id_element = driver.find_element(By.XPATH, CUSTOMER_ID_XPATH)
customer_id_element.send_keys(os.getenv('CUSTOMER_ID'))

continue_btn = driver.find_element(By.XPATH, CONTINUE_XPATH)
continue_btn.click()

time.sleep(2)

IPIN_XPATH = '//*[@id="fldPasswordDispId"]'
SECURE_ID_CHECKBOX_XPATH = '//*[@id="chkrsastu"]'
LOGIN_XPATH = '/html/body/form/div/div[3]/div/div[1]/div[2]/div[1]/div[4]/div[2]/a'

# input IPIN, click secure ID, login
ipin_element = driver.find_element(By.XPATH, IPIN_XPATH)
ipin_element.send_keys(os.getenv('IPIN'))

secure_id_checkbox = driver.find_element(By.XPATH, SECURE_ID_CHECKBOX_XPATH)
secure_id_checkbox.click()

login_btn = driver.find_element(By.XPATH, LOGIN_XPATH)
login_btn.click()

print('logged in')

time.sleep(3)

driver.switch_to.default_content()

# Enquire -> A/c Statement - Current & Previous Month
print('got to main menu ?')
driver.switch_to.frame('left_menu')


ENQUIRE_XPATH = '//*[@id="enquiryatag"]'
enquire_button = driver.find_element(By.XPATH, ENQUIRE_XPATH)
enquire_button.click()

AC_STATEMENT_XPATH = '/html/body/form/div/div/div/ul/li[4]/div/ul/li[2]/a/span'
account_stmt_button = driver.find_element(By.XPATH, AC_STATEMENT_XPATH)
account_stmt_button.click()


# Choose options to get transaction list
driver.switch_to.default_content()
driver.switch_to.frame('main_part')

time.sleep(1)

# Choose Savings account option, and account number
ACCOUNT_TYPE_SELECT_XPATH = '/html/body/form/table[1]/tbody/tr[1]/td[2]/select'
account_type_select = Select(driver.find_element(By.XPATH, ACCOUNT_TYPE_SELECT_XPATH))
account_type_select.select_by_value("SCA")

ACCOUNT_NO_SELECT_XPATH = '/html/body/form/table[1]/tbody/tr[2]/td[2]/select'
account_no_select = Select(driver.find_element(By.XPATH, ACCOUNT_NO_SELECT_XPATH))
account_no_select.select_by_value("00101460006100  ") # there are 2 spaces in the end for some reason

# Choose custom period button
SELECT_PERIOD_XPATH = '/html/body/form/table[1]/tbody/tr[4]/td[1]/span'
select_period_button = driver.find_element(By.XPATH, SELECT_PERIOD_XPATH)
select_period_button.click()

# choose date in calendar
def choose_date_in_calendar(driver: webdriver.Firefox, date: int) -> None:
    CALENDER_DIV_XPATH = '//*[@id="ui-datepicker-div"]'
    calendar_div = driver.find_element(By.XPATH, CALENDER_DIV_XPATH)

    calender_table_element = calendar_div.find_element(By.CLASS_NAME, 'ui-datepicker-calendar')
    calendar_tbody = calender_table_element.find_element(By.TAG_NAME, 'tbody')
    calendar_dates = calendar_tbody.find_elements(By.TAG_NAME, 'td')

    date_element_to_choose = list(filter(lambda date_element: date_element.text == str(date), calendar_dates))[0]
    date_element_to_choose.click()
    
    time.sleep(1)
    

# open from-date calendar
FROM_DATE_CALENDAR_BUTTON_XPATH = '/html/body/form/table[1]/tbody/tr[4]/td[2]/div[2]/button/span[1]'
from_date_calendar_button = driver.find_element(By.XPATH, FROM_DATE_CALENDAR_BUTTON_XPATH)
from_date_calendar_button.click()
choose_date_in_calendar(driver, date=11)

# open to-date calendar
TO_DATE_CALENDAR_BUTTON_XPATH = '/html/body/form/table[1]/tbody/tr[5]/td[2]/div[2]/button/span[1]'
to_date_calendar_button = driver.find_element(By.XPATH, TO_DATE_CALENDAR_BUTTON_XPATH)
to_date_calendar_button.click()
choose_date_in_calendar(driver, date=12)

# get list of transactions
VIEW_BUTTON_XPATH = '/html/body/form/table[1]/tbody/tr[7]/td/a'
driver.find_element(By.XPATH, VIEW_BUTTON_XPATH).click()

time.sleep(2)

# select download format as excel, and download
download_format_select = Select(driver.find_element(By.NAME, "fldFormatType"))
download_format_select.select_by_value('X')

DOWNLOAD_BUTTON_XPATH = '/html/body/form/table[5]/tbody/tr[2]/td/a'
download_button = driver.find_element(By.XPATH, DOWNLOAD_BUTTON_XPATH).click()

time.sleep(2)

driver.close()    

