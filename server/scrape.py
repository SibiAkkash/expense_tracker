from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import os
import time
import datetime
from pathlib import Path

from dotenv import load_dotenv
from parse_transactions import parse_transactions

load_dotenv()


HDFC_NETBANKING_URL = "https://netbanking.hdfcbank.com/netbanking/"

# Element locations
# ? is this a good place to list out all XPATHs, or should it be right next to the elements ?
CUSTOMER_ID_XPATH = (
    "/html/body/div[1]/form/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/input"
)
CONTINUE_XPATH = "/html/body/div[1]/form/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/a"
IPIN_XPATH = '//*[@id="fldPasswordDispId"]'
SECURE_ID_CHECKBOX_XPATH = '//*[@id="chkrsastu"]'
LOGIN_XPATH = "/html/body/form/div/div[3]/div/div[1]/div[2]/div[1]/div[4]/div[2]/a"


def init_driver_with_options() -> webdriver.Firefox:
    """Return firefox webdriver with options (headless mode, custom download location)"""
    # set custom download directory
    download_dir: Path = Path.cwd() / "transaction_lists"
    download_dir.mkdir(exist_ok=True)

    options = FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", str(download_dir))
    options.add_argument("--headless")

    print(
        f"initialised driver headless mode, files download location: {str(download_dir)}"
    )
    # initialise driver with options
    # searches for firefox driver in current directory
    # is there a way to specify path to the driver ?
    return webdriver.Firefox(options=options)


def login_to_site(driver: webdriver.Firefox) -> None:
    """Switches to login_page iframe, input customer ID, netbanking IPIN, switch back to default frame"""
    driver.get(HDFC_NETBANKING_URL)
    time.sleep(3)
    print("loaded ?")

    driver.switch_to.frame("login_page")
    # input customer id
    driver.find_element(By.XPATH, CUSTOMER_ID_XPATH).send_keys(os.getenv("CUSTOMER_ID"))
    # click continue button
    driver.find_element(By.XPATH, CONTINUE_XPATH).click()
    # sleep to allow time to load
    time.sleep(2)

    # input IPIN, click secure ID, login
    driver.find_element(By.XPATH, IPIN_XPATH).send_keys(os.getenv("IPIN"))
    # click secure id checkbox
    driver.find_element(By.XPATH, SECURE_ID_CHECKBOX_XPATH).click()
    # click login button
    driver.find_element(By.XPATH, LOGIN_XPATH).click()
    print("logged in")
    time.sleep(3)

    driver.switch_to.default_content()


def navigate_to_account_statement(driver: webdriver.Firefox) -> None:
    """Navigate to the account statement section"""
    # Enquire -> A/c Statement - Current & Previous Month
    print("got to main menu ?")
    driver.switch_to.frame("left_menu")
    # open enquire tab
    ENQUIRE_XPATH = '//*[@id="enquiryatag"]'
    driver.find_element(By.XPATH, ENQUIRE_XPATH).click()
    # choose A/c statement option
    AC_STATEMENT_XPATH = "/html/body/form/div/div/div/ul/li[4]/div/ul/li[2]/a/span"
    driver.find_element(By.XPATH, AC_STATEMENT_XPATH).click()

    print("navigated to account statement section")
    driver.switch_to.default_content()


def choose_date_in_calendar(driver: webdriver.Firefox, date: datetime.date) -> None:
    print(f"choosing {date} in datepicker")
    CALENDER_DIV_XPATH = '//*[@id="ui-datepicker-div"]'
    calendar_div = driver.find_element(By.XPATH, CALENDER_DIV_XPATH)

    calendar_month_dropdown = Select(
        calendar_div.find_element(By.CLASS_NAME, "ui-datepicker-month")
    )

    calendar_year_dropdown = Select(
        calendar_div.find_element(By.CLASS_NAME, "ui-datepicker-year")
    )

    # months are zero-indexed
    calendar_month_dropdown.select_by_value(str(date.month - 1))
    time.sleep(1)

    calendar_year_dropdown.select_by_value(str(date.year))
    time.sleep(1)

    calender_table_element = calendar_div.find_element(
        By.CLASS_NAME, "ui-datepicker-calendar"
    )
    calendar_tbody = calender_table_element.find_element(By.TAG_NAME, "tbody")
    calendar_dates = calendar_tbody.find_elements(By.TAG_NAME, "td")

    date_element_to_choose = list(
        filter(lambda date_element: date_element.text == str(date.day), calendar_dates)
    )[0]
    date_element_to_choose.click()

    print("done")
    time.sleep(1)


def download_transaction_list(
    driver: webdriver.Firefox, from_date: datetime.date, to_date: datetime.date
) -> None:
    """Download transactions between from_date and to_date range"""
    print(f"trying to download transactions from {from_date} to {to_date}")
    # Choose options to get transaction list
    driver.switch_to.frame("main_part")
    time.sleep(1)

    # Choose Savings account option, and account number
    ACCOUNT_TYPE_SELECT_XPATH = "/html/body/form/table[1]/tbody/tr[1]/td[2]/select"
    account_type_select = Select(
        driver.find_element(By.XPATH, ACCOUNT_TYPE_SELECT_XPATH)
    )
    account_type_select.select_by_value("SCA")

    ACCOUNT_NO_SELECT_XPATH = "/html/body/form/table[1]/tbody/tr[2]/td[2]/select"
    account_no_select = Select(driver.find_element(By.XPATH, ACCOUNT_NO_SELECT_XPATH))
    account_no_select.select_by_value(
        "00101460006100  "
    )  # there are 2 spaces in the end for some reason

    # Choose custom period button
    SELECT_PERIOD_XPATH = "/html/body/form/table[1]/tbody/tr[4]/td[1]/span"
    driver.find_element(By.XPATH, SELECT_PERIOD_XPATH).click()

    # open from-date calendar
    FROM_DATE_CALENDAR_BUTTON_XPATH = (
        "/html/body/form/table[1]/tbody/tr[4]/td[2]/div[2]/button/span[1]"
    )
    driver.find_element(By.XPATH, FROM_DATE_CALENDAR_BUTTON_XPATH).click()
    choose_date_in_calendar(driver, date=from_date)

    # open to-date calendar
    TO_DATE_CALENDAR_BUTTON_XPATH = (
        "/html/body/form/table[1]/tbody/tr[5]/td[2]/div[2]/button/span[1]"
    )
    driver.find_element(By.XPATH, TO_DATE_CALENDAR_BUTTON_XPATH).click()
    choose_date_in_calendar(driver, date=to_date)

    # get list of transactions
    VIEW_BUTTON_XPATH = "/html/body/form/table[1]/tbody/tr[7]/td/a"
    driver.find_element(By.XPATH, VIEW_BUTTON_XPATH).click()

    time.sleep(2)

    # select download format as excel, and download
    download_format_select = Select(driver.find_element(By.NAME, "fldFormatType"))
    download_format_select.select_by_value("X")
    DOWNLOAD_BUTTON_XPATH = "/html/body/form/table[5]/tbody/tr[2]/td/a"
    driver.find_element(By.XPATH, DOWNLOAD_BUTTON_XPATH).click()

    today = datetime.date.today()
    print(
        f"""downloading transaction excel sheet for {from_date}/{today.month}/{today.year} to {to_date}/{today.month}/{today.year} range"""
    )

    time.sleep(2)


def quit(driver: webdriver.Firefox) -> None:
    driver.close()
    print("quit driver")


if __name__ == "__main__":
    driver = init_driver_with_options()
    login_to_site(driver)
    navigate_to_account_statement(driver)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    download_transaction_list(driver, from_date=yesterday, to_date=today)
    quit(driver)

    transactions_dir = Path.cwd() / "transaction_lists"
    latest_downloaded_file_path = list(
        sorted(transactions_dir.iterdir(), key=lambda file: file.name, reverse=True)
    )[0]
    parse_transactions(transactions_xls_file_path=str(latest_downloaded_file_path))
