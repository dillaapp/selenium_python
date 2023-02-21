import logging
import os

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service

desired_capabilities = DesiredCapabilities().CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True

s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, desired_capabilities=desired_capabilities)
browser.implicitly_wait(10)

#############################################################################################################################################
# Logging format starts here
"""This will format the message style and color"""
FMT = "{message}"  # i.e [INFO] root: Info Message
Formats = {
    logging.DEBUG: f"\33[37m{FMT}\33[0m",  # debug is gray
    logging.INFO: f"\33[36m{FMT}\33[0m",  # Info is green
    logging.WARNING: f"\33[33m{FMT}\33[0m",  # Warning is yellowish
    logging.ERROR: f"\33[31m{FMT}\33[0m",  # Error is red
    logging.CRITICAL: f"\33[1m\33[33m{FMT}\33[0m",  # Critical is yellowish

}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = Formats[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)


handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logging.basicConfig(
    level=logging.INFO,  # it will only start printing from Info and downwards (Info, Warning, Error and Critical)
    handlers=[handler],
    # filename=r"C:\Users\User\PycharmProjects\Selenium\Data\logfile.log"
)


# Logging format ends here

# Printing out time duration for function run Start
def print_timeDuration(stratSecs, endSecs):
    # Total duration = End time - start time
    time_duration = round(float(endSecs) - float(stratSecs), 2)

    # Editing the time fro display
    if time_duration <= 60:
        logging.info("Total duration: {} secs.".format(time_duration))
    elif time_duration > 60 and time_duration <= 3600:
        mins = round(time_duration / 60, 2)
        logging.info("Total duration: {} mins.".format(mins))
    elif time_duration > 3600 and time_duration <= 216000:
        hours = round(time_duration / 3600, 2)
        logging.info("Total duration: {} hours.".format(hours))
    else:
        days = round(time_duration / 86400, 2)
        logging.info("Total duration: {} days.".format(days))


# Printing out time duration for function run End


# root directory
"""This is so we dont have to change our local directory every time we pull some changes from the remote repo"""
ROOT_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..'))  ## C:\XXX\XXX\PycharmProjects\Selenium........


# Read file function
def readfile(Filepath):
    df = pd.read_csv(Filepath, sep=";", dtype=str)  # , sep='delimiter'
    return df


# Open Url
def Openurl(URL):
    browser.get(URL)


# Alert when something is wrong - START
def alert():
    """This function will create alert box"""
    create_alert = "alert('Something is wrong, check the log before clicking *Ok*');"
    browser.execute_script(create_alert)
    browser.switch_to.alert


def isAlertPresent():
    """This function checks is there is alert box in the window and returns "True" if there is one;
    returns "False" if there is no alert box (or when you click ok the alert box; the alert box is gone)"""
    global alertvisible
    alertvisible = True
    try:
        wait = WebDriverWait(browser, timeout=1)
        wait.until(EC.alert_is_present())
        return alertvisible
    except:
        alertvisible = False
        return alertvisible


def holdAlert(holdAlertText):
    """This Function print error message in the log every 3 secs until the alert box is invisible on the window"""
    while alertvisible:
        logging.error("{}".format(holdAlertText))
        isAlertPresent()
        time.sleep(2)
    logging.info("to continue")


# Alert when something is wrong - END


# Dropdown Validation
def ValidateDrpDwnListByXPATH(Element, Data):
    """
        Checks if elements in dropdown list are present
        :param Element: Dropdown elements XPATH
        :param Data: Values / data you want you check -  Pulled from test data
        :return: Pass / Fail / Exception
        """
    try:
        # Dropdown list
        DropdownList = browser.find_element(by=By.XPATH, value=Element)
        select = Select(DropdownList)
        DrpList = []

        # Converting comma separated strings into a list
        Assertlist = [x.strip() for x in Data.split(',')]

        # Empty list to put the list that are not in the dropdown
        MissingDrpList = []

        # This is to create a list of elements from the dropdown
        for x in select.options:
            DrpList.append(x.text)
        # This is to compare the list from the dropdown with the list from excel
        for value in Assertlist:
            if value not in DrpList:
                if value not in MissingDrpList:
                    MissingDrpList.append(value)

        if len(MissingDrpList) == 0:
            logging.info("ValidateDrpDwnListByID :{} - Nothing is missing - PASSED".format(Element))
        else:
            logging.error("The Following are missing from the dropdown list {} - FAILED".format(Element))
            # Alert when something is wrong - START
            holdAlertText = "ValidateDrpListByXPATH :", Element, " - FAILED"
            alert()
            isAlertPresent()
            holdAlert(holdAlertText)
            # Alert when something is wrong - END

    except Exception as e:
        exceptionMsg = "ValidateDrpDwnListByXPATH - FAILED."
        logging.error("{}".format(exceptionMsg))
        logging.critical(e)
        # Alert when something is wrong - START
        holdAlertText = "ValidateDrpDwnListByXPATH - FAILED."
        alert()
        isAlertPresent()
        holdAlert(holdAlertText)
        # Alert when something is wrong - END
