import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from workspace.tests.driver_utils import DriverUtils
import datetime

CSS = By.CSS_SELECTOR
today = datetime.datetime.today()
today_str = today.strftime("%m/%d/%Y")


def show_home_journeys(driver):
    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((CSS, ".home-show-mode"))
    )
    time.sleep(1)

    # Submit the form
    home_show_mode = driver.find_element(CSS, '.home-show-mode')
    time.sleep(0.5)
    home_show_mode.click()
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .v-list-item:nth-child(5)').click()
    time.sleep(0.5)


def test_journey_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_journeys(driver)

    driver.find_element(By.ID, 'add-journey').click()
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("test journey")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys("test description")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .bg-primary').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(2)
    driver.close()


def test_journey_update_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_journeys(driver)

    driver.find_element(CSS, '.journey .v-card-title button').click()
    start_title = driver.find_element(CSS, '.journey .v-card-title').text
    start_description = driver.find_element(CSS, '.journey .v-card-text').text
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("2")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys("3")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .bg-primary').click()
    time.sleep(1)

    assert driver.find_element(CSS, '.journey .v-card-title').text == start_title + '2'
    assert driver.find_element(CSS, '.journey .v-card-text').text == start_description + '3'
    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()


def test_journey_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_journeys(driver)

    # Open First Task
    driver.find_element(CSS, '.journey .v-card-title button').click()
    time.sleep(1)

    # Click Delete Button
    driver.find_element(CSS, '.v-overlay-container .bg-red').click()
    time.sleep(1)

    # Click Confirm Delete Button
    driver.find_element(CSS, '.v-overlay-container > .v-overlay:nth-of-type(2) .bg-red').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()
