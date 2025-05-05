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


def show_home_tasks(driver):
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

    driver.find_element(CSS, '.v-overlay-container .v-list-item:nth-child(3)').click()
    time.sleep(0.5)


def test_task_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_tasks(driver)

    driver.find_element(By.ID, 'add-task').click()
    time.sleep(0.5)

    title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
    title_input.send_keys("test task")
    time.sleep(0.5)

    status_input = driver.find_element(CSS, '.v-overlay-container .task-status')
    status_input.click()
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .v-list-item:nth-child(2)').click()
    time.sleep(0.5)

    title_input = driver.find_element(CSS, '.v-overlay-container #task-due-date')
    title_input.send_keys(today_str)
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

    show_home_tasks(driver)

    task = driver.find_element(CSS, '.task.v-list-item')
    start_text = task.text

    task.click()
    time.sleep(1)

    title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
    title_input.send_keys("2")
    time.sleep(0.5)

    driver.find_element(CSS, '.v-overlay-container .bg-primary').click()
    time.sleep(1)

    updated_task = driver.find_element(CSS, '.task.v-list-item')

    assert updated_task.text == start_text + '2'
    assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()


def test_task_done_checkbox_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_tasks(driver)
    first_task_css = '.task.v-list-item:nth-of-type(2)'
    task = driver.find_element(CSS, first_task_css)
    checkbox = task.find_element(CSS, '[type="checkbox"]')
    if checkbox.get_attribute('checked'):  # Set Task to Open for Start
        checkbox.click()
        time.sleep(0.5)

    checked = checkbox.get_attribute('checked')
    if not checked:  # if Task is Open or Pending
        checkbox.click()  # Set Task to Done
        time.sleep(0.5)

        # Check is text line through Added
        assert DriverUtils.check_exists_by_css(driver, first_task_css + ' .text-decoration-line-through')

        # Check Task Checkbox is Checked
        assert driver.find_element(CSS, first_task_css + ' [type="checkbox"]').get_attribute('checked') != checked

        # Refresh the Page
        driver.refresh()
        time.sleep(3)
        assert driver.find_element(CSS, first_task_css + ' [type="checkbox"]').get_attribute('checked') != checked

    task = driver.find_element(CSS, first_task_css)
    checkbox = task.find_element(CSS, '[type="checkbox"]')
    checked = checkbox.get_attribute('checked')
    if checked:  # if Task is Done
        checkbox.click()  # Set Task to Open
        time.sleep(1)

        # Check is text line through Removed
        assert not DriverUtils.check_exists_by_css(driver, first_task_css + ' .text-decoration-line-through')

        # Check Task Checkbox is NOT Checked
        assert driver.find_element(CSS, first_task_css + ' [type="checkbox"]').get_attribute(
            'checked') != checked

        # Refresh the Page
        driver.refresh()
        time.sleep(3)
        # Check Task Checkbox is Checked after Refresh
        assert driver.find_element(CSS, first_task_css + ' [type="checkbox"]').get_attribute('checked') != checked

    assert 'http://localhost:3000/home' == driver.current_url
    time.sleep(1)
    driver.close()


def test_task_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    show_home_tasks(driver)

    # Open First Task
    driver.find_element(CSS, '.task.v-list-item').click()
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
