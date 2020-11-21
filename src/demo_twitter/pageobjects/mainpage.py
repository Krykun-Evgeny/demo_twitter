from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from values import strings
from values import integers
import allure


class MainPage(BasePage):

    def __init__(self, driver):
        with allure.step("Finding components of the main page"):
            self.driver = driver
            webdriver_waiter = WebDriverWait(self.driver.instance, integers.default_timeout)
            self.body = webdriver_waiter.until(
                EC.presence_of_element_located((
                    By.ID, strings.general_id_body)),
                strings.id_is_not_present_timeout_message.format(strings.general_id_body))

            self.header = WebDriverWait(self.body, integers.default_timeout).until(
                EC.visibility_of_element_located((By.TAG_NAME, strings.html_tag_header)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_header))
            self.home_btn = BasePage.find_button(self.header, (By.CSS_SELECTOR,
                                                               strings.main_page_css_selector_home_btn))
            self.new_tweet_btn = BasePage.find_button(self.header, (By.CSS_SELECTOR,
                                                                    strings.main_page_css_selector_new_tweet_btn))

            self.main = WebDriverWait(self.body, integers.default_timeout).until(
                EC.visibility_of_element_located((By.TAG_NAME, strings.html_tag_main)),
                strings.tag_timeout_message.format(strings.general_id_body, strings.html_tag_main))
            self.primary_column = WebDriverWait(self.main, integers.default_timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, strings.main_page_css_selector_primary_column)),
                strings.css_selector_timeout_message.format(strings.html_tag_main,
                                                            strings.main_page_css_selector_primary_column))
            self.sidebar_column = WebDriverWait(self.main, integers.default_timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, strings.main_page_css_selector_sidebar_column)),
                strings.css_selector_timeout_message.format(strings.html_tag_main,
                                                            strings.main_page_css_selector_sidebar_column))
            self.modal_form_new_tweet = None
            self.draft_editor = None
            self.draft_editor_content = None
            self.toolbar = None
            self.tweet_btn = None
            self.own_tweets = []

    @allure.step("Verify main buttons (home, new_tweet)")
    def validate_buttons(self):
        for temp_button in [self.home_btn, self.new_tweet_btn]:
            BasePage.validate_element_is_displayed_and_enabled(self, temp_button)

    @allure.step("Handle a modal form of new tweet")
    def get_modal_form_new_tweet(self):
        self.modal_form_new_tweet = WebDriverWait(self.driver.instance, integers.default_timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, strings.main_page_css_selector_modal_form)),
            strings.assert_element_with_css_selector_is_not_presence.format(
                strings.main_page_css_selector_modal_form))
        modal_form_waiter = WebDriverWait(self.modal_form_new_tweet, integers.default_timeout)
        self.draft_editor = modal_form_waiter.until(
            EC.visibility_of_element_located((By.CLASS_NAME, strings.main_page_class_draft_editor)),
            strings.class_timeout_message.format(strings.main_page_css_selector_modal_form,
                                                 strings.main_page_class_draft_editor))
        self.draft_editor_content = WebDriverWait(self.draft_editor, integers.default_timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, strings.main_page_class_draft_editor_content)),
            strings.class_timeout_message.format(strings.main_page_class_draft_editor,
                                                 strings.main_page_class_draft_editor_content))
        self.toolbar = WebDriverWait(self.modal_form_new_tweet, integers.default_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, strings.main_page_css_selector_modal_form_toolbar)),
            strings.css_selector_timeout_message.format(strings.main_page_css_selector_modal_form,
                                                        strings.main_page_css_selector_modal_form_toolbar))
        self.tweet_btn = WebDriverWait(self.modal_form_new_tweet, integers.default_timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, strings.main_page_css_selector_modal_form_tweet_btn)),
            strings.css_selector_timeout_message.format(strings.main_page_css_selector_modal_form,
                                                        strings.main_page_css_selector_modal_form_tweet_btn))

    @allure.step("Modal form is closed and removed from DOM")
    def modal_form_new_tweet_is_removed(self):
        WebDriverWait(self.driver.instance, integers.default_timeout).until(
            EC.staleness_of(self.modal_form_new_tweet),
            strings.assert_element_with_css_selector_is_presence.format(
                strings.main_page_css_selector_modal_form))

    @allure.step("Get own tweets")
    def get_own_tweets(self):
        self.own_tweets = WebDriverWait(self.driver.instance, integers.default_timeout).until(
            EC.visibility_of_any_elements_located((
                By.CSS_SELECTOR, strings.main_page_css_selector_own_tweet)),
            strings.assert_element_with_css_selector_is_not_presence.format(
                strings.main_page_css_selector_own_tweet))

    @allure.step("Validate the added tweet")
    def validate_the_last_tweet(self, expected_string):
        spans = WebDriverWait(self.own_tweets[0], integers.default_timeout).until(
            EC.visibility_of_any_elements_located((
                By.TAG_NAME, strings.html_tag_span)),
            strings.tag_timeout_message.format(strings.main_page_css_selector_own_tweet,
                                               strings.html_tag_span))
        found = False
        for span in spans:
            if expected_string == span.text:
                found = True
        if not found:
            assert False, strings.main_page_own_tweet_is_nof_found.format(expected_string)

    @allure.step("Create a new tweet")
    def create_new_tweet(self, string_tweet="TEST"):
        with allure.step("Click on the 'New Tweet' button"):
            self.new_tweet_btn.click()
        self.get_modal_form_new_tweet()
        with allure.step("Set a tweet: {}".format(string_tweet)):
            self.draft_editor_content.send_keys(string_tweet)
        with allure.step("Verify a value of draft editor"):
            current_value = self.draft_editor.text
            assert current_value == string_tweet, strings.main_page_difference_in_values_assert_message. \
                format(string_tweet, current_value)
        with allure.step("Click on the 'Tweet' button"):
            self.tweet_btn.click()
        self.modal_form_new_tweet_is_removed()
        self.get_own_tweets()
        self.validate_the_last_tweet(expected_string=string_tweet)
