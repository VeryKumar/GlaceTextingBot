from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from seleniumbase import SB
import time
import config
import gvoice
import dummyPtArr as patients

DATE = '3/20/2023'


with SB(uc=True) as gdriver:

    # Initialize driver + Login

    gdriver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    gdriver.type("#identifierId", gvoice.USER)
    gdriver.click("#identifierNext > div > button")
    gdriver.type(
        "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", gvoice.PASSWORD)
    gdriver.click("#passwordNext > div > button")

    # Navigate to Google Voice

    gdriver.get("https://voice.google.com/")
    time.sleep(1)
    personalUseBtnPath = "/html/body/div[2]/div[3]/div/button/span"
    gdriver.click(personalUseBtnPath)
    time.sleep(1)
    webBtnPath = "/html/body/div[2]/div[3]/div/div/button[3]/span"
    gdriver.click(webBtnPath)
    time.sleep(1)
    messageBtnPath = "/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-side-nav/div/div/gmat-nav-list/a[2]/div"
    gdriver.click(messageBtnPath)
    newMessageBtnPath = "/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/div/gv-messaging-view/div/div/md-content/div/div/div"
    gdriver.click(newMessageBtnPath)
    print('clicked on elem 2')

    # Send message
    for patient in patients.patients:

        txt = f"Hello {patient['name']}, this is Dr.Kumar's office letting you know that you have an appointment on {DATE} at {patient['time']}. You can text Y to confirm your appointment. Thank you!"

        textInputXPath, numberInputXPath = "//textarea", "//input[@gv-test-id='recipient-picker-input']"

        gdriver.type(numberInputXPath, "0000000000" + Keys.RETURN)
        gdriver.type(textInputXPath, txt)

        # if patient["cellphone"] != "" and patient["cellphone"] != "0000000000":
        #     gdriver.type(
        #         numberInputXPath, patient["cellphone"] + Keys.RETURN)
        # else:
        #     gdriver.type(
        #         numberInputXPath, patient["homephone"] + Keys.RETURN)

        time.sleep(1)
        sendBtnPath = "#ib2"
        gdriver.click(sendBtnPath)
        print('clicked send')
        # close = "//*[@id='mat-chip-list-0']/div/gmat-input-chip/mat-icon"
        # gdriver.click(close)
        time.sleep(1)
        newMessageButtonPath = "//div[@gv-id='send-new-message']"
        gdriver.click(newMessageButtonPath)
        print('clicked new message')
        # action = ActionChains(driver)
        # newMessageButton = driver.find_element_by_xpath(
        #     newMessageButtonPath)
        # action.move_to_element(newMessageButton).perform()

    # gdriver.type("#input_1", "test-message")
    # # print(patients)
    # gdriver.type("#input_0", "7164744839" + Keys.RETURN)
    # time.sleep(1)
    # sendBtnPath = "#ib2"
    # # gdriver.click(sendBtnPath)
    # close = "//*[@id='mat-chip-list-0']/div/gmat-input-chip/mat-icon"
    # gdriver.click(close)
    time.sleep(100)
