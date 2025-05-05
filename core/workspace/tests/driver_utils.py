import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class DriverUtils:

    @staticmethod
    def get_chrome_driver() -> webdriver.Chrome:
        # Create ChromeOptions to disable proxy
        chrome_options = Options()
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.add_argument('--proxy-server="direct://"')
        chrome_options.add_argument('--proxy-bypass-list=*')
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.ignore_local_proxy_environment_variables()

        # Start the WebDriver with these options
        driver = webdriver.Chrome(options=chrome_options, )
        return driver

    @staticmethod
    def arrived_to_url(driver, destination, max_second=5):
        check = 0
        while check <= max_second * 2:
            time.sleep(0.5)
            if destination in driver.current_url:
                break
            check += 1
        return destination in driver.current_url

    @staticmethod
    def login_and_return(driver) -> webdriver.Chrome:
        driver.get('http://localhost:3000/')
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
        return driver

    @staticmethod
    def delete_nuxt_dev_tools(driver):
        try:
            nuxt_dev_tools_element = driver.find_element(By.ID, 'nuxt-devtools-container')
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, nuxt_dev_tools_element)
        except:
            pass

    @staticmethod
    def check_exists_by_css(driver, selector):
        try:
            string = "var exists=document.querySelector('" + selector + "');return !!exists;"
            x = driver.execute_script(string)
            print(x)
            return x
        except NoSuchElementException:
            return False
        return True
