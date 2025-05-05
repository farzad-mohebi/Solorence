import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from workspace.tests.driver_utils import DriverUtils


def test_login_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver.get('http://localhost:3000/login')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_username"))
    )
    time.sleep(2)
    # Find and fill in the username and password fields
    username_input = driver.find_element(By.ID, "id_username")
    time.sleep(0.5)
    username_input.send_keys("string")

    password_input = driver.find_element(By.ID, "id_password")
    time.sleep(0.5)
    password_input.send_keys("string")

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    check = 0
    while check <= 5:
        time.sleep(1)
        if driver.current_url == 'http://localhost:3000/home':
            break
        check += 1

    # Check that the user is redirected to the homepage after login
    final_url = driver.current_url
    cookies = driver.get_cookies()

    # Store cookies in a file
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    driver.close()
    assert 'http://localhost:3000/home' == final_url
