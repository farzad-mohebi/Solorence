import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from workspace.tests.driver_utils import DriverUtils


def test_template_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "create-template"))
    )
    time.sleep(2)

    # Submit the form
    driver.find_element(By.ID, 'create-template').click()

    assert DriverUtils.arrived_to_url(driver, '/template/')

    assert '/template/' in driver.current_url

    driver.close()


def test_template_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".template-card"))
    )
    DriverUtils.delete_nuxt_dev_tools(driver)

    driver.find_element(By.CSS_SELECTOR, '.template-card').click()

    assert DriverUtils.arrived_to_url(driver, '/template/')

    driver.find_element(By.ID, 'id-show-template-toolbar').click()
    time.sleep(1)

    driver.find_element(By.ID, 'id-template-delete').click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '.v-overlay-container button.bg-red').click()
    time.sleep(3)

    final_url = driver.current_url
    driver.close()
    assert 'http://localhost:3000/home' == final_url
