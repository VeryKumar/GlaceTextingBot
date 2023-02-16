from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import config
import difflib

# Initialize driver
url = "https://asp.glaceemr.com/Glace/jsp/loginPage.jsp"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

# Set appiontment date
DATE = '2/7/2023'

# Helper methods
# Explicit Wait
def document_initialized(driver):
    if driver.execute_script("return document.readyState") == "complete":
        return True

# Login to portal
userInput = driver.find_element(By.ID, "txtUserName" )
userPass = driver.find_element(By.ID, "txtPWord")
accountInput = driver.find_element(By.ID, "accountID")

userInput.send_keys(config.USER)
userPass.send_keys(config.PASSWORD)
accountInput.send_keys(config.ACCOUNT_ID)
submit = driver.find_element(By.ID, "SubmitButton")
submit.click()

time.sleep(1)

# Portal navigation
acknowledgeBtn = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/button")

acknowledgeBtn.click()


time.sleep(1)

# Get today's appointments

scheduleBtn = driver.find_element(By.ID, "Home1")
action = ActionChains(driver)
action.move_to_element(scheduleBtn).perform()

calendarBtn = driver.find_element(By.XPATH, "/html/body/div[18]/div/table/tbody/tr[1]")
calendarBtn.click()
appointmentUrl = f"javascript:todaysAppointmentNew({DATE});"
# driver.find_element(By.XPATH, '//a[@href="'+appointmentUrl+'"]').click()
# print(appointmentUrl)
# driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

iframe = wait(driver, timeout=10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "MainWindow")))

appointments = wait(driver, timeout=10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title*='Appointments']")))




# links = driver.find_elements(By.TAG_NAME, "a")

# for link in links:
#     # if(link.get_attribute("href")) == appointmentUrl:
#     print(link.get_attribute("href"))

# print("appointments: ", appointments)
for appointment in appointments:
    a = appointment.get_attribute("href")
    b = appointmentUrl

    # print(appointment.get_attribute("href"), appointmentUrl)

    if DATE in appointment.get_attribute("href"):
        print(f"Found {DATE}'s appointment")
        # appointment.click()
# time.sleep(5)
# driver.close()
