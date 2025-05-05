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


def show_home_events(driver):
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

    driver.find_element(CSS, '.v-overlay-container .v-list-item:nth-child(2)').click()
    time.sleep(0.5)


def test_event_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_events(driver)

    driver.find_element(By.ID, 'add-event').click()
    time.sleep(0.5)

    title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
    title_input.send_keys("test event")
    time.sleep(0.5)

    desc_input = driver.find_element(CSS, '.v-overlay-container textarea[name="description"]')
    desc_input.send_keys("test description")
    time.sleep(0.5)

    # title_input = driver.find_element(CSS, '.v-overlay-container #event-date-picker')
    # title_input.send_keys(today_str)
    # time.sleep(0.5)

    start_input = driver.find_element(CSS, '.v-overlay-container .event-time-start .v-field__input')
    # start_input.send_keys("14:30")
    start_input.click()
    time.sleep(1)
    driver.find_element(CSS, '.event-start-time-picker > div.v-picker__body > div > div > div:nth-child(7)').click()
    time.sleep(1)
    driver.find_element(CSS, '.event-start-time-picker > div.v-picker__body > div > div > div:nth-child(7)').click()
    time.sleep(1)
    driver.find_element(CSS, '.v-overlay-container .close-time-picker').click()
    time.sleep(1)

    end_input = driver.find_element(CSS, '.v-overlay-container .event-time-end .v-field__input')
    # end_input.send_keys("14:30")
    end_input.click()
    time.sleep(1)
    driver.find_element(CSS, '.event-end-time-picker > div.v-picker__body > div > div > div:nth-child(10)').click()
    time.sleep(1)
    driver.find_element(CSS, '.event-end-time-picker > div.v-picker__body > div > div > div:nth-child(10)').click()
    time.sleep(1)
    driver.find_element(CSS, '.v-overlay-container .close-time-picker').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .v-card-actions button.bg-primary').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(2)
    driver.close()


def test_event_update_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_events(driver)

    event = driver.find_element(CSS, '.event-chip')
    start_text = event.text

    event.click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .text-primary[title="edit"]').click()
    time.sleep(1)

    title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
    title_input.send_keys("2")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .v-card-actions .bg-primary').click()
    time.sleep(2)

    updated_event = driver.find_element(CSS, '.event-chip')

    assert updated_event.text == start_text + '2'
    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()


def test_event_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_events(driver)

    driver.find_element(CSS, '.event-chip').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .text-red[title="delete"]').click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '.v-overlay-container button.bg-red').click()
    time.sleep(3)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()
