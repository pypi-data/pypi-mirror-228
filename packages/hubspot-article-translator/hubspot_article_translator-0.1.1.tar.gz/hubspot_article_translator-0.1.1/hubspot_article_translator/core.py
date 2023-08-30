import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .translation.helpers import translate, translateHTML

logger = logging.getLogger()


class State(object):
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, key: str):
        return self.__dict__.get(key, None)

    def __setattr__(self, key: str, value: any):
        self.__dict__[key] = value

    def __getitem__(self, key: str):
        return self.__getattr__(key)

    def __setitem__(self, key: str, value: any):
        self.__setattr__(key, value)

    def get(self, key: str):
        return self.__getitem__(key)

    def set(self, key: str, value: any):
        self.__setitem__(key, value)

    def mutate(self, **kwargs):
        return State(
            **{
                **self.__dict__,
                **kwargs
            }
        )


class Action(object):
    def __init__(
        self,
        *actions: "Action"
    ) -> None:
        self.actions = actions

    def execute(self, driver: webdriver.Chrome, state: State):
        for action in self.actions:
            action.execute(driver, state)


class ActionBranch(Action):
    def __init__(
        self,
        *actions: "Action",
        read_key: str,
        write_key: str
    ) -> None:
        super().__init__(*actions)
        self.read_key = read_key
        self.write_key = write_key

    def execute(
        self,
        driver: webdriver.Chrome,
        state: State
    ):
        for item in state[self.read_key]:
            mutated_state = state.mutate(
                **{
                    self.write_key: item
                }
            )
            super().execute(driver, mutated_state)


class SkipPopupAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        for data_key in [
            'knowledgeContentUI.edit.newInsertMenuPopover.dismissButton',
            'introModal.buttons.gotIt'
        ]:
            try:
                label = driver.find_element(By.CSS_SELECTOR, f'[data-key="{data_key}"]')
                if not label:
                    return
                button = label.find_element(By.XPATH, "./..")
                if not button:
                    return
                button.click()
                time.sleep(1)
            except Exception:
                pass


class LoginAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        driver.get('https://app.hubspot.com/login/beta')

        username_input = driver.find_element(value="username")
        username_input.send_keys(state.email)

        login_button = driver.find_element(value="loginBtn")
        login_button.click()
        time.sleep(1)

        password_input = driver.find_element(value="current-password")
        password_input.send_keys(state.password)

        login_button = driver.find_element(value="loginBtn")
        login_button.click()
        time.sleep(1)

        code_input = driver.find_element(value="code")
        code_input.send_keys(state.code)

        login_button = driver.find_element(
            by=By.CLASS_NAME,
            value="login-submit"
        )
        login_button.click()
        time.sleep(1)

        remember_button = driver.find_element(
            by=By.CSS_SELECTOR,
            value='[data-2fa-rememberme="false"]'
        )
        if remember_button:
            remember_button.click()
        time.sleep(3)


class NavigateToArticleAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        driver.get(f"https://app.hubspot.com/knowledge/{state.knowledge_base_id}/edit/{state.article_id}")
        time.sleep(3)
        SkipPopupAction().execute(driver, state)


class CreateVariantArticleAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        language_name = state.to_languages[state.to_language]
        create_variation_label = driver.find_element(By.CSS_SELECTOR, '[data-key="knowledgeContentUI.edit.languageSwitcher.languageActions.createLanguageVariant"]')
        create_variation_button = create_variation_label.find_element(By.XPATH, "./..")
        create_variation_button.click()
        time.sleep(1)

        language_dropdown_button = driver.find_element(By.CLASS_NAME, 'private-dropdown__caret--form')
        language_dropdown_button.click()
        time.sleep(1)

        language_selection_button = driver.find_element(By.CSS_SELECTOR, f'[title="{language_name}"]')
        if not language_selection_button:
            logger.warning(f"Unable to create `{language_name}` variant for Article `{state.article_id}`... Looks like the language isn't setup in Hubspot")
            return False

        language_selection_div = language_selection_button.find_element(By.XPATH, "./../..")
        if 'is-disabled' in language_selection_div.get_attribute('class'):
            logger.warning(f"Unable to create `{language_name}` variant for Article `{state.article_id}`... apparently is already exists but I couldn't find it")
            return False

        language_selection_button.click()
        time.sleep(1)

        save_label = driver.find_element(By.CSS_SELECTOR, '[data-key="knowledgeContentUI.manage.createLanguageVariantModal.buttons.save"]')
        save_button = save_label.find_element(By.XPATH, "./..")
        save_button.click()
        time.sleep(1)

        driver.refresh()
        time.sleep(3)
        return True


class NavigateToVariantArticleAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        language_name = state.to_languages[state.to_language]

        header = driver.find_element(By.CSS_SELECTOR, '[aria-label="Page Section"]')
        language_popup_button = header.find_elements(By.TAG_NAME, "BUTTON")[1]
        language_popup_button.click()
        time.sleep(1)

        language_popup_div = driver.find_element(By.CSS_SELECTOR, '[role="presentation"]')
        languages_tbody = language_popup_div.find_element(By.TAG_NAME, "TBODY")
        if language_name not in languages_tbody.text:
            if not CreateVariantArticleAction().execute(driver, state):
                return False

            return self.execute(driver, state)

        language_buttons = languages_tbody.get_property('children')
        language_button = [btn for btn in language_buttons if language_name in btn.text]
        if not language_button:
            return False

        language_button = language_button[0]
        if "Draft" not in language_button.text:
            logger.info(f"`{language_name}` variant of Article `{state.article_id}` is not in draft state, skipping...")
            return False

        language_button.click()
        time.sleep(1)

        SkipPopupAction().execute(driver, state)
        return True


class ArticleAction(Action):
    def get_title(self, driver: webdriver.Chrome):
        title_textarea = driver.find_element(By.CLASS_NAME, 'article-title-text')
        return title_textarea.text

    def get_subtitle(self, driver: webdriver.Chrome):
        title_textarea = driver.find_element(By.CLASS_NAME, 'article-subtitle-text')
        return title_textarea.text

    def get_body(self, driver: webdriver.Chrome):
        title_textarea = driver.find_element(By.CLASS_NAME, 'mce-content-body')
        return title_textarea.get_attribute("innerHTML")

    def set_title(self, driver: webdriver.Chrome, value):
        element = driver.find_element(By.CLASS_NAME, 'article-title-text')
        element.clear()
        element.send_keys(value)

    def set_subtitle(self, driver: webdriver.Chrome, value):
        element = driver.find_element(By.CLASS_NAME, 'article-subtitle-text')
        element.clear()
        element.send_keys(value)

    def set_body(self, driver: webdriver.Chrome, value):
        element = driver.find_element(By.CLASS_NAME, 'mce-content-body')
        driver.execute_script(
            'arguments[0].innerHTML = arguments[1]',
            element,
            value
        )
        self.save(driver, element)

    def save(self, driver: webdriver.Chrome, element):
        time.sleep(0.2)
        element.send_keys(" ")
        time.sleep(0.2)
        element.send_keys(Keys.BACKSPACE)
        time.sleep(0.2)


class CaptureArticleAction(ArticleAction):
    def execute(self, driver: webdriver.Chrome, state: State):
        state.title = self.get_title(driver)
        state.subtitle = self.get_subtitle(driver)
        state.body = self.get_body(driver)


class TranslateArticleAction(ArticleAction):
    def execute(self, driver: webdriver.Chrome, state: State):
        for state.to_language in state.to_languages:
            if NavigateToVariantArticleAction().execute(driver, state):
                self.set_title(
                    driver,
                    translate(
                        text=state.title,
                        from_language=state.from_language,
                        to_language=state.to_language
                    )
                )

                self.set_subtitle(
                    driver,
                    translate(
                        text=state.subtitle,
                        from_language=state.from_language,
                        to_language=state.to_language
                    )
                )

                self.set_body(
                    driver,
                    translateHTML(
                        html=state.body,
                        from_language=state.from_language,
                        to_language=state.to_language
                    )
                )
                SkipPopupAction().execute(driver, state)
                time.sleep(2)

                PublishArticleAction().execute(driver, state)
            else:
                time.sleep(3)
                driver.execute_script("window.onbeforeunload = function() {};")
                driver.refresh()
                time.sleep(3)


class PublishArticleAction(Action):
    def execute(self, driver: webdriver.Chrome, state: State):
        if not state.auto_publish:
            return

        publish_label = driver.find_element(By.CSS_SELECTOR, f'[data-key="knowledgeContentUI.button.publish"]')
        if not publish_label:
            logger.error(f"Unable to publish article `{state.article_id}... Publish label not found")
            return
        publish_button = publish_label.find_element(By.XPATH, "./..")
        if not publish_button:
            logger.error(f"Unable to publish article `{state.article_id}... Publish button not found")
            return
        publish_button.click()
        time.sleep(6)

        driver.back()
        time.sleep(3)
