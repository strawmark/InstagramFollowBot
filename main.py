import credentials

import pyotp
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

browser_options = webdriver.EdgeOptions()
browser_options.add_experimental_option('detach', True)  # keep browser open

driver = webdriver.Edge(options=browser_options)

driver.get("https://www.instagram.com")
driver.implicitly_wait(10)

credentials = credentials.get()

# Reject cookies
try:
    reject_cookie_button = driver.find_element(By.CSS_SELECTOR, value='button._a9--._ap36._a9_1')
    reject_cookie_button.click()
except NoSuchElementException:
    pass

# Login

try:
    login_entries = driver.find_elements(By.CSS_SELECTOR, value='#loginForm input')
    login_button = driver.find_element(By.CSS_SELECTOR, value='#loginForm button')
    user_login_data = [credentials['username'], credentials['password']]

    for i, entry in enumerate(login_entries):
        entry.send_keys(user_login_data[i])
        sleep(randint(1, 2))

    try:
        login_button.click()
    except ElementClickInterceptedException:
        print('Wrong password: password is too short. Check "user_data.json"')
        exit(1)

    try:
        login_error_text = driver.find_element(By.CSS_SELECTOR,value='#loginForm ._ab2z')
        print('Credentials error. Check "user_data.json"')
        exit(1)
    except NoSuchElementException:
        pass

except NoSuchElementException:
    exit(1)

# 2FA (if exists)
try:
    otp_input = driver.find_element(By.NAME,'verificationCode')
    otp_confirmation_button = driver.find_element(By.CSS_SELECTOR,'._acap')
    otp_checkbox = driver.find_element(By.NAME,'checkbox')

    otp = pyotp.TOTP(credentials['otp_secret']).now()
    otp_input.send_keys(otp)
    sleep(1)

    otp_checkbox.click()
    sleep(randint(1,3))

    otp_confirmation_button.click()
    sleep(5)

except NoSuchElementException:
    pass # Account can be unprotected by 2FA

# Save access -> not now
try:
    save_access_button = driver.find_element(By.CSS_SELECTOR,value="[role='button']")
    save_access_button.click()
    sleep(1)
except NoSuchElementException:
    exit(1)

# Activate notifications -> not now
try:
    activate_notifications_button = driver.find_element(By.CSS_SELECTOR,"._a9--._ap36._a9_1")
    activate_notifications_button.click()
except NoSuchElementException:
    exit(1)

# Gather followers

target = credentials['target']

driver.get(f"https://instagram.com/{target}/")

follower_button = driver.find_element(By.CSS_SELECTOR,value=f"[href='/{target}/followers/']")
follower_button.click()
sleep(3)

followers_popup = driver.find_element(By.CSS_SELECTOR, value=".xyi19xy")

for i in range(10):
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
    sleep(2)

sleep(3)

followers = driver.find_elements(By.CSS_SELECTOR, value=".x1dm5mii")

followers_dict = [{'link': follower.find_element(By.CSS_SELECTOR, value='.x1rg5ohu a'),
                   'button': follower.find_element(By.CSS_SELECTOR,value=".xyi19xy [type='button']")} for follower in followers]

#Logout

driver.get(f"https://instagram.com/{target}/")
try:
    menu_button = driver.find_element(By.CSS_SELECTOR,value="[aria-describedby=':rc:']")
    menu_button.click()
    sleep(2)
    menu_popup = driver.find_element(By.CSS_SELECTOR,"div.xq9evs9")

    popup_buttons = menu_popup.find_elements(By.CSS_SELECTOR, value='[role="button"]')
    quit_button = popup_buttons[-1]
    quit_button.click()

except NoSuchElementException:
    exit(1)
finally:
    sleep(2)
    driver.quit()
