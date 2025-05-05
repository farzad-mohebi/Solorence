import random

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from workspace.tests.driver_utils import DriverUtils
import datetime

CSS = By.CSS_SELECTOR
today = datetime.datetime.today()
today_str = today.strftime("%m/%d/%Y")


def test_note_editor_functionality():
    driver = DriverUtils.get_chrome_driver()
    driver = DriverUtils.login_and_return(driver)

    def add_empty_block():
        page_len = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
        match = False
        while not match:
            last_count = page_len
            time.sleep(0.25)
            page_len = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
            if last_count == page_len:
                match = True
        action = ActionBuilder(driver)
        action.pointer_action.move_to_location(500, 800)
        action.pointer_action.click()
        action.perform()
        time.sleep(0.25)

    def activate_editor(prepend_qs=''):
        if not prepend_qs:
            if DriverUtils.check_exists_by_css(driver, prepend_qs + ' .ce-block:last-child .edit-page-holder') or \
                    DriverUtils.check_exists_by_css(driver, prepend_qs + ' .ce-block:last-child .task-holder') or \
                    DriverUtils.check_exists_by_css(driver, prepend_qs + ' .ce-block:last-child .edit-board-holder'):
                add_empty_block()
        element = driver.find_element(CSS, prepend_qs + ' .ce-block:last-child')
        element.click()
        time.sleep(0.5)

    def show_toolbar(prepend_qs=''):
        activate_editor(prepend_qs)
        driver.find_element(CSS, prepend_qs + ' .ce-toolbar__plus').click()
        time.sleep(0.5)

    # driver.find_element(By.ID, 'create-note').click()
    # time.sleep(0.5)

    driver.get('http://localhost:3000/note/57')
    DriverUtils.arrived_to_url(driver, '/note/')
    time.sleep(2)

    activate_editor()

    # Paragraph
    def test_paragraph(prepend_qs=''):
        show_toolbar(prepend_qs)
        paragraph_tool = driver.find_element(CSS, prepend_qs + ' .ce-popover-item[data-item-name="paragraph"]')
        paragraph_tool.click()
        active_element = driver.switch_to.active_element
        active_element.send_keys("As per the documentation switches to the element that currently has focus within.")
        time.sleep(0.5)

    # Header
    def test_header():
        show_toolbar()
        header_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="header"]')
        header_tool.click()
        active_element = driver.switch_to.active_element
        active_element.send_keys("Header Test")
        time.sleep(0.5)

    # Delimiter
    def test_delimiter():
        show_toolbar()
        delimiter_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="delimiter"]')
        delimiter_tool.click()
        time.sleep(0.5)

    # Checklist
    def test_checklist():
        for n in range(3):
            show_toolbar()
            delimiter_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="checklist"]')
            delimiter_tool.click()
            time.sleep(0.5)
            active_element = driver.switch_to.active_element
            active_element.send_keys("Check box " + str(n))
            time.sleep(0.5)
        driver.find_element(CSS, '.ce-block:last-child .cdx-checklist__item-checkbox-check').click()
        assert DriverUtils.check_exists_by_css(driver, '.cdx-checklist__item--checked')

    # List
    def test_list():
        show_toolbar()
        driver.find_element(CSS, '.ce-popover-item[data-item-name="list"]').click()
        time.sleep(0.25)
        active_element = driver.switch_to.active_element
        for n in range(3):
            active_element = driver.switch_to.active_element
            active_element.send_keys("List item #" + str(n))
            time.sleep(0.25)
            active_element = driver.switch_to.active_element
            active_element.send_keys(Keys.ENTER)
            time.sleep(0.25)
            active_element = driver.switch_to.active_element
        active_element.send_keys(Keys.TAB)
        time.sleep(0.25)
        active_element = driver.switch_to.active_element
        for n in range(3):
            active_element = driver.switch_to.active_element
            active_element.send_keys("Sub list item #" + str(n))
            time.sleep(0.25)
            active_element.send_keys(Keys.ENTER)
            active_element = driver.switch_to.active_element
            time.sleep(0.25)
        active_element.send_keys(Keys.TAB)
        time.sleep(0.25)
        for n in range(3):
            active_element = driver.switch_to.active_element
            active_element.send_keys("Third list item #" + str(n))
            time.sleep(0.25)
            active_element.send_keys(Keys.ENTER)
            time.sleep(0.25)
        active_element = driver.switch_to.active_element
        active_element.send_keys(Keys.ENTER)
        time.sleep(0.25)
        active_element = driver.switch_to.active_element
        active_element.send_keys(Keys.ENTER)
        time.sleep(0.25)
        active_element = driver.switch_to.active_element
        active_element.send_keys(Keys.ENTER)

    # Page
    def test_page():
        if not DriverUtils.check_exists_by_css(driver, '.bg-yellow-lighten-3:last-child'):
            show_toolbar()
            page_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="page"]')
            page_tool.click()
            time.sleep(0.5)
            driver.find_element(CSS, '.bg-yellow-lighten-3:last-child').click()
            time.sleep(0.5)

        time.sleep(1)

        page_title_input = driver.find_element(CSS, '.v-overlay-container input[placeholder="page_title"]')
        page_title_input.clear()
        time.sleep(0.5)
        page_title_input.send_keys("Example page name")
        time.sleep(0.5)

        activate_editor('#pageEditor')
        time.sleep(0.5)
        test_paragraph('#pageEditor')

        driver.find_element(CSS, '.v-overlay-container .v-card-text .bg-green').click()
        time.sleep(2)

        assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
        time.sleep(1)
        add_empty_block()

    # Meet
    def test_meet():
        show_toolbar()
        meet_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="meet"]')
        meet_tool.click()
        time.sleep(3)

        title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
        title_input.send_keys("test")
        time.sleep(0.5)

        desc_input = driver.find_element(CSS, '.v-overlay-container textarea[name="description"]')
        desc_input.send_keys("test description")
        time.sleep(0.5)

        # title_input = driver.find_element(CSS, '.v-overlay-container #event-date-picker')
        # title_input.send_keys(today_str)
        # time.sleep(0.5)
        driver.find_element(CSS, '.v-overlay-container #meet-due-date').click()
        time.sleep(1)
        driver.find_element(CSS, '.v-overlay-container .v-date-picker-month__day .v-btn--variant-outlined').click()
        time.sleep(0.5)

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
        add_empty_block()

    # Meet
    def test_task():
        show_toolbar()
        driver.find_element(CSS, '.ce-popover-item[data-item-name="task"]').click()
        time.sleep(2)

        title_input = driver.find_element(CSS, '.v-overlay-container input[name="title"]')
        title_input.click()
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

        activate_editor('#task-editor')
        time.sleep(0.5)
        test_paragraph('#task-editor')

        driver.find_element(CSS, '.v-overlay-container .v-card-actions button.bg-primary').click()
        time.sleep(1)

        assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
        add_empty_block()

    # Page
    def test_board():
        if not DriverUtils.check_exists_by_css(driver, '.bg-pink-lighten-5:last-child'):
            show_toolbar()
            page_tool = driver.find_element(CSS, '.ce-popover-item[data-item-name="board"]')
            page_tool.click()
            time.sleep(0.5)
            driver.find_element(CSS, '.bg-pink-lighten-5:last-child').click()
            time.sleep(0.5)

        time.sleep(1)

        page_title_input = driver.find_element(CSS, '.v-overlay-container input[placeholder="page_title"]')
        page_title_input.clear()
        time.sleep(0.5)
        page_title_input.send_keys("Example board name")
        time.sleep(0.5)

        time.sleep(5)
        assert DriverUtils.check_exists_by_css(driver, '.excalidraw__canvas')

        driver.find_element(CSS, '.excalidraw label[title="Text — T or 8"]').click()
        action = ActionBuilder(driver)
        action.pointer_action.move_to_location(500, 500)
        action.pointer_action.click()
        action.perform()

        active_element = driver.switch_to.active_element
        active_element.send_keys("test board")
        time.sleep(2)

        driver.find_element(CSS, '.v-overlay-container .v-card-text .bg-green').click()
        time.sleep(2)

        driver.find_element(CSS, '.bg-pink-lighten-5:last-child').click()
        time.sleep(2)

        driver.find_element(CSS, '.v-overlay-container .v-card-text .bg-green').click()
        time.sleep(2)

        assert not DriverUtils.check_exists_by_css(driver, '.v-overlay.v-dialog')
        time.sleep(1)
        add_empty_block()

    # Test All
    def test_all():
        test_header()
        test_paragraph()
        test_delimiter()
        test_checklist()
        test_list()
        test_page()
        test_meet()
        test_task()
        test_board()

    test_all()