from driverfactory.driverinterface import DriverInterface
from selenium import webdriver
import allure


class FirefoxDriver(DriverInterface):
    @allure.step("Initiate the Firefox")
    def initiate_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'en')
        return webdriver.Firefox(firefox_profile=profile)
