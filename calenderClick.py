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
# Set appointment date

PeskyURL = "https://developers.google.com/oauthplayground/?code=4%2F0AWtgzh6e6jUrI8Lw89_8hCOD-80-mXasq_GkO_jeQmxoMxd8jfys7fFnkPzgF6dZw-z8MA&scope=email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+openid&authuser=0&prompt=consent"
skip_number = 0
DATE = '3/31/2023'

MODE = 'ACTIVE'
# MODE = 'TEST'

# Options for headless mode

# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")


# Initialize driver
url = "https://asp.glaceemr.com/Glace/jsp/loginPage.jsp"
driver = webdriver.Chrome()
driver.get(url)

# Patients Array

patients = []

# Helper methods

# Explicit Wait


def document_initialized(driver):
    if driver.execute_script("return document.readyState") == "complete":
        return True

# Find appointment by date


def find_appointment_by_date(appointments, DATE):
    for appointment in appointments:
        if DATE in appointment.get_attribute("href"):
            print(f"Found {DATE}'s appointment")
            appointment.click()
        else:
            print("not found")


# Login to portal

wait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtUserName")))
userInput = driver.find_element(By.ID, "txtUserName")
userPass = driver.find_element(By.ID, "txtPWord")
accountInput = driver.find_element(By.ID, "accountID")

userInput.send_keys(config.USER)
userPass.send_keys(config.PASSWORD)
accountInput.send_keys(config.ACCOUNT_ID)
submit = driver.find_element(By.ID, "SubmitButton")
submit.click()

time.sleep(1)

# Portal navigation
acknowledgeBtn = driver.find_element(
    By.XPATH, "/html/body/div[6]/div/div[1]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/button")

acknowledgeBtn.click()


time.sleep(1)

# Get today's appointments

scheduleBtn = driver.find_element(By.ID, "Home1")
action = ActionChains(driver)
action.move_to_element(scheduleBtn).perform()

calendarBtn = driver.find_element(
    By.XPATH, "/html/body/div[18]/div/table/tbody/tr[1]")
calendarBtn.click()

# appointmentUrl = f"javascript:todaysAppointmentNew({DATE});"
# driver.find_element(By.XPATH, '//a[@href="'+appointmentUrl+'"]').click()
# print(appointmentUrl)
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

iframe = wait(driver, timeout=10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "MainWindow")))

# appointments = wait(driver, timeout=10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title*='Appointments']")))
# appointments = driver.find_elements(
#     By.CSS_SELECTOR, "a[title*='Appointments']")
# re-locate the element or refresh the page
wait(driver, timeout=10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a[title*='Appointments']")))
calClick = driver.find_element(
    By.CSS_SELECTOR, "a[title*='Appointments']").click()
time.sleep(3)
wait(driver, timeout=10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, f"a[href*='{DATE}']")))

appointment = driver.find_element(
    By.CSS_SELECTOR, f"a[href*='{DATE}']")
time.sleep(8)
action.click(appointment).perform()
time.sleep(8)

# At appointment with provided date
wait(driver, timeout=10).until(EC.presence_of_element_located(
    (By.XPATH, "//span[contains(@id, 'appt')]")))

patientsAtDate = driver.find_elements(
    By.XPATH, "//span[contains(@id, 'appt')]")

count = 0

for patient in patientsAtDate:
    patientDict = {}

    action.double_click(patient).perform()
    time.sleep(3)

    patientName = driver.find_element(By.ID, "pat_name")
    patientDict["name"] = patientName.get_attribute('value')
    print("name", patientName.get_attribute('value'))

    appointmentTme = driver.find_element(By.ID, "time")
    print("time", appointmentTme.get_attribute('value'))
    patientDict["time"] = appointmentTme.get_attribute('value')

    homephone = driver.find_element(By.ID, "phone_num")
    print("home num", homephone.get_attribute('value'))
    patientDict["homephone"] = homephone.get_attribute('value')

    cellphone = driver.find_element(By.ID, "cell_num")
    print("cell num", cellphone.get_attribute('value'))
    patientDict["cellphone"] = cellphone.get_attribute('value')

    closeBtn = driver.find_element(
        By.XPATH, "//a[@onclick='javascript:closecovid()']")
    closeBtn.click()

    patients.append(patientDict)


# Generate text message
patients = patients[skip_number:]
with SB(uc=True) as gdriver:

    # Initialize driver + Login

    gdriver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    gdriver.type("#identifierId", gvoice.USER)
    gdriver.click("#identifierNext > div > button")
    gdriver.type(
        "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", gvoice.PASSWORD)
    gdriver.click("#passwordNext > div > button")
    print('made it past login')
    # Navigate to Google Voice

    gdriver.get("https://voice.google.com/")
    print('made it to voice.google.com')
    time.sleep(1)
    personalUseBtnPath = "/html/body/div[2]/div[3]/div/button/span"
    gdriver.wait_for_element(personalUseBtnPath, timeout=100)
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
    for patient in patients:
        print(f"currently sending txt to {patient['name']}")

        txt = f"Hello {patient['name']}, this is Dr.Kumar's office letting you know that you have an appointment on {DATE} at {patient['time']}. You can text Y to confirm your appointment. Thank you!"

        textInputXPath, numberInputXPath = "//textarea", "//input[@gv-test-id='recipient-picker-input']"

        if MODE == "TEST":
            gdriver.type(numberInputXPath, 0000000000)
        if MODE == "ACTIVE":
            if patient["cellphone"] != "" and patient["cellphone"] != "0000000000":
                gdriver.type(
                    numberInputXPath, patient["cellphone"] + Keys.RETURN)
            else:
                gdriver.type(
                    numberInputXPath, patient["homephone"] + Keys.RETURN)

        gdriver.type(textInputXPath, txt)
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
