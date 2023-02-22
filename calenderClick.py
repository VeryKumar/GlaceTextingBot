from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
import time
import config

# Initialize driver
url = "https://asp.glaceemr.com/Glace/jsp/loginPage.jsp"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# Set appiontment date
DATE = '2/2/2023'

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
appointmentUrl = f"javascript:todaysAppointmentNew({DATE});"
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
    (By.CSS_SELECTOR, "a[href*='2/2/2023']")))
appointment = driver.find_element(
    By.CSS_SELECTOR, f"a[href*='2/7/2023']").click()
time.sleep(5)

# wait(driver, timeout=5).until(EC.presence_of_element_located(
#     (By.XPATH, f"//*[contains(@href, {DATE})]"))
# )
# appointment = driver.find_element(
#     By.XPATH, f"//*[contains(@href, {DATE})]").click()

# wait(driver, timeout=10).until(EC.presence_of_element_located(
#     (By.XPATH, f"//*[contains(@href, {DATE})]"))
# )
# driver.find_element(
#     By.XPATH, f"//*[contains(@href, {DATE})]").click()


# //*[contains(@href,"AppointmentNew('2/7/2023')")]
# //*[contains(@href,"AppointmentNew('2/7/2023')")]
# retry the action
# for appointment in appointments:
#     if DATE in appointment.get_attribute("href"):
#         print(f"Found {DATE}'s appointment")
#         driver.execute_sc xript("arguments[0].click();", appointment)
#     else:
#         print("not found")
# find_appointment_by_date(appointments, DATE)

# time.sleep(5)
# driver.close()
