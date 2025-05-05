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


def show_home_goals(driver):
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

    driver.find_element(CSS, '.v-overlay-container .v-list-item:nth-child(4)').click()
    time.sleep(2)


def test_task_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_goals(driver)

    driver.find_element(By.ID, 'add-goal').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("Check this goal works")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys(
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .bg-primary').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(2)
    driver.close()


def test_task_update_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_goals(driver)

    goal = driver.find_element(CSS, '.goal')
    start_title = driver.find_element(CSS, '.goal .text-uppercase').text
    start_description = driver.find_element(CSS, '.goal .text-grey').text

    goal.click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .v-toolbar-items > button:nth-child(2)').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("2")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys("3")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .bg-primary').click()
    time.sleep(1)

    assert driver.find_element(CSS, '.goal .text-uppercase').text == start_title + '2'
    assert driver.find_element(CSS, '.goal .text-grey').text == start_description + '3'
    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()


def test_task_target_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_goals(driver)

    driver.find_element(CSS, '.goal').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container button.bg-primary').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("Earn my first $100")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys(
        "Utilize a combination of Card properties and utility classes to create a unique funding card.")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container #goal-target-deadline').click()
    time.sleep(0.5)
    driver.find_element(CSS, '.v-date-picker-month__day .v-btn--variant-outlined').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .v-dialog:nth-child(2) button.bg-primary').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay-container .v-dialog:nth-child(2)')
    assert 'http://localhost:3000/home' == driver.current_url

    time.sleep(1)

    start_title = driver.find_element(CSS, '.target-card .text-h6').text
    start_description = driver.find_element(CSS, '.target-card .text-muted').text

    driver.find_element(CSS, '.v-overlay-container .target-card').click()
    time.sleep(2)

    driver.find_element(CSS, '.v-overlay-container input[name="title"]').send_keys("2")
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container textarea[name="description"]').send_keys("3")
    time.sleep(1)

    goal_deadline = driver.find_element(CSS, '.v-overlay-container #goal-target-deadline')
    goal_deadline.clear()
    time.sleep(0.5)
    goal_deadline.click()
    time.sleep(0.5)
    driver.find_element(CSS, '.v-date-picker-controls__month button:last-child').click()
    time.sleep(0.5)
    driver.find_element(CSS, '.v-date-picker-month__day button:last-child').click()
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .v-dialog:last-child button.bg-primary').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay-container .v-dialog:nth-child(2)')
    assert driver.find_element(CSS, '.target-card .text-h6').text == start_title + '2'
    assert driver.find_element(CSS, '.target-card .text-muted').text == start_description + '3'
    assert 'http://localhost:3000/home' == driver.current_url

    time.sleep(1)

    start_title = driver.find_element(CSS, '.target-card .text-h6').text

    driver.find_element(CSS, '.v-overlay-container .target-card').click()
    time.sleep(2)

    driver.find_element(CSS, '.v-overlay-container .v-dialog .v-card-actions button.bg-red').click()
    time.sleep(1)

    # Click Confirm Delete Button
    driver.find_element(CSS, '.v-overlay-container > .v-dialog:nth-of-type(3) .bg-red').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay-container .v-dialog:nth-child(2)')
    assert driver.find_element(CSS, '.target-card .text-h6').text != start_title
    assert 'http://localhost:3000/home' == driver.current_url

    time.sleep(1)
    driver.close()


def test_task_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_goals(driver)

    # Open First Task
    driver.find_element(CSS, '.goal').click()
    time.sleep(1)

    driver.find_element(CSS, '.v-overlay-container .v-toolbar-items > button:nth-child(1)').click()
    time.sleep(1)

    # Click Confirm Delete Button
    driver.find_element(CSS, '.v-overlay-container > .v-overlay:nth-of-type(2) .bg-red').click()
    time.sleep(1)

    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()
