from driverfactory.driverinterface import DriverInterface
from selenium import webdriver
import allure


class ChromeDriver(DriverInterface):
    @allure.step("Initiate the Chrome")
    def initiate_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(options=options)
