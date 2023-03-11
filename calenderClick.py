from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from seleniumbase import SB
import time
import config
import gvoice


# Set appiontment date
DATE = '2/2/2023'

# Initialize driver
# url = "https://asp.glaceemr.com/Glace/jsp/loginPage.jsp"
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get(url)

# Patients Array

patients = []
'''
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

wait(driver, timeout=10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "a[href*='3/2/2023']")))

appointment = driver.find_element(
    By.CSS_SELECTOR, f"a[href*='3/28/2023']")
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

'''

# driver.get("https://www.google.com")
# driver.get("https://voice.google.com/")
# time.sleep(2)
# signUp = driver.find_element(By.XPATH, "//a[contains(@href, 'sign')]")
# signUp.click()
# driver.find_element(By.ID, "identifierId").send_keys(gvoice.USER)
# time.sleep(3)
# driver.find_elements(By.XPATH, "//button")[2].click()
# time.sleep(3)

with SB(uc=True) as driver:
    driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    driver.type("#identifierId", gvoice.USER)
    driver.click("#identifierNext > div > button")

    driver.type(
        "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", gvoice.PASSWORD)
    driver.click("#passwordNext > div > button")
    driver.get("https://voice.google.com/")
    time.sleep(1)
    driver.click("/html/body/div[2]/div[3]/div/button/span")
    time.sleep(1)
    driver.click("/html/body/div[2]/div[3]/div/div/button[3]/span")
    time.sleep(1)
    driver.click(
        "/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/gv-side-nav/div/div/gmat-nav-list/a[2]/div")
    driver.click(
        "/html/body/div[1]/div[2]/gv-side-panel/mat-sidenav-container/mat-sidenav-content/div/div[2]/div/gv-messaging-view/div/div/md-content/div/div/div")
    # driver.type("//*[@id='input_0']", "test-number")
    driver.send_keys("#input_0", "test-number")
    driver.type("#input_1", "test-message")

    time.sleep(100)
    # driver.save_screenshot("test.png")
