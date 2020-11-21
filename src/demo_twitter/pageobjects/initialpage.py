from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from values import strings
from values import integers
import allure


class InitialPage(BasePage):

    def __init__(self, driver):
        with allure.step("Finding components of the initial page"):
            self.driver = driver
            webdriver_waiter = WebDriverWait(self.driver.instance, integers.default_timeout)

            self.body = webdriver_waiter.until(
                EC.presence_of_element_located((
                    By.ID, strings.general_id_body)),
                strings.id_is_not_present_timeout_message.format(strings.main_page_id_body))

            self.form_login = WebDriverWait(self.body, integers.default_timeout).until(
                EC.visibility_of_element_located((By.TAG_NAME, strings.html_tag_form)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_form))
            self.input_username = WebDriverWait(self.form_login, integers.default_timeout).until(
                EC.visibility_of_element_located((By.NAME, strings.initial_page_name_username)),
                strings.name_timeout_message.format(strings.html_tag_form,
                                                                 strings.initial_page_name_username))
            self.input_password = WebDriverWait(self.form_login, integers.default_timeout).until(
                EC.visibility_of_element_located((By.NAME, strings.initial_page_name_password)),
                strings.name_timeout_message.format(strings.html_tag_form,
                                                                 strings.initial_page_name_password))

            self.form_submit = BasePage.find_button(self.form_login, (By.CSS_SELECTOR,
                                                                      strings.initial_page_css_selector_form_submit))

            self.signup = BasePage.find_button(self.body, (By.CSS_SELECTOR, strings.initial_page_css_selector_signup))
            self.login = BasePage.find_button(self.body, (By.CSS_SELECTOR, strings.initial_page_css_selector_login))

            self.nav_footer = WebDriverWait(self.body, integers.default_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, strings.html_tag_nav)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_nav))

    @allure.step("Verify inputs of form")
    def validate_inputs(self):
        for temp_input in [self.input_username, self.input_password]:
            assert temp_input.is_enabled(), strings.input_enabling_assert_message.format(
                temp_input.get_attribute('name'))

    @allure.step("Verify main buttons (form_login, signup, login)")
    def validate_buttons(self):
        for temp_button in [self.form_submit, self.signup, self.login]:
            BasePage.validate_element_is_displayed_and_enabled(self, temp_button)

    @allure.step("Click on the 'Signup' button")
    def click_signup_button(self):
        self.signup.click()

    @allure.step("Click on the 'Login' button")
    def click_login_button(self):
        self.login.click()
