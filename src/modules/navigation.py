#!/usr/bin/env python3

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Navigation:
    def __init__(self, driver, center, captcha_solver, safe_clicker):
        self.driver = driver
        self.center = center
        self.captcha_solver = captcha_solver
        self.clicker = safe_clicker

    def select_option_by_text(self, identifier, select_text, backup="Egypt"):
        select_element = self.driver.find_element(By.ID, identifier)
        try:
            Select(select_element).select_by_visible_text(select_text)
            print(f"{select_text} was found")
        except Exception:
            Select(select_element).select_by_visible_text(backup)
            print(f"Fallback to {backup}")

    def page_is_blank(self):
        return self.driver.execute_script(
            """
            return document.body === null ||
                   document.body.innerText.trim() === "" ||
                   document.body.offsetHeight === 0;
        """
        )

    def page_refresher(self):
        if not self.page_is_blank():
            print("Blank Check: Page not blank (change)")
            return
        while self.page_is_blank():
            print("Refreshing blank page")
            self.driver.refresh()
            self.driver.sleep(2)
        print("Blank page problem fixed")

    def back_to_prelogin(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "btn-apply-for-a-visa"))
            )
            return True
        except TimeoutException:
            return False

    def navigate_pre_login(self):
        try:
            # self.driver.click("#btn-apply-for-a-visa")
            self.clicker.click_by_id("btn-apply-for-a-visa")
            print("Clicked 'Prendre un rendez-vous'")
            self.driver.sleep(1)
            try:
                self.driver.find_element(By.ID, "btn-yes-uk-visa")
                print("Popup found, Clicking")
                self.driver.sleep(2)
                # self.driver.click("#btn-yes-uk-visa")
                self.clicker.click_by_id("btn-yes-uk-visa")
                self.driver.sleep(2)
                # self.driver.click("#btn-select-country")
                self.clicker.click_by_id("btn-select-country")
                self.driver.sleep(2)
                print("Clicked 'Sélectionner un pays'")
            except NoSuchElementException:
                print("No popup detected")
            self.select_option_by_text("select-country", "Égypte")
            self.driver.sleep(2)
            # self.driver.click("#btn-confirm-country")
            self.clicker.click_by_id("btn-confirm-country")
            print("Clicked 'Confirmer'")
            self.driver.sleep(2)
            self.captcha_solver.solve()
        except Exception as e:
            print(f"Error in pre-login navigation: {e}")

    def select_center(self):
        self.clicker.click_by_text(self.center)
        self.driver.sleep(2)
        self.captcha_solver.solve()
