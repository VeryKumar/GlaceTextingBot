from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

import time
 
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://asp.glaceemr.com/Glace/jsp/loginPage.jsp")


# text method is used in python to retrieve the text of WebElement
# login to portal
userInput = driver.find_element(By.ID, "txtUserName" )
userPass = driver.find_element(By.ID, "txtPWord")
accountInput = driver.find_element(By.ID, "accountID")

userInput.send_keys("")
userPass.send_keys("")
accountInput.send_keys("eclinic")
submit = driver.find_element(By.ID, "SubmitButton")
submit.click()

time.sleep(1)

# Portal navigation
acknowledgeBtn = driver.find_element(By.XPATH, "/html/body/div[6]/div/div[1]/div/div/div[1]/div/div/div[3]/div/div[2]/div[1]/button")

acknowledgeBtn.click()


time.sleep(1)

# Get today's appointments

scheduleBtn = driver.find_element(By.ID, "Home1")
# scheduleBtn.click()
action = ActionChains(driver)
action.move_to_element(scheduleBtn).perform()

todaysAppointmentsBtn = driver.find_element(By.XPATH, "/html/body/div[18]/div/table/tbody/tr[2]/td")
todaysAppointmentsBtn.click()
time.sleep(7)

booking = driver.find_element(By.ID, "dateGobalLabel")

print(booking.text)

# settingsBtn = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[7]")

# settingsBtn.click()

# classicViewBtn = driver.find_element(By.ID, "ClassicViewAnchorElem")
# classicViewBtn.click()
time.sleep(5)
driver.close()
