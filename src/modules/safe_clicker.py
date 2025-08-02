#!/usr/bin/env python3

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SafeClick:
    def __init__(self, driver):
        self.driver = driver

    def tryclick(self, element):
        try:
            self.scroll_into_view(element)
            self.driver.sleep(1)
            element.click()
        except Exception as e:
            print(f"Failed to click element: {element} with error: ", e)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            """
                let el = arguments[0];
                el.scrollIntoView({block: 'center', inline: 'nearest'});
                let parent = el.offsetParent;
                while (parent) {
                    parent.scrollTop = el.offsetTop - parent.offsetTop - parent.clientHeight/2;
                    parent = parent.offsetParent;
                }
            """,
            element,
        )

    def click_by_text(self, text):
        # wait for element to appear before clicking
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[normalize-space(text())='{text}']")
            )
        )
        self.tryclick(element)

    def click_by_id(self, ID):
        element = WebDriverWait(self.driver, 20).until(
            (EC.presence_of_element_located((By.ID, ID)))
        )
        self.tryclick(element)

    def click_btn_content(self, btncontent):
        button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//button[contains(text(), '{btncontent}')]")
            )
        )
        self.tryclick(button)
