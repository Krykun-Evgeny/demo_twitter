from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from values import strings
from values import integers
import allure


class LoginPage(BasePage):

    def __init__(self, driver):
        with allure.step("Finding components of the login page"):
            self.driver = driver
            webdriver_waiter = WebDriverWait(self.driver.instance, integers.default_timeout)

            self.body = webdriver_waiter.until(
                EC.presence_of_element_located((
                    By.ID, strings.general_id_body)),
                strings.id_is_not_present_timeout_message.format(strings.general_id_body))

            self.form_login = WebDriverWait(self.body, integers.default_timeout).until(
                EC.visibility_of_element_located((By.TAG_NAME, strings.html_tag_form)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_form))
            self.input_username = WebDriverWait(self.form_login, integers.default_timeout).until(
                EC.visibility_of_element_located((By.NAME, strings.login_page_name_username)),
                strings.name_timeout_message.format(strings.html_tag_form,
                                                    strings.login_page_name_username))
            self.input_password = WebDriverWait(self.form_login, integers.default_timeout).until(
                EC.visibility_of_element_located((By.NAME, strings.login_page_name_password)),
                strings.name_timeout_message.format(strings.html_tag_form,
                                                    strings.login_page_name_password))

            self.form_submit = BasePage.find_button(self.form_login, (By.CSS_SELECTOR,
                                                                      strings.login_page_css_selector_form_submit))

            self.links = WebDriverWait(self.body, integers.default_timeout).until(
                EC.visibility_of_all_elements_located((By.TAG_NAME, strings.html_tag_a)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_a))

    @allure.step("Verify inputs of form")
    def validate_inputs(self):
        for temp_input in [self.input_username, self.input_password]:
            assert temp_input.is_enabled(), strings.input_enabling_assert_message.format(
                temp_input.get_attribute('name'))

    @allure.step("Verify links")
    def validate_links(self):
        for temp_link in self.links:
            assert temp_link.is_enabled(), strings.href_enabling_assert_message.format(
                temp_link.text)

    @allure.step("Verify a main button (login)")
    def validate_button(self):
        BasePage.validate_element_is_displayed_and_enabled(self, self.form_submit)

    @allure.step("Login")
    def login(self, username="test", password="test"):
        with allure.step("Set username: {}".format(username)):
            self.input_username.send_keys(username)
            username_dic = {
                'expected_value': username,
                'obj': self.input_username
            }
        with allure.step("Set password: {}".format(password)):
            self.input_password.send_keys(password)
            password_dic = {
                'expected_value': password,
                'obj': self.input_password
            }
        with allure.step("Verify values of input"):
            for temp_input in [username_dic, password_dic]:
                current_value = temp_input['obj'].get_attribute(strings.attribute_value)
                assert current_value == temp_input['expected_value'], \
                    strings.login_page_difference_in_values_assert_message. \
                    format(temp_input['expected_value'], current_value)

        with allure.step("Click on the 'Login' button"):
            self.form_submit.click()
