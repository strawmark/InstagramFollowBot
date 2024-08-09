import os
import pyotp
from random import randint
from time import sleep

from fontTools.misc.cython import returns
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser_options = webdriver.EdgeOptions()
browser_options.add_experimental_option('detach', True)  # keep browser open

driver = webdriver.Edge(options=browser_options)

driver.get("https://www.instagram.com")
driver.implicitly_wait(randint(3,5))

reject_cookie_button = driver.find_element(By.CSS_SELECTOR, value='button._a9--._ap36._a9_1')

if reject_cookie_button:    # Reject cookies
    reject_cookie_button.click()
    sleep(1)

login_entries = driver.find_elements(By.CSS_SELECTOR, value='#loginForm input')
login_button = driver.find_element(By.CSS_SELECTOR, value='#loginForm button')

if login_entries:
    user_login_data = [os.getenv("USERNAME"), os.getenv("PASSWORD")]

    for i, entry in enumerate(login_entries):
        entry.send_keys(user_login_data[i])
        sleep(randint(1,2))

    sleep(0.5)
    login_button.click()

else:
    exit(1)

#2FA (if exists)
sleep(randint(3, 5))
otp_input = driver.find_element(By.NAME,'verificationCode')
otp_confirmation_button = driver.find_element(By.CSS_SELECTOR,'._acap')
otp_checkbox = driver.find_element(By.NAME,'checkbox')

if otp_input:
    otp = pyotp.TOTP(os.getenv('OTP_SECRET')).now()
    otp_input.send_keys(otp)
    sleep(1)
    otp_checkbox.click()
    sleep(randint(1,3))
    otp_confirmation_button.click()
    sleep(5)

# Save access -> not now
save_access_button = driver.find_element(By.XPATH,"//*[contains(text(), 'Non ora')]") # Should switch to a better selector

if save_access_button is not None:
    save_access_button.click()
else:
    page = driver.find_element(By.CSS_SELECTOR,'html')
    page.send_keys(Keys.TAB)
    page.send_keys(Keys.TAB)
    page.send_keys(Keys.ENTER)

# Activate notifications -> not now
sleep(1)
activate_notifications_button = driver.find_element(By.CSS_SELECTOR,"._a9--._ap36._a9_1")

if activate_notifications_button:
    activate_notifications_button.click()
else:
    page = driver.find_element(By.CSS_SELECTOR,'html')
    page.send_keys(Keys.TAB)
    page.send_keys(Keys.TAB)
    page.send_keys(Keys.ENTER)

