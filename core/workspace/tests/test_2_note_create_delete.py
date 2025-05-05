import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from workspace.tests.driver_utils import DriverUtils


def test_note_create_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "create-note"))
    )
    time.sleep(2)

    # Submit the form
    driver.find_element(By.ID, 'create-note').click()

    check = 0
    while check <= 5:
        time.sleep(1)
        if 'http://localhost:3000/note/' in driver.current_url:
            break
        check += 1

    assert 'http://localhost:3000/note/' in driver.current_url

    driver.close()


def test_note_move_to_trash_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".note-card"))
    )
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '.note-card').click()
    time.sleep(2)

    assert DriverUtils.arrived_to_url(driver, '/note/')

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id-show-note-toolbar"))
    )
    driver.find_element(By.ID, 'id-show-note-toolbar').click()
    time.sleep(1)

    driver.find_element(By.ID, 'id-show-note-delete').click()
    time.sleep(1)

    driver.find_element(By.ID, 'id-note-delete').click()
    time.sleep(3)

    final_url = driver.current_url
    driver.close()
    assert 'http://localhost:3000/home' == final_url



def test_note_delete_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    driver.get('http://localhost:3000/home')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".trash-note-card"))
    )
    driver.find_element(By.CSS_SELECTOR, '.trash-note-card').click()

    assert DriverUtils.arrived_to_url(driver, '/note/')

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "id-show-note-toolbar"))
    )
    driver.find_element(By.ID, 'id-show-note-toolbar').click()
    time.sleep(1)

    driver.find_element(By.ID, 'id-show-note-delete').click()
    time.sleep(1)

    driver.find_element(By.ID, 'id-note-delete').click()
    time.sleep(3)

    final_url = driver.current_url
    driver.close()
    assert 'http://localhost:3000/home' == final_url

