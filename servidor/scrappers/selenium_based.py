from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from seleniumwire import webdriver as wire_webdriver


class SeleniumBasedScrapper:
    def __init__(self, url):
        self.url = url
        self.driver_options = webdriver.FirefoxOptions()
        self.driver_options.add_argument('--headless')
        self.driver_options.add_argument('--no-sandbox')
        self.driver_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Firefox(executable_path='', options=self.driver_options)
        self.driver.get(url)

    def get_page(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()


class SeleniumWireBasedScrapper:
    def __init__(self, url):
        self.url = url
        self.driver = wire_webdriver.Firefox(executable_path='')
        self.driver_options = wire_webdriver.FirefoxOptions()
        self.driver_options.add_argument('--headless')
        self.driver_options.add_argument('--no-sandbox')
        self.driver_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Firefox(executable_path='', options=self.driver_options)
        self.driver.get(url)

    def get_page(self):
        return self.driver.page_source

    def get_requests(self):
        return self.driver.requests

    def close(self):
        self.driver.close()
